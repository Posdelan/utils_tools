#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import fnmatch
"""
@author:yangzhou
@contact:@yangzhou@antiy.cn
@create:2016-05-09 14:03
"""

__author__ = 'Yangzhou'
__version__ = '0.1'


def get_message_count(prefix=None, suffix=None):
    """
    get messages count by http api
    get queue dict by http api, you can use prefix and suffix as filter
    queue_name will be the dict key, and the value is message count
    @rtype: list
    @return: error code and queuename: message dict
    @note: error code definition:
           0 - get queue dict success
           1 - get queue dict failed
    """
    queue_dict = {}
    messages_count = None
    api_url = 'http://%s:15672/api/queues' % '192.168.12.39'
    try:
        r = requests.get(api_url, auth=('guest', 'guest'))
        result_json = r.json()
        for line in result_json:
            queue_name = str(line['name']).strip()
            if (not prefix) and (not suffix):
                queue_dict[queue_name] = int(line['messages']) if 'messages' in line else 0
            elif not suffix:
                pattern = '%s*' % prefix
                if fnmatch.fnmatch(queue_name, pattern):
                    queue_dict[queue_name] = int(line['messages']) if 'messages' in line else 0
                else:
                    continue
            elif not prefix:
                pattern = '*%s' % suffix
                if fnmatch.fnmatch(queue_name, pattern):
                    queue_dict[queue_name] = int(line['messages']) if 'messages' in line else 0
                else:
                    continue
            else:
                prefix_pattern = '%s*' % prefix
                suffix_pattern = '*%s' % suffix
                if fnmatch.fnmatch(queue_name, prefix_pattern) and fnmatch.fnmatch(queue_name, suffix_pattern):
                    queue_dict[queue_name] = int(line['messages']) if 'messages' in line else 0
                else:
                    continue
        return 0, queue_dict
    except:
        return 1, queue_dict


def main():
    """
    main process

    """
    aa, bb = get_message_count(prefix='sample_info_fixer')
    print aa, bb
    print bb.get('sample_info_fixer_for_search'), '\n', bb.get('sample_info_fixer_out_for_search')
    if bb.get('sample_info_fixer_for_search') == 0 and bb.get('sample_info_fixer_out_for_search') == 0:
        print 'ok'
    else:
        print 'not ok'

if __name__ == '__main__':
    main()