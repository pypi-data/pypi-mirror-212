#!/usr/bin/env python3
# -*- coding=utf-8 -*-
from bigdata_util.util.table_info import TableInfo
from bigdata_util.util.logger import get_logger
from pydash import _

logger = get_logger(__file__)


class PhoenixConnector:
    def __init__(self, *args, **kwargs):
        import pyphoenix
        if isinstance(args[0], dict):
            proxy = _.get(args[0], 'proxy', None)
            if proxy is not None:
                if 'proxy' not in kwargs:
                    kwargs['proxy'] = proxy
                else:
                    logger.warning('[PhoenixConnector] proxy option in dict is ignored.')

            if 'zkQuorum' in args[0]:
                ip = args[0]['zkQuorum'].split(',')[0]
                self.phoenix_conn = pyphoenix.connect(
                    ip,
                    autocommit=True
                )
        pass

    def __del__(self):
        if self.phoenix_conn is not None:
            self.phoenix_conn.close()
        pass

    def desc_table(self, table_name):
        cursor = self.phoenix_conn.cursor()
        cursor.execute(f'select * from {table_name} limit 1')

        result = {
            'cols': []
        }
        for col in cursor.description:
            result['cols'].append({
                'name': col[0].lower(),
                'type': col[1],
            })

        return result

    def drop_table(self, table_name):
        from pyphoenix.errors import InternalError
        cursor = self.phoenix_conn.cursor()

        try:
            cursor.execute(f'drop table if exists {table_name}')
        except InternalError as e:
            if e.message == 'got an empty frame, but the statement is not done yet':
                pass
            else:
                raise e
            pass

    def create_table(self, ddl):
        from pyphoenix.errors import InternalError
        cursor = self.phoenix_conn.cursor()
        try:
            cursor.execute(ddl)
        except InternalError as e:
            if e.message == 'got an empty frame, but the statement is not done yet':
                pass
            else:
                raise e
            pass


    @staticmethod
    def mapping_col_type(sdf_type):
        sdf_type = sdf_type.lower()
        mapping = {
            'string': 'varchar',
            'bigint': 'bigint'
        }

        return mapping[sdf_type]

    def run(self):
        pass


if __name__ == '__main__':
    PhoenixConnector().run()


