#!/usr/bin/env python3
# -*- coding=utf-8 -*-
from abc import ABC

from bigdata_util.connector.base_query import IBaseQuery
from bigdata_util.util import partition_to_where

from bigdata_util.util.table_info import TableInfo
from bigdata_util.util.logger import get_logger
from pydash import _

logger = get_logger(__file__)


class HiveConnector(IBaseQuery):

    def __init__(self, *args, **kwargs):
        from impala.dbapi import connect
        self.hive_conn = connect(
            host=_.get(args[0], 'host'),
            port=_.get(args[0], 'port'),
            database=_.get(args[0], 'database'),
            auth_mechanism='PLAIN'
        )

    def create_table(self, schema_or_desc, table_name):
        # TODO
        pass

    def exist_table(self, table_name):
        # TODO
        pass

    def execute_sql(self, sql, sql_hints=None):
        return self.run_sql(sql, sql_hints=sql_hints)

    def run_sql_with_logview_return_plain_json(self, sql):
        logger.info('''
            executing... hive have no logview.
        ''')
        return self.run_sql_return_plain_json(sql)

    def run_sql_return_plain_json(self, sql):
        col_list, data_list = self.run_sql(sql)

        result = []
        for row in data_list:
            meta = {}
            for idx, col in enumerate(col_list):
                col_name = col[0].split('.')[-1]
                meta[col_name] = row[idx]
            result.append(meta)

        return result

    def run_sql(self, sql):
        logger.info(f'''
executing sql:
{sql}
''')

        cursor = self.hive_conn.cursor()
        cursor.set_arraysize(10)
        cursor.execute("set batch_size=10")

        cursor.execute(sql)
        data_list = cursor.fetchall()

        col_list = cursor.description
        cursor.close()

        return col_list, data_list

    def get_table_data(self, table_name, partition=None, project=None):
        """
        hive的请求不进行本地cache
        :param table_name:
        :param partition:
        :param project:
        :param sep:
        :param ignore_cache:
        :return:
        """
        if isinstance(table_name, TableInfo):
            table_info = table_name
            table_name = table_info.table_name
            partition = table_info.partition
            project = table_info.project
        partition = self.__adjust_partition(partition)

        project_prefix = ''
        if project is not None and len(project) > 0:
            project_prefix = project + '.'

        sql = f'''
            select * from {project_prefix}{table_name}
            where {partition_to_where(partition)}
        '''

        return self.run_sql_return_plain_json(sql)

    @staticmethod
    def __adjust_partition(partition):
        if type(partition) is not str:
            return partition

        return partition.replace('/', ',')
