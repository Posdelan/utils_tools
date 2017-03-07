#!/usr/bin/env python
# -*- coding: utf-8 -*-


import psycopg2
import psycopg2.extras


class PostgresClient:
    def __init__(self, host='localhost', port=5432, user='user', password='password', database='database'):
        """
        init function
        create db connection
        """
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.conn_string = "host=%s port=%s user=%s password=%s dbname=%s" % \
                           (self.host, self.port, self.user, self.password, self.database)
        self.conn = psycopg2.connect(self.conn_string)

    def create_cursor(self):
        """
        create cursor
        """
        self.cursor = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    def close_cursor(self):
        """
        close cursor
        """
        self.cursor.close()

    def query(self, query_sql, query_dict):
        """
        user sql string to query data
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
        query single data
        """
        self.create_cursor()
        query_result = self.query(query_sql, query_dict)
        self.close_cursor()
        return query_result

    def insert(self, tablename, data_dict):
        """
        insert single line data to table, do not forget to use commit() function
        """
        # form insert sql
        key_string, value_string = '', ''
        for key_item, value_item in data_dict.iteritems():
            key_string += '%s,' % key_item
            value_string += "%%(%s)s" % key_item + ','
        insert_sql = """INSERT INTO %s (%s) VALUES (%s);""" % (tablename, key_string[:-1], value_string[:-1])

        # excute insert sql
        try:
            self.cursor.execute(insert_sql, data_dict)
            return True
        except Exception, err:
            print "here"
            print err
            return False

    def insert_with_return_value(self, tablename, data_dict, return_field='id'):
        """
        insert single line data to table, do not forget to use commit() function
        this function will return a value
        """
        return_value = None
        # form insert sql
        key_string, value_string = '', ''
        for key_item, value_item in data_dict.iteritems():
            key_string += '%s,' % key_item
            value_string += "%%(%s)s" % key_item + ','
        insert_sql = """INSERT INTO %s (%s) VALUES (%s) RETURNING %s;""" % \
                     (tablename, key_string[:-1], value_string[:-1], return_field)

        # excute insert sql
        try:
            self.cursor.execute(insert_sql, data_dict)
            return_value = self.cursor.fetchone()[0]
            return True, return_value
        except Exception, err:
            return False, return_value

    def insert_single(self, tablename, data_dict):
        """
        insert single data
        """
        # form insert sql
        key_string, value_string = '', ''
        for key_item, value_item in data_dict.iteritems():
            key_string += '%s,' % key_item
            value_string += "%%(%s)s" % key_item + ','
        insert_sql = """INSERT INTO %s (%s) VALUES (%s);""" % (tablename, key_string[:-1], value_string[:-1])

        # excute insert sql
        try:
            self.create_cursor()
            self.cursor.execute(insert_sql, data_dict)
            self.close_cursor()
            self.conn.commit()
            return True
        except psycopg2.Error, err:
            try:
                self.conn.rollback()
                self.cursor.close()
            except:
                pass
            return False

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

    def update_single(self, tablename, data_dict, condition_string):
        """
        update single data
        """
        # form insert sql
        update_string = ''
        for key_item, value_item in data_dict.iteritems():
            update_string += '%s=%%(%s)s,' % (key_item, key_item)
        update_sql = """UPDATE %s SET %s WHERE %s;""" % (tablename, update_string.rstrip(','), condition_string)
        # excute insert sql
        try:
            self.create_cursor()
            self.cursor.execute(update_sql, data_dict)
            self.close_cursor()
            self.conn.commit()
            return True
        except None, err:
            try:
                self.conn.rollback()
                self.cursor.close()
            except:
                pass
            return False

    def delete(self, delete_sql, delete_dict):
        """
        update db
        """
        try:
            self.cursor.execute(delete_sql, delete_dict)
            return True
        except Exception, err:
            print err
            return False

    def delete_single(self, delete_sql, delete_dict):
        """
        insert single data
        """
        self.create_cursor()
        delete_result = self.update(delete_sql, delete_dict)
        self.close_cursor()
        if delete_result:
            return self.commit()
        else:
            return False

    def commit(self):
        """
        commit update
        """
        try:
            self.conn.commit()
            return True
        except Exception, err:
            return False

    def close(self):
        # type: () -> object
        """
        """
        self.conn.close()
