#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import os
from odps import ODPS, options
from odps.models import Schema
from odps.errors import NoSuchObject
from odps.models.table import Table

from bigdata_util.connector.base_query import IBaseQuery
from bigdata_util.util import load_csv, save_csv, get_logger
from datetime import datetime, timedelta
from bigdata_util.util.table_info import TableInfo
import urllib3
import requests
import re
import hashlib
from pydash import _
options.verbose = True
options.connect_timeout = 1200
logger = get_logger(__file__)


class MaxcomputeTable(Table):
    def __init__(self, *args, **kwargs):
        self._maxcompute_proxy = kwargs['proxy']
        super(Table, self).__init__(*args, **kwargs)

    def open_reader(self, *args, **kwargs):
        if self.parent.parent.parent._client._proxy is not None:
            options.data_proxy = self.parent.parent.parent._client._proxy['http']
        r = self.open_reader_back(*args, **kwargs)
        options.data_proxy = None
        return r

    def open_writer(self, *args, **kwargs):
        if self.parent.parent.parent._client._proxy is not None:
            options.data_proxy = self.parent.parent.parent._client._proxy['http']
        r = self.open_writer_back(*args, **kwargs)
        options.data_proxy = None
        return r

MaxcomputeTable = MaxcomputeTable


Table.open_reader_back = Table.open_reader
Table.open_reader = MaxcomputeTable.open_reader
Table.open_writer_back = Table.open_writer
Table.open_writer = MaxcomputeTable.open_writer
Table.maxcompute_proxy = None


class MaxcomputeConnector(ODPS, IBaseQuery):
    cache_data_dir = '.connector_maxcompute_cache'

    def __init__(self, *args, **kwargs):
        if len(args) > 0 and isinstance(args[0], dict):
            proxy = _.get(args[0], 'proxy', None)
            if proxy is not None:
                if 'proxy' not in kwargs:
                    kwargs['proxy'] = proxy
                else:
                    logger.warning('[MaxcomputeConnector] proxy option in dict is ignored.')
            self.__init__with_proxy(
                _.get(args[0], 'access_id', _.get(args[0], 'accessId')),
                _.get(args[0], 'access_key', _.get(args[0], 'accessKey')),
                _.get(args[0], 'project'),
                endpoint=_.get(args[0], 'endpoint', _.get(args[0], 'endPoint')),
                logview_host=_.get(args[0], 'logview_host'),
                **kwargs
            )
        else:
            self.__init__with_proxy(*args, **kwargs)
        pass

    def save_odps_ini_file(self, filename):
        from configobj import ConfigObj
        cfg = ConfigObj(encoding='utf8')
        cfg.filename = filename
        cfg['access_id'] = self.account.access_id
        cfg['access_key'] = self.account.secret_access_key
        cfg['project_name'] = self.project
        cfg['end_point'] = self.endpoint
        cfg['logview_host'] = self.logview_host

        try:
            cfg.write()
        except Exception as e:
            logger.error(e)
            pass
        pass

    def execute_sql(self, sql, sql_hints=None):
        return self.run_sql_with_logview(sql, sql_hints=sql_hints)

    def __init__with_proxy(self, *args, **kwargs):
        if 'proxy' in kwargs:
            from odps.config import options
            options.api_proxy = kwargs['proxy']
            super(MaxcomputeConnector, self).__init__(*args, **kwargs)
            options.api_proxy = None
            self._maxcompute_proxy = kwargs['proxy']
        else:
            super(MaxcomputeConnector, self).__init__(*args, **kwargs)
            self._maxcompute_proxy = None
        pass

    @staticmethod
    def __has_force_cache_flag_in_env() -> bool:
        return 'FORCE_RECACHE' in os.environ

    @staticmethod
    def __get_cache_file_suffix(partition):
        cache_file_suffix = ''
        if partition:
            partition = str(partition)
            pts = partition.split(',')
            pt_json = {}
            for pt in pts:
                pt_kv = pt.split('=')
                pt_json[pt_kv[0]] = pt_kv[1].strip("'").strip('"')
            pt_keys = list(pt_json.keys())
            pt_keys.sort()

            for key in pt_keys:
                cache_file_suffix += '_' + pt_json[key]
        return cache_file_suffix

    def get_table(self, *args, **kwargs):
        if len(args) > 0 and isinstance(args[0], TableInfo):
            table_info: TableInfo = args[0]
            kwargs['name'] = table_info.table_name
            kwargs['project'] = table_info.project
            result_table: Table = super().get_table(*[], **kwargs)
        else:
            result_table: Table = super().get_table(*args, **kwargs)

        return result_table

    def copy_table_from(self, original_odps_ins, table_info):
        original_odps_ins.copy_table_to(self, table_info)

    def copy_table_to(self, target_odps_ins, table_info: TableInfo):
        t_original = self.get_table(table_info)
        ddl = t_original.get_ddl(with_comments=True, if_not_exists=True)
        ddl = ddl.replace(self.project + '.', target_odps_ins.project + '.')
        data_list = self.get_table_data(table_info)

        target_odps_ins.run_sql_with_logview(ddl)
        t_target = target_odps_ins.get_table(table_info)

        if len(data_list) == 0:
            return

        if 'PARTITIONED BY' in ddl:
            t_target.delete_partition(partition_spec=table_info.get_partition(), if_exists=True)
            target_odps_ins.write_table(table_info.get_table_name(), list(map(
                lambda x: [x[name] for name in t_target.schema.names],
                data_list
            )), partition=table_info.get_partition(), create_partition=True)
        else:
            t_target.truncate()
            target_odps_ins.write_table(table_info.get_table_name(), list(map(
                lambda x: [x[name] for name in t_target.schema.names],
                data_list
            )))
        pass

    @staticmethod
    def __check_cache_dir_exist():
        if not os.path.exists(MaxcomputeConnector.cache_data_dir):
            logger.info('py_connector maxcompute cache dir not found, creating: ' + MaxcomputeConnector.cache_data_dir)
            os.makedirs(MaxcomputeConnector.cache_data_dir)
        pass

    @staticmethod
    def __get_full_cache_file_name(filename):
        return os.path.join(MaxcomputeConnector.cache_data_dir, filename)

    @staticmethod
    def __get_data_from_cache(table_name, cache_file_suffix, sep='$'):
        # MaxcomputeConnector.__check_cache_dir_exist()
        filename = MaxcomputeConnector.__get_full_cache_file_name(table_name + cache_file_suffix + '.csv')
        logger.info('loading data from cache file: ' + filename)
        return load_csv(filename, sep=sep)

    @staticmethod
    def __adjust_partition(partition):
        if type(partition) is not str:
            return partition

        return partition.replace('/', ',')

    def run_sql_in_file(self, file_name, placeholder_value_map=None, sql_hints=None):
        """
        run sql in maxcompute file, support placeholder values.
        :param sql_hints:
        :param file_name:
        :param placeholder_value_map:
        :return:
        """
        if placeholder_value_map is None:
            placeholder_value_map = {}
        if sql_hints is None:
            sql_hints = {}
        with open(file_name, mode='rb') as reader:
            sql_list_str = reader.read().decode('utf-8')
            sql_list_str = self.__replace_placeholder_values(sql_list_str, placeholder_value_map)

            sql_list = re.split(';[$\n]', sql_list_str)
            for sql in sql_list:
                self.run_sql_with_logview(sql, sql_hints=sql_hints)
                pass
            pass
        pass

    def run_sql_return_plain_json(self, *args, **kwargs):
        return self.run_sql_with_logview_return_plain_json(*args, **kwargs)

    def run_sql_with_logview_return_plain_json(self, original_sql, sql_hints=None, param_map=None):
        return self.run_sql_with_logview(original_sql, sql_hints, return_type='plain_json', param_map=param_map)

    def run_sql_with_logview_return_records(self, original_sql, sql_hints=None, param_map=None):
        return self.run_sql_with_logview(original_sql, sql_hints, return_type='records', param_map=param_map)

    def run_sql_with_logview(self, original_sql, sql_hints=None, return_type='instance', param_map=None, wait_complete=True):
        if param_map is not None:
            original_sql = self.__replace_placeholder_values(original_sql, param_map)

        if sql_hints is None:
            sql_hints = {}
        sql = original_sql.strip()
        sql = '\n'.join(list(filter(
            lambda x: x and not x.startswith('--'),
            sql.split('\n')
        )))
        if sql != '':
            logger.info('''
executing sql:
{sql}
                    '''.format(
                sql=sql
            ))
            priority = 7
            if sql_hints is not None and 'odps.instance.priority' in sql_hints:
                priority = int(sql_hints['odps.instance.priority'])
            instance = self.run_sql(sql, priority=priority, hints=sql_hints)
            logger.info('''
=========================>
logview: {logview}
waiting for finishing...
                    '''.format(
                logview=instance.get_logview_address()
            ))

            if wait_complete:
                instance.wait_for_success()
            else:
                return instance

            logger.info('<=========================== sql execution done.')
            if return_type == 'instance':
                return instance
            if return_type == 'plain_json':
                columns = []
                records = []

                if instance._client._proxy is not None:
                    options.data_proxy = instance._client._proxy['http']
                with instance.open_reader() as reader:
                    options.data_proxy = None
                    for meta in reader:
                        if len(columns) == 0:
                            columns = list(map(
                                lambda x: x.name,
                                meta.__getattribute__('_columns')
                            ))
                        m = {}
                        for col in columns:
                            m[col] = meta[col]
                        records.append(m)

                return records
            elif return_type == 'records':
                if instance._client._proxy is not None:
                    options.data_proxy = instance._client._proxy['http']
                with instance.open_reader() as reader:
                    records = list(reader)
                    options.data_proxy = None
                return records
        else:
            # logger.info('empty sql, skipped.')
            return None
        pass

    def update_udf(self, udf_name, class_name, resource_name):
        """
        force update udf.
        :param udf_name:
        :param class_name:
        :param resource_name:
        :return:
        """
        if self.exist_function(udf_name):
            self.delete_function(udf_name)
        self.create_function(
            udf_name,
            class_type=class_name,
            resources=[resource_name]
        )

    @staticmethod
    def get_file_md5(file_path):
        md5 = None
        if os.path.isfile(file_path):
            f = open(file_path, 'rb')
            md5_obj = hashlib.md5()
            md5_obj.update(f.read())
            hash_code = md5_obj.hexdigest()
            f.close()
            md5 = str(hash_code).lower()
        else:
            raise Exception(f'resource file `{file_path}` not exists!')
        return md5

    def update_file_resource(self, rsc_name, rsc_type, filepath):
        result = None
        need_udpate = True

        # 确定rsc_name是否需要更新
        if self.exist_resource(rsc_name):
            exist_rsc = self.get_resource(rsc_name)
            file_md5 = self.get_file_md5(filepath)

            if exist_rsc.content_md5 == file_md5:
                need_udpate = False
                result = exist_rsc
                # logger.debug(f'resource {rsc_name} not modified, using cache.')
            else:
                self.delete_resource(rsc_name)
            pass

        if need_udpate:
            from io import BytesIO
            result = self.create_resource(
                rsc_name,
                rsc_type,
                fileobj=BytesIO(open(filepath, 'rb').read())
            )

        return result

    @staticmethod
    def get_default_mr_jar_resource_name(name):
        return f'bigdata_util_{name}.jar'

    def update_mr_jar(self, mr_jar_base_path, project_base_path=None, mr_jar_name='default_jar_name.jar', resource_name=''):
        file_md5 = MaxcomputeConnector.get_file_md5(os.path.join(mr_jar_base_path, 'target', mr_jar_name))

        if not resource_name:
            resource_name = MaxcomputeConnector.get_default_mr_jar_resource_name(file_md5)
        logger.info('uploading mr jar: "{mr_jar_name}" -> "{resource_name}"'.format(
            mr_jar_name=mr_jar_name,
            resource_name=resource_name
        ))

        if project_base_path is not None and project_base_path != '':
            self.copy_mr_jar(mr_jar_base_path, project_base_path, mr_jar_name)

        try:
            resource = self.get_resource(resource_name)
            if resource.content_md5 == MaxcomputeConnector.get_file_md5(os.path.join(mr_jar_base_path, 'target', mr_jar_name)):
                return resource_name
        except NoSuchObject:
            pass

        if self.exist_resource(resource_name):
            self.delete_resource(resource_name)

        self.create_resource(
            resource_name,
            'jar',
            file_obj=open(os.path.join(mr_jar_base_path, 'target', mr_jar_name), 'rb')
        )
        return resource_name

    def update_resource(self, resource_name=None, table_name=None, partition=None):
        if not table_name:
            raise Exception('no table name provided.')
        if resource_name is None:
            resource_name = table_name

        self.delete_resource(resource_name)
        if not partition:
            self.create_resource(resource_name, type='table', table_name=table_name)
        else:
            self.create_resource(resource_name, type='table', table_name=table_name, partition=partition)
        pass

    @staticmethod
    def copy_mr_jar(mr_jar_base_path, project_base_path, mr_jar_name):
        """
        若在本地开发环境中，拷贝jar包到本项目对应目录下以执行最新jar包代码
        :return:
        """
        if mr_jar_base_path == project_base_path:
            return

        source_absolute_path = os.path.join(mr_jar_base_path, 'target')
        target_absolute_path = os.path.join(project_base_path, 'target')
        if not os.path.exists(target_absolute_path):
            os.makedirs(target_absolute_path)

        source_absolute_file = os.path.join(source_absolute_path, mr_jar_name)
        target_absolute_file = os.path.join(target_absolute_path, mr_jar_name)
        open(target_absolute_file, "wb").write(open(source_absolute_file, "rb").read())

    @staticmethod
    def __replace_placeholder_values(original_sql: str, value_map: dict) -> str:
        result_sql = original_sql

        pattern = re.compile(r'\${.*?}')
        placeholder_value_map = {}
        for key in pattern.findall(result_sql):
            key_in_map = key[2:-1].split('.')[0]
            if key_in_map not in value_map:
                continue
            placeholder_value_map[key] = key[1:].format(**value_map)

        for key in placeholder_value_map.keys():
            result_sql = result_sql.replace(key, str(placeholder_value_map[key]))
            pass

        return result_sql

    def get_table_data(self, table_name, partition=None, project=None, sep='$', ignore_cache=False):
        if isinstance(table_name, TableInfo):
            table_info = table_name
            table_name = table_info.table_name
            partition = table_info.partition
            project = table_info.project

        # force cache in env
        if MaxcomputeConnector.__has_force_cache_flag_in_env():
            ignore_cache = True

        partition = self.__adjust_partition(partition)
        if not ignore_cache:
            return self.__get_table_with_cache(table_name, partition, project, sep)
        else:
            return self.__get_table_re_cache(table_name, partition, project, sep)
        pass

    def __file_fresh_than_table(self, table_name, partition, project):
        """
        比较
        table_last_modified_time
        file_last_modified_time
        :return:
        """
        try:
            MaxcomputeConnector.__check_cache_dir_exist()
            cache_file_suffix = self.__get_cache_file_suffix(partition)
            filename = MaxcomputeConnector.__get_full_cache_file_name(table_name + cache_file_suffix + '.csv')
            file_last_modified_time = datetime.fromtimestamp(os.path.getmtime(filename))
        except FileNotFoundError:
            # 文件不存在，必须要从odps上拉
            return False

        try:
            table = self.get_table(table_name, project=project)
            table_last_modified_time = table.last_modified_time
        except ConnectionError:
            # 文件存在但没有网的时候可以继续使用cache table
            return True
        except urllib3.exceptions.NewConnectionError:
            return True
        except urllib3.exceptions.MaxRetryError:
            return True
        except requests.exceptions.ConnectionError:
            return True

        if timedelta(minutes=5) < file_last_modified_time - table_last_modified_time:
            return True
        else:
            return False
        pass

    def __get_table_with_cache(self, table_name, partition=None, project=None, sep='$'):
        """
        从odps下载，并cache到本地，
        此处做了升级： 如果odps里的表更新时间比本地文件的时间新，则更新本地的cache；操作为 查看odps表的update时间、本地文件的update时间。
        :param table_name:
        :param partition:
        :param project:
        :param sep:
        :return:
        """
        if self.__file_fresh_than_table(table_name, partition, project):
            cache_file_suffix = self.__get_cache_file_suffix(partition)
            records = self.__get_data_from_cache(table_name, cache_file_suffix)
            return records

        return self.__get_table_re_cache(table_name, partition, project, sep)

    def __get_table_re_cache(self, table_name, partition=None, project=None, sep='$'):
        """
        从odps拿到这张表的信息，忽略本地cache，并刷新cache
        """
        cache_file_suffix = self.__get_cache_file_suffix(partition)

        t = self.get_table(table_name, project=project)

        '''
        若输入的分区不存在，则返回空数组
        '''
        if partition and not t.exist_partition(partition):
            return []

        columns = t.schema.names
        rows = []
        records = []

        with t.open_reader(partition=partition) as reader:
            for meta in reader:
                row = [meta[key] for key in columns]
                m = {}
                for col in columns:
                    m[col] = meta[col]
                records.append(m)
                rows.append(row)

        MaxcomputeConnector.__check_cache_dir_exist()
        filename = MaxcomputeConnector.__get_full_cache_file_name(table_name + cache_file_suffix + '.csv')
        save_csv(filename, records, sep=sep)
        return records

    def create_ots_external_table(self, original_table_name, key_list, ots_id=None, ots_key=None, endpoint='hzbrainv2.cn-hangzhou-hzbjxn-d01.ots-internal.hzjjcloud.bj.cn', ots_location=None):
        if endpoint.startswith('http://'):
            endpoint = endpoint[7:]
        if endpoint.startswith('https://'):
            endpoint = endpoint[8:]

        external_table_name = 'ots_external_' + original_table_name
        self.delete_table(external_table_name, if_exists=True)

        t = self.get_table(original_table_name)

        schema_column_list = []
        columns_mapping = [':' + key for key in key_list]
        for key in key_list:
            schema_column_list.append(
                list(filter(
                    lambda c: c.name == key,
                    t.schema.columns
                ))[0]
            )
        for col in t.schema.columns:
            if col.name not in key_list:
                columns_mapping.append(col.name)
                schema_column_list.append(col)
            pass

        storage_handler = 'com.aliyun.odps.TableStoreStorageHandler'
        serde_properties = {
            'tablestore.columns.mapping': ','.join(columns_mapping),
            'tablestore.table.name': t.name
        }
        if ots_location is not None:
            location = ots_location
        else:
            location = f'tablestore://{ots_id}:{ots_key}@{endpoint}'
        self.create_table(external_table_name, schema=Schema(columns=schema_column_list), **{
            'storage_handler': storage_handler,
            'serde_properties': serde_properties,
            'location': location
        })
        return external_table_name

    def update_table_resource(self, resource_table: TableInfo):
        if self.exist_resource(resource_table.get_resource_name()):
            self.delete_resource(resource_table.get_resource_name())
        self.create_resource(
            resource_table.get_resource_name(),
            'table',
            table_name=resource_table.get_table_name_with_project(),
            partition=resource_table.get_partition(),
            # project=resource_table.get_project()      # 注册资源只准注册在本 odps_ins 的 project
        )

    def run_mr(
            self,
            project_base_path,
            mr_jar_name,
            mapper_class,
            mapper_key,
            mapper_value,
            reducer_class,
            input_table,
            output_table,
            mr_jar_path=None,
            resource_table=None,
            user_defined_param=None,
            split_size=32,
            reduce_cnt=100,
            reduce_mem=4096,
            key_sort_cols=None,
            partition_cols=None,
            value_group_cols=None,
    ):
        """
        :param project_base_path: 项目地址
        :param mr_jar_name:
        :param mapper_class:
        :param mapper_key:
        :param mapper_value:
        :param reducer_class:
        :param input_table:
        :param output_table:
        :param mr_jar_path: mr_jar的地址
        :param resource_table:
        :param user_defined_param:
        :param split_size:
        :param reduce_cnt:
        :param reduce_mem:
        :param key_sort_cols:
        :param partition_cols:
        :param value_group_cols:
        :return:
        """
        if mr_jar_path is not None:
            self.update_mr_jar(mr_jar_path, project_base_path, mr_jar_name, mr_jar_name)

        proxy_prefix = ''
        if self.rest._proxy is not None:
            proxy_info = self.rest._proxy['http']
            if proxy_info.startswith('socks5://'):
                host_port = proxy_info.split('://')[1].split(':')
                proxy_prefix = f' -DsocksProxyHost={host_port[0]} -DsocksProxyPort={host_port[1]} '
            else:
                raise Exception(f'proxy type {proxy_info} not supported!')

        if isinstance(input_table, TableInfo):
            input_table = [input_table]
        if isinstance(output_table, TableInfo):
            output_table = [output_table]
        if resource_table is None:
            resource_table = []
        elif isinstance(resource_table, TableInfo):
            resource_table = [resource_table]

        for rsc_table in resource_table:
            self.update_table_resource(rsc_table)

        input_table_name = ' '.join(list(map(
            lambda x: x.get_table_name_with_project(),
            input_table
        )))
        input_table_partition = ' '.join(list(map(
            lambda x: x.get_partition(),
            list(filter(
                lambda t: t.get_partition() is not None,
                input_table
            ))
        )))
        output_table_name = ' '.join(list(map(
            lambda x: x.get_table_name_with_project(),
            output_table
        )))
        output_table_partition = ' '.join(list(map(
            lambda x: x.get_partition(),
            list(filter(
                lambda t: t.get_partition() is not None,
                output_table
            ))
        )))
        resource_table_str = ' '.join(list(map(
            lambda x: x.get_resource_name(),
            resource_table
        )))

        if user_defined_param is None:
            user_defined_param = {}
        if key_sort_cols is not None:
            user_defined_param['keySortCols'] = key_sort_cols
        if partition_cols is not None:
            user_defined_param['partitionCols'] = partition_cols
        if value_group_cols is not None:
            user_defined_param['valueGroupCols'] = value_group_cols

        user_defined_param_str = ' '.join(list(map(
            lambda x: '-' + x + ' ' + str(user_defined_param[x]),
            user_defined_param.keys()
        )))

        cmd = f'''
            java {proxy_prefix} -Djava.ext.dirs={project_base_path}/target/lib -cp
                target/{mr_jar_name}
                com.aliyun.citybrain.traffic.MapReduceLauncher
            -access_id {self.account.access_id}
            -access_key {self.account.secret_access_key}
            -endpoint {self.endpoint}
            -logview_host {self.logview_host}
            -project_name {self.project}
            -mapper {mapper_class}
            -reducer {reducer_class}
            -key {mapper_key}
            -value {mapper_value}
            -input {input_table_name}
            -partin {input_table_partition}
            -output {output_table_name}
            -partout {output_table_partition}
            -resource {mr_jar_name} {resource_table_str}
            {user_defined_param_str}
            -splitSize {split_size}
            -reduceCnt {reduce_cnt}
            -reduceMem {reduce_mem}
        '''.replace('\n', '\\\n').replace('$', '\\$')

        logger.info(cmd)
        cmd_exit_code = os.system(cmd)
        logger.info('cmd_exit_code => ' + str(cmd_exit_code))
        if cmd_exit_code != 0:
            import sys
            sys.exit()
        pass

MaxComputeConnector = MaxcomputeConnector
