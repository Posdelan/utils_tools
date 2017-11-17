#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@author:posdelan
@create:2017-09-08 14:57
"""

__author__ = 'yangzhou'
__version__ = '0.1'


def check_string(tmp_string):
    """
    检查一个对象是不是类似字符串的最简单，最快速方法
    :return:
    """
    try: tmp_string + ''
    except TypeError: pass
    else: raise TypeError


def main():
    """
    main process
    """
    # 检查

if __name__ == '__main__':
    main()
