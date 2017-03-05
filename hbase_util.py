#!/usr/bin/env python
# -*- coding: utf-8 -*-

import happybase


class HbaseClient(object):
    """
    a hbase client
    """
    def __init__(self, hbase_host):
        self.conn = happybase.Connection(host=hbase_host)

    def __enter__(self):
        return self

    def batch_put(self, table, column_family, data_dict):
        table = self.conn.table(table)
        batch = table.batch()
        try:
            for key, value_dict in data_dict.iteritems():
                for sub_key, sub_value in value_dict.iteritems():
                    column = '%s:%s' % (column_family, sub_key)
                    batch.put(key, {column: sub_value, })
            batch.send()
            return True
        except None, err:
            return False

    def close(self):
        self.conn.close()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


def main():
    """

    """


if __name__ == '__main__':
    main()
