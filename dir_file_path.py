#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os


"""
@author:posdelan
@create:2017-11-07 11:29
"""

__author__ = 'posdelan'
__version__ = '0.1'


def main(test_dir):
    """
    main process
    """
    onlyfiles = [os.path.join(test_dir, f) for f in os.listdir(test_dir) if os.path.isfile(os.path.join(test_dir, f))]
    print onlyfiles

if __name__ == '__main__':
    main(test_dir='./')
