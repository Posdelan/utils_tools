#!/usr/bin/env python
# -*- coding: utf-8 -*-


import socket
import hmac
from hashlib import sha1, md5

__author__ = 'Yangzhou'
__version__ = '0.1'


class AliyunClient(object):
    def __init__(self):
        """

        :param :
        :return:
        :rtype:
        """
        pass

    @staticmethod
    def get_signature(sign_string, secret_key):
        """

        :param :
        :return:
        :rtype:
        """
        try:
            mac = hmac.new(secret_key, sign_string, sha1)
            return mac.digest().encode('base64').rstrip()
        except:
            return None

    @staticmethod
    def get_content_md5(content):
        """

        :param :
        :return:
        :rtype:
        """
        try:
            return md5(content).hexdigest()
        except:
            return None



def main():
    """
    main process

    """


if __name__ == '__main__':
    main()
