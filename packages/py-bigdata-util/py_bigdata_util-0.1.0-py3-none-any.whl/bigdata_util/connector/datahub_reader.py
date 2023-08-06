#!/usr/bin/env python3
# -*- coding=utf-8 -*-

from datahub.exceptions import ResourceNotFoundException, InvalidParameterException, DatahubException, \
    InvalidOperationException, OffsetResetException
from datahub.models import CursorType, OffsetWithSession
import time
import sys
MAX_INT = sys.maxsize


class DatahubReader:
    def __init__(self, project_name, topic_name, dh, shard_id='0'):
        self.dh = dh
        self.shard_id = shard_id
        self.shards = [shard_id]
        self.project_name = project_name
        self.topic_name = topic_name
        self.fetch_num = 100

    def __read(self, limit, wait_second):
        project_name = self.project_name
        topic_name = self.topic_name
        shard_id = self.shard_id
        dh = self.dh
        start_time = int(time.time())
        cur_time = start_time

        dh.wait_shards_ready(project_name, topic_name)
        print("shards all ready!!!")
        print("=======================================\n\n")

        cursor = dh.get_cursor(project_name, topic_name, shard_id, CursorType.SYSTEM_TIME, start_time).cursor
        schema = dh.get_topic(project_name, topic_name).record_schema

        records = []

        if limit > self.fetch_num:
            limit = self.fetch_num

        record_count = 0
        while len(records) < limit and (cur_time - start_time) < wait_second:
            cur_time = int(time.time())
            try:
                record_result = dh.get_tuple_records(project_name, topic_name, shard_id, schema, cursor, limit)
                if record_result.record_count <= 0:
                    time.sleep(1)
                    continue

                for record in record_result.records:
                    record_count += 1
                    records.append(record)

                cursor = record_result.next_cursor
            except DatahubException as e:
                print(e)
                break
        return records

    def read_limit(self, limit):
        return self.__read(limit, 600)

    def read_wait(self, wait_second):
        return self.__read(MAX_INT, wait_second)