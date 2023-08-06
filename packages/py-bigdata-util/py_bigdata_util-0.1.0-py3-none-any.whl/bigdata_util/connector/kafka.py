#!/usr/bin/env python3
# -*- coding=utf-8 -*-


class KafkaConnector:
    bootstrap_servers = None

    def __init__(self, *args, **kwargs):
        if len(args) > 0 and isinstance(args[0], dict):
            self.bootstrap_servers = args[0]['bootstrapServers']
        pass

    def read_topic_last_msg_from_every_partition(self, topic='aaa', timeout_ms=30000, max_record_num=50):
        from kafka import KafkaConsumer, TopicPartition
        import json
        consumer = KafkaConsumer(
            # topic,
            bootstrap_servers=self.bootstrap_servers,
            auto_offset_reset='latest',
            value_deserializer=lambda m: json.loads(m.decode('utf-8')),
            group_id='albin_test'
        )
        partition_num = len(consumer.partitions_for_topic(topic))

        assigned_topic = []
        for partition_idx in range(partition_num):
            partition = TopicPartition(topic, partition_idx)
            assigned_topic.append(partition)

        consumer.assign(assigned_topic)
        return consumer.poll(timeout_ms=timeout_ms, max_records=max_record_num, update_offsets=True)


if __name__ == '__main__':
    KafkaConnector().run()

