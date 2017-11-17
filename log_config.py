#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging.config
import os
import sys
import time


# 创建目录

log_dir = os.path.join(os.path.join(os.path.dirname(__file__), os.path.pardir), "log")

# try:
#     log_dir = os.path.join(os.path.dirname(__file__), "log")
# except:
#     log_dir = os.path.dirname(os.path.abspath(sys.argv[0]))

if not os.path.isdir(log_dir):
    try:
        os.makedirs(log_dir)
    except Exception, e:
        log_file_err = "Create log file dir err:%s" % e.message
        print log_file_err
        sys.exit(0)   # 创建日志目录失败，直接退出

file_name = 'data_in_oss.log'
log_file_name = os.path.join(log_dir, file_name)


logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': "[%(asctime)s] [%(levelname)s] %(message)s",
            'datefmt': "%Y-%m-%d %H:%M:%S"
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            # 当达到10MB时分割日志
            'maxBytes': 1024 * 1024 * 1,
            # 最多保留10份文件
            'backupCount': 10,
            # If delay is true,
            # then file opening is deferred until the first call to emit().
            'delay': True,
            'filename': log_file_name,
            'formatter': 'verbose'
        }
    },
    'loggers': {
        '': {
            'handlers': ['file'],
            'level': 'ERROR',
        },
    }
})
