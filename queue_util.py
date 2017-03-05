#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pika
import pika.credentials


class RabbitmqClient(object):
    def __init__(self, host, port=5672, username='guest', password='guest', prefetch_count=1):
        """
        initial with queue host, make a connection
        @rtype:
        @return:
        @note:

        """
        self.queue_host = host
        self.queue_port = port
        self.credentials = pika.credentials.PlainCredentials(username=username, password=password)
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.queue_host,
                                                                            port=self.queue_port,
                                                                            credentials=self.credentials))
        self.channel = self.connection.channel()
        self.channel.basic_qos(prefetch_count=prefetch_count)
        self.prefetch_count = prefetch_count

    def recreate_channel(self):
        """

        :param :
        :return:
        :rtype:
        """
        self.channel = self.connection.channel()
        self.channel.basic_qos(prefetch_count=self.prefetch_count)

    def check_exchange_exists(self, exchange_name):
        """
        check if exchange exists
        :param :
        :return:
        :rtype:
        """
        try:
            self.channel.exchange_declare(exchange=exchange_name, passive=True)
            return True
        except:
            return False

    def check_queue_exists(self, queue_name):
        """
        check if the queue exists
        :param :
        :return:
        :rtype:
        """
        try:
            self.channel.queue_declare(queue=queue_name, passive=True)
            return True
        except:
            return False

    def declare_exchange(self, exchange_name, exchange_type='fanout', durable=True, auto_delete=False):
        """
        declare an exchange
        :param :
        :return:
        :rtype:
        """
        try:
            self.channel.exchange_declare(exchange=exchange_name,
                                          exchange_type=exchange_type,
                                          durable=durable,
                                          auto_delete=auto_delete)
            return True
        except:
            return False

    def declare_queue(self, queue_name, durable=True, args=None):
        """

        :param :
        :return:
        :rtype:
        """
        try:
            self.channel.queue_declare(queue=queue_name, durable=durable, arguments=args)
            return True
        except:
            return False

    def bind_queue(self, exchange_name, queue_name, routing_key=''):
        """
        declare and bind queues

        """
        try:
            self.channel.queue_bind(exchange=exchange_name, queue=queue_name, routing_key=routing_key)
            return True
        except:
            return False

    def delete_queue(self, queue_name):
        """
        delete queue by queue name
        :param :
        :return:
        :rtype:
        """
        try:
            self.channel.queue_delete(queue=queue_name)
            return True
        except:
            return False

    def write_exchange(self, exchange_name, content, routing_key=''):
        """
        write to exchange
        @rtype:
        @return:
        @note:

        """
        try:
            self.channel.basic_publish(exchange=exchange_name, routing_key=routing_key, body=content)
            return True
        except Exception, err:
            print err
            return False

    def start_consuming(self, queue_name, processor, no_ack=False):
        """
        start to get data from queues
        """
        self.channel.basic_consume(processor, queue=queue_name, no_ack=no_ack)
        self.channel.start_consuming()

    def close(self):
        """
        close connection
        :param :
        :return:
        :rtype:
        """
        self.connection.close()

if __name__ == '__main__':
    a = RabbitmqClient(host='localhost', port=5672,)
    print a.check_exchange_exists(exchange_name='exchange_name')
    print a.check_queue_exists(queue_name='queue_name')
    # declare a test exchange
    print a.declare_exchange(exchange_name='test')
    a.close()
