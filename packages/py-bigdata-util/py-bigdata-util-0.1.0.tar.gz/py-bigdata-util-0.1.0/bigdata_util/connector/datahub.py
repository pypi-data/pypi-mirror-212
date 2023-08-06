#!/usr/bin/env python3
# -*- coding=utf-8 -*-

from collections import OrderedDict
from datahub import DataHub
from datahub.exceptions import ResourceNotFoundException

from bigdata_util.connector.datahub_reader import DatahubReader
from bigdata_util.util import load_csv, save_csv, get_logger
from datahub.models import OdpsConnectorConfig, ConnectorType, PartitionMode, FieldType, RecordSchema, \
    DatabaseConnectorConfig, ListSubscriptionResult, Subscription, CursorType
from pydash import _

logger = get_logger(__file__)


class DatahubConnector(DataHub):

    def __init__(self, *args, **kwargs):
        if len(args) > 0 and isinstance(args[0], dict):
            super(DatahubConnector, self).__init__(
                _.get(args[0], 'access_id', _.get(args[0], 'accessId')),
                _.get(args[0], 'access_key', _.get(args[0], 'accessKey')),
                endpoint=_.get(args[0], 'endpoint', _.get(args[0], 'endPoint')),
                **kwargs
            )
        else:
            super(DatahubConnector, self).__init__(*args, **kwargs)
        pass

    @staticmethod
    def is_datahub_connector() -> bool:
        return True

    @staticmethod
    def datahub_col_type_mapping(col_type):
        col_type = col_type.lower()
        if col_type in ('string', 'char', 'varchar'):
            return FieldType.STRING
        if col_type in ('int', 'bigint', 'long'):
            return FieldType.BIGINT
        if col_type in ('double', 'float', 'number'):
            return FieldType.DOUBLE
        pass

    def delete_connectors(self, project_name, topic_name):
        connector_detail_list = []

        connector_ids = self.list_connector(project_name, topic_name).connector_ids
        connector_types = []
        for connector_id in connector_ids:
            connector_types.append(self.get_connector(project_name, topic_name, connector_id).type)
        for connector_type in connector_types:
            connector_detail_list.append(
                self.get_connector(project_name, topic_name, ConnectorType(connector_type))
            )
            self.delete_connector(project_name, topic_name, ConnectorType(connector_type))
            logger.info('delete')
            pass

        return connector_detail_list, connector_types

    def delete_subscriptions(self, project_name, topic_name):
        r: ListSubscriptionResult = self.list_subscription(project_name, topic_name, '', 1, 10)
        for sub in self.list_subscription(project_name, topic_name, '', 1, r.total_count).subscriptions:
            sub: Subscription = sub
            self.delete_subscription(project_name, topic_name, sub.sub_id)
            pass
        pass

    def create_or_update_register_topic(
            self,
            project_name,
            topic_name,
            column_meta_list,
            record_type='TUPLE',
            shards_cnt=3,
            lifecycle=7,
            comment='Registered by py-bigdate-util.'
    ):
        if len(column_meta_list) == 0:
            raise Exception(f'没有提供创建datahub的信息')
        # delete connectors
        topic_meta = None
        try:
            topic_meta = self.get_topic(project_name, topic_name)
            original_field_list = topic_meta.record_schema.field_list
            need_update = False
            if len(original_field_list) == len(column_meta_list):
                for idx, field_meta in enumerate(original_field_list):
                    column_meta = column_meta_list[idx]
                    if field_meta.name != column_meta['fieldName'] or \
                            field_meta.type != self.datahub_col_type_mapping(column_meta['fieldType']):
                        need_update = True
                        break
            else:
                need_update = True

            if topic_meta.life_cycle != lifecycle:
                need_update = True

            if topic_meta.shard_count != shards_cnt:
                need_update = True
        except ResourceNotFoundException:
            need_update = True

        if not need_update:
            logger.info(f'topic {topic_name} not updated.')
            return

        connector_detail_list = []
        connector_types = []
        if topic_meta:
            connector_detail_list, connector_types = self.delete_connectors(project_name, topic_name)
            self.delete_subscriptions(project_name, topic_name)
            self.delete_topic(project_name, topic_name)

        if record_type == 'TUPLE':
            self.create_tuple_topic(
                project_name,
                topic_name,
                shards_cnt,
                lifecycle,
                RecordSchema.from_lists(
                    list(map(
                        lambda x: x['fieldName'],
                        column_meta_list
                    )),
                    list(map(
                        lambda x: self.datahub_col_type_mapping(x['fieldType']),
                        column_meta_list
                    ))
                ),
                comment
            )
        else:
            self.create_blob_topic(project_name, topic_name, shards_cnt, lifecycle, comment)

        logger.warn(f'''
        datahub topic 已重建，手动添加各个 connectors ， 原有的 connector 列表为:
        {", ".join(list(map(lambda x: x.name, connector_types)))}
        {", ".join(list(map(lambda x: x.value, connector_types)))}
''')
        # # 新版的pydatahub在connector详情中不返回connector的ak信息，因此无法自动重建
        # for connector_detail in connector_detail_list:
        #     self.create_connector(
        #         project_name,
        #         topic_name,
        #         connector_detail.type,
        #         [v['fieldName'] for v in column_meta_list],
        #         connector_detail.config
        #     )
        #     pass
        pass

    def add_odps_connector(
            self,
            project_name,
            topic_name,
            odps_project,
            odps_endpoint,
            odps_ak_id,
            odps_ak_key,
            column_fields,
            column_partitions,
            odps_table_name=None,
            partition_mode=PartitionMode.USER_DEFINE,
            time_range=0
    ):
        if odps_table_name is None:
            odps_table_name = topic_name
        partition_config = OrderedDict([(v, v) for v in column_partitions])
        odps_connector_config = OdpsConnectorConfig(
            odps_project,
            odps_table_name,
            odps_endpoint,
            '',
            odps_ak_id,
            odps_ak_key,
            partition_mode,
            time_range,
            partition_config
        )
        if ConnectorType.SINK_ODPS.name in self.list_connector(project_name, topic_name).connector_names:
            self.delete_connector(project_name, topic_name, ConnectorType.SINK_ODPS)
        self.create_connector(
            project_name, topic_name, ConnectorType.SINK_ODPS,
            column_fields, odps_connector_config
        )
        self.reload_connector(project_name, topic_name, ConnectorType.SINK_ODPS)
        pass

    def add_mysql_connector(
            self,
            project_name,
            topic_name,
            mysql_host,
            mysql_db,
            mysql_user,
            mysql_passwd,
            column_fields,
            mysql_port=3306,
            mysql_table_name=None,
            max_commit_size=-1,
            ignore=True
    ):
        if mysql_table_name is None:
            mysql_table_name = topic_name

        database_connector_config = DatabaseConnectorConfig(
            mysql_host,
            mysql_port,
            mysql_db,
            mysql_user,
            mysql_passwd,
            mysql_table_name,
            max_commit_size,
            ignore
        )

        if ConnectorType.SINK_MYSQL.name in self.list_connector(project_name, topic_name).connector_names:
            self.delete_connector(project_name, topic_name, ConnectorType.SINK_MYSQL)
        self.create_connector(
            project_name, topic_name, ConnectorType.SINK_MYSQL,
            column_fields, database_connector_config
        )
        self.reload_connector(project_name, topic_name, ConnectorType.SINK_MYSQL)
        pass

    def get_reader(self,project_name, topic_name, shard_id='0'):
        return DatahubReader(project_name,topic_name,self,shard_id)

    def get_last_n_records(self, project_name, topic_name, shard_id='0', limit_num=10):
        if project_name is None:
            project_name = self.get_project()

        if limit_num <= 0:
            limit_num = 0
        else:
            limit_num = limit_num - 1

        sequence = self.get_cursor(
            project_name, topic_name, shard_id, CursorType.LATEST
        ).sequence
        cursor = self.get_cursor(
            project_name, topic_name, shard_id, CursorType.SEQUENCE, sequence - limit_num
        ).cursor
        record_schema = self.get_topic(project_name, topic_name).record_schema
        records = self.get_tuple_records(
            project_name, topic_name, shard_id, record_schema, cursor, limit_num
        )

        result = []
        for record in records.records:
            row = {}
            for field in record.field_list:
                row[field.name] = record.get_value(field.name)
            result.append(row)

        return result
