#!/usr/bin/env python
# -*- coding: utf-8 -*-

from confluent_kafka import Producer
from confluent_kafka import Consumer
import sys
import os
import time
import pprint
"""
@author:yangzhou
@contact:@yangzhou@antiy.cn
@create:2017-01-03 11:21
"""

__author__ = 'yangzhou'
__version__ = '0.1'


class ConfluentKafkaProducerUtil(object):
    def __init__(self, host):
        self.host = host
        self.producer = Producer(self.host)

    def single_producer(self, topic_name, content):
        """
        put single message, flush
        :param topic_name:
        :param content:
        :return:
        """
        try:
            self.producer.produce(topic_name, content)
            self.producer.flush()
            return True
        except Exception as e:
            raise e.message

    def producer_message(self, topic_name, content):
        """
        producer single message, not flush
        :return:
        """
        try:
            self.producer.produce(topic_name, content)
        except Exception as e:
            raise e.message

    def message_flush(self):
        """
        message flush
        :return:
        """
        try:
            self.producer.flush()
        except Exception as e:
            raise e.message

    def close(self):
        """
        close producer connection
        :return:
        """
        self.producer.close()

    def batch_producer(self, topic_name, content_list):
        """
        batch produce message to kafka
        :param topic_name:
        :param content_list:
        :return:
        """
        try:
            for tmp_message in content_list:
                self.producer.produce(topic_name, tmp_message)
            self.producer.flush()
        except Exception as e:
            raise e.message


class ConfluentKafkaConsumerUtil(object):
    def __init__(self, host):
        self.host = host
        self.consumer = Consumer(self.host)

    def start_consuming(self, topic_name, processor=None, batch_count=1):
        """

        :param topic_name:
        :param processor:
        :param batch_count:
        :return:
        """
        if processor is None:
            raise 'processor is None'
        self.consumer.subscribe([topic_name])
        try:
            while True:
                msg = self.consumer.poll()
                if msg.value() == '':
                    continue
                if not msg.error():
                    processor(msg.value())
        except Exception as e:
            raise e.message
        finally:
            self.consumer.close()

    def close(self):
        """
        close consumer connection
        :return:
        """
        self.consumer.close()


def main():
    """
    main process
    """
    test_producer_host = {'bootstrap.servers': 'localhost'}
    test_consumer_host = {'bootstrap.servers': 'localhost', 'group.id': 'mygroup', 'default.topic.config': {'auto.offset.reset': 'smallest'}}

    def test_get(body_list):
        for i in body_list:
            print i
        print '---line-----'

    test_producer_obj = ConfluentKafkaProducerUtil(host=test_producer_host)
    print test_producer_obj.single_producer(topic_name='confluent_kafka_test', content='test message')

    #test_consuer_obj = ConfluentKafkaConsumerUtil(host=test_consumer_host)
    #test_consuer_obj.start_consuming(topic_name='confluent_kafka_test', processor=test_get)

if __name__ == '__main__':
    main()
