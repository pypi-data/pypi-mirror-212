#!/usr/bin/env python3
# -*- coding=utf-8 -*-


class TableInfoException(Exception):
    pass


class TableInfo:
    def __init__(self, table_name, partition=None, project=None, resource_name=None):
        if not isinstance(table_name, str):
            raise TableInfoException('table_name should be a string.')

        self.table_name = table_name
        self.project = project
        if self.project is None and len(self.table_name.split('.')) > 1:
            self.table_name = self.table_name.split('.')[1]
            self.project = self.table_name.split('.')[0]

        self.partition = partition
        if self.partition:
            self.partition = self.partition.replace('/', ',')
            list_partition_kv = self.partition.split(',')
            list_partition_kv = list(map(
                lambda x: x.split('=')[0] + '=' + '"' + x.split('=')[1].replace('"', '\\"') + '"',
                list_partition_kv
            ))
            self.partition = ','.join(list_partition_kv)

        self.resource_name = resource_name
        if not self.resource_name:
            self.resource_name = self.gen_resource_name()
        pass

    def has_partition(self):
        return self.partition is not None and self.partition != ''

    def get_table_name_with_project(self):
        if self.project is not None:
            return self.project + '.' + self.table_name
        else:
            return self.table_name

    def get_resource_name(self):
        return self.resource_name

    def gen_resource_name(self):
        """
        如果把这张表作为resource，名称应该为: prefix_project_table_partition
        :return:
        """
        result = 'rsc_' + self.get_table_name_with_project().replace('.', '_')
        if self.partition:
            partition_suffix = '_' + self.partition.replace('"', '')\
                .replace("'", '').replace('/', '_').replace(',', '_').replace('=', '_')
            result += partition_suffix
        return result

    def get_table_name(self):
        return self.table_name

    def get_partition(self):
        return self.partition

    def get_project(self):
        return self.project

    def __str__(self):
        result = self.table_name
        if self.project is not None:
            result = self.project + '.' + result
        if self.partition is not None:
            result = result + '/' + self.partition
        return result
