#!/usr/bin/env python
# -*- coding: utf-8 -*-
import MySQLdb
from MySQLdb.cursors import DictCursor



class Mysqlclient:
    def __init__(self, dbconfig):
        try:
            self.conn = MySQLdb.connect(host=dbconfig['host'],
                                        port=dbconfig['port'],
                                        user=dbconfig['user'],
                                        passwd=dbconfig['passwd'],
                                        db=dbconfig['db'])
        except MySQLdb.Error, err:
            print err

    def create_cursor(self):
        """
        :return:
        """
        self.cursor = self.conn.cursor(DictCursor)

    def close_cursor(self):
        """
        :return:
        """
        self.cursor.close()

    def query(self, query_sql, query_dict):
        """
        use sql string to query data
        :param query_sql:
        """
        # excute sql
        sql_result = None
        try:
            self.cursor.execute(query_sql, query_dict)
            sql_result = self.cursor.fetchall()
            return True, sql_result
        except None, err:
            print err
            return False, sql_result

    def query_single(self, query_sql, query_dict):
        """
        :param query_sql:
        :param query_dict:
        :return:
        """
        query_result = self.query(query_sql, query_dict)
        return query_result

    def update(self, update_sql, update_dict):
        """
        update db
        """
        try:
            self.cursor.execute(update_sql, update_dict)
            return True
        except Exception, err:
            print err
            return False

    def commit(self):
        """
        commit update
        """
        try:
            self.conn.commit()
            return True
        except Exception, err:
            print err
            return False

    def close(self):
        """
        close connection
        """
        self.conn.close()
