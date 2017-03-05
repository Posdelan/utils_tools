#!/usr/bin/env python
# -*- coding: utf-8 -*-

# import log_config
from mns.account import Account
import logging
from mns.queue import *


class MnsClient(object):
    def __init__(self, access_key, secret_key, endpoint, wait_seconds=1):
        """

        :param :
        :return:
        :rtype:
        """
        self.access_key = access_key
        self.secret_key = secret_key
        self.endpoint = endpoint
        self.wait_seconds = wait_seconds
        self.account = Account(access_id=self.access_key,
                               access_key=self.secret_key,
                               host=self.endpoint)
        self.account.set_log_level(log_level=logging.CRITICAL)
        self.account.close_log()

    def send_data(self, queue_name, messsages):
        """

        :param :
        :return:
        :rtype:
        """
        print queue_name, messsages, type(messsages)
        queue = self.account.get_queue(queue_name=queue_name)
        try:
            queue.batch_send_message(messages=messsages)
            return True
        except:
            return False

    def publish_data(self, queue_name, messages):
        """

        :param queue_name:
        :param messages:
        :return:
        """
        queue = self.account.get_queue(queue_name=queue_name)
        queue.set_encoding(encoding=False)
        try:
            msg = Message(messages)
            queue.send_message(msg)
            return True
        except:
            return False

    def delete_queue_message(self, queue_name, handle_name):
        queue = self.account.get_queue(queue_name=queue_name)
        try:
            queue.delete_message(handle_name)
        except:
            print 'delete message failed,'

    def get_data(self, queue_name, batch_size=1):
        """

        :param :
        :return:
        :rtype:
        """

        queue = self.account.get_queue(queue_name=queue_name)
        queue.set_encoding(encoding=False)

        try:
            return queue.batch_receive_message(batch_size=batch_size, wait_seconds=self.wait_seconds)
        except:
            return None

    def delete_data(self, queue_name, handle_list):
        """

        :param :
        :return:
        :rtype:
        """
        queue = self.account.get_queue(queue_name=queue_name)
        try:
            queue.batch_delete_message(receipt_handle_list=handle_list)
            return True
        except None:
            return False

    def start_consuming(self, queue_name, batch_size=1, processor=None):
        """

        :param :
        :return:
        :rtype:
        """
        try:
            while True:
                data_list = self.get_data(queue_name=queue_name, batch_size=batch_size)
                if not data_list:
                    continue
                elif processor is not None:
                    body_list = [i.message_body for i in data_list]
                    handle_list = [i.receipt_handle for i in data_list]
                    self.delete_data(queue_name=queue_name, handle_list=handle_list)
                    processor(body_list)
                else:
                    continue
        except KeyboardInterrupt:
            print "interrupted"

    def get_queueinfo(self, queue_name):
        """
        获取队列info,
        :return:
        :rtype: 返回instance类型
        """
        queue = self.account.get_queue(queue_name=queue_name)
        try:
            queue_attr = queue.get_attributes()
            return queue_attr.__dict__
        except None:
            return False


def test_get():
    """

    :param :
    :return:
    :rtype:
    """
    # url = "http://1546059688730522.mns.cn-hangzhou.aliyuncs.com"
    # access_key = ''
    # secret_key = ''
    url = "http://1159266580440312.mns.cn-shenzhen.aliyuncs.com"
    access_key = 'Nu6pjZErb6xSyWUM'
    secret_key = 'y9rAtIXtzoQVoGpPGLhQsZcCwabEQm'

    a = MnsClient(access_key=access_key,
                  secret_key=secret_key,
                  endpoint=url,
                  wait_seconds=1)
    test_queue = 'test-lactoni'

    def processor(body_list):
        """

        :param :
        :return:
        :rtype:
        """
        for i in body_list:
            print i
        print "========"

    a.start_consuming(queue_name=test_queue, processor=processor, batch_size=1)

def test_send():
    """

    :param :
    :return:
    :rtype:
    """
    # url = "http://1523163571078731.mns.cn-hangzhou.aliyuncs.com"
    # access_key = 'yHGrjYMGbKKt31Kj'
    # secret_key = 'DaiWKTrru26IWfGnnrv8aeU0B4OtZW'
    # a = MnsClient(access_key=access_key,
    #               secret_key=secret_key,
    #               endpoint=url,
    #               wait_seconds=1)
    # test_queue = 'test-knktc'
    # import sys
    # filepath = sys.argv[1]

    url = "https://1159266580440312.mns.cn-shenzhen.aliyuncs.com"
    access_key = 'Nu6pjZErb6xSyWUM'
    secret_key = 'y9rAtIXtzoQVoGpPGLhQsZcCwabEQm'
    a = MnsClient(access_key=access_key,
                  secret_key=secret_key,
                  endpoint=url)
    test_queue = 'test-lactoni'
    import json
    import pprint
    test_list = []
    test_data = {'test': '123'}
    pprint.pprint(json.dumps(test_data))
    test_list.append(json.dumps(test_data))
    pprint.pprint(a.publish_data(queue_name=test_queue, messages=json.dumps(test_data)))


def delete_test():
    url = "https://1159266580440312.mns.cn-shenzhen.aliyuncs.com"
    access_key = 'Nu6pjZErb6xSyWUM'
    secret_key = 'y9rAtIXtzoQVoGpPGLhQsZcCwabEQm'
    a = MnsClient(access_key=access_key,
                  secret_key=secret_key,
                  endpoint=url)
    test_queue = 'test-lactoni'
    handle_list = '1-ODU4OTkzNDYwMC0xNDY3ODgxNzQyLTItOA=='
    a.delete_queue_message(queue_name=test_queue, handle_name=handle_list)


def test_getqueueinfo():
    url = "https://1159266580440312.mns.cn-shenzhen.aliyuncs.com"
    access_key = 'Nu6pjZErb6xSyWUM'
    secret_key = 'y9rAtIXtzoQVoGpPGLhQsZcCwabEQm'
    account = Account(access_id=access_key,
                      access_key=secret_key,
                      host=url)
    test_queue_name = 'test-lactoni'
    test_queue = account.get_queue(queue_name=test_queue_name)
    aa = test_queue.get_attributes()
    print type(aa), dir(aa) , aa.active_messages
    import pprint
    pprint.pprint(aa)


def getinfo():
    url = "http://1546059688730522.mns.cn-hangzhou.aliyuncs.com"
    access_key = 'iaPhgo9HU7tYI9s9'
    secret_key = 'mH10oLcmoGqfOsYwsRLzR2cRQQ1wrV'
    a = MnsClient(access_key=access_key,
                  secret_key=secret_key,
                  endpoint=url)
    test_queue = 'avlsec-log'
    aa = a.get_queueinfo(queue_name=test_queue)
    print aa.get('active_messages')
    import pprint
    pprint.pprint(aa)
    # for key, values in aa.items():
    #     print key, values


def main():
    """
    main process

    """
    # test_get()
    # test_send()
    # delete_test()
    # test_getqueueinfo()
    getinfo()

if __name__ == '__main__':
    main()
