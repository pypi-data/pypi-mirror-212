#!/usr/bin/env python
# -*- coding=utf-8 -*-
# @Author  : magong
# @Time    : 2022/5/31

import os
import logging

import pandas as pd
from pydash import py_
from bigdata_util.connector.base_query import IBaseQuery
from bigdata_util.util import get_logger, set_proxy_global, reset_proxy_global

logger = get_logger(__name__)


class HiveKerberos(IBaseQuery):
    __instance = None

    @classmethod
    def instance(cls, *args, **kwargs):
        if cls.__instance:
            return cls.__instance
        else:
            try:
                from impala.dbapi import connect
                from krbcontext import krbcontext
                set_proxy_global(kwargs['proxy'])
                with krbcontext(using_keytab=True, principal=py_.get(args[0], 'principal'), keytab_file=py_.get(args[0], 'keytab_file_path')):
                    logger.warning('Make sure `krb5.conf` is placed in `/etc` directory and host is added in `/etc/hosts`. ')
                    conn = connect(host=py_.get(args[0], 'host'),
                                   port=py_.get(args[0], 'port'),
                                   auth_mechanism=py_.get(args[0], 'auth_mechanism'),
                                   kerberos_service_name=py_.get(args[0], 'kerberos_service_name'),
                                   database=py_.get(args[0], 'database'))
                    return cls(conn)
            except Exception as e:
                raise e

    def __init__(self, conn):
        self.conn = conn

    def create_table(self, schema_or_desc, table_name):
        # TODO
        pass

    def exist_table(self, table_name):
        # TODO
        pass

    def execute(self, sql):
        """执行."""
        try:
            cur = self.conn.cursor()
            cur.execute(sql)
        except Exception as err:
            print(err)
            raise err

    def query(self, sql):
        """查询."""
        cur = self.conn.cursor()
        res = None
        try:
            cur.execute(sql)
            res = cur.fetchall()
        except Exception as err:
            print("查询失败, %s" % err)
            raise err
        finally:
            return res, cur.description
    
    def execute_with_result(self, sql):
        logger.info('''
            executing sql: >>> 
            {sql} <<<
            '''.format(sql=sql))
        
        cur = self.conn.cursor()
        cur.execute(sql)
        res = cur.fetchall()
        # cur.close()

        return cur, res

    def query_to_df(self, sql):
        """查询输出DataFrame."""
        with self.conn.cursor() as cursor:
            logger.info('''
                executing sql: >>> {sql} <<<
                '''.format(sql=sql))
            
            cursor.execute(sql)
            columns = [col[0] for col in cursor.description]
            records = [dict(zip(columns, row)) for row in cursor.fetchall()]
            results = pd.DataFrame(records)
            results.columns = columns
            return results
    
    def close(self):
        self.conn.close()
        
    def execute_sql(self, sql, sql_hints=None):
        if sql.endswith(';'):
            sql = sql[:-1]
        logger.info('''
        executing sql: >>> {sql} <<<
        '''.format(sql=sql))
        return self.execute(sql)
    
    def run_sql_return_plain_json(self, sql):
        result = []

        cur, fetched_list = self.execute_with_result(sql)
        if cur.description is None or len(cur.description) < 1:
            return result

        columns = [col[0] for col in cur.description]
        for row in fetched_list:
            meta = {}
            for col, val in zip(columns, row):
                meta[col] = val
            result.append(meta)

        return result
    
    def run_sql_with_logview_return_plain_json(self, sql):
        pass 
    
    def check_table_exists(self, table_name):
        '''检查表是否存在.'''
        # TODO: 
        print(table_name)
        query_res = self.query('''SELECT COUNT(*) FROM information_schema.tables WHERE table_name = '{0}' '''.format(table_name.replace('\'', '\'\'')))
        if query_res[0] == 1:
            print(true) 
        # return len(self.query('''SHOW TABLES LIKE '{table_name}' '''.format(table_name=table_name))) == 1
    
    def truncate_table_if_exists(self, table_name, force_trunc=False):
        '''如果表存在,清空表数据.如果不是algtmp开头的表,需要增加强制清空参数.'''
        if not table_name.startswith('algtmp_') and not force_trunc:
            logger.info('table {table_name} is not algtmp type, truncate it anyway please use force_trunc argument.'.format(table_name=table_name))
        else:
            if self.check_table_exists(table_name):
                self.query('TRUNCATE TABLE {table_name}'.format(table_name=table_name))
            

if __name__ == '__main__':
    pass
