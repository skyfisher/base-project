#!/usr/bin/env python
# -*- coding:utf-8 -*-

# create by liquan.nie : 2017-4-11
# update by liquan.nie : 2018-3-16

import MySQLdb
import json
from log import Log
from result import Result

class MySQLConn(object):
    conn_pool = {}

    def __init__(self, host, port, user, passwd, db, charset = 'utf8'):
        try:
            self.host = host
            self.port = port
            self.user  = user
            self.passwd = passwd
            self.db = db
            self.charset = charset
            self.connect()
        except Exception as e:
            error_msg = "error when creating MySQLConn object: %s" % e
            Log.wError(error_msg)

    def __del__(self):
        self.close()

    def reconnect(self):
        try:
            self.conn.ping()
        except Exception as e:
            event_msg = "MySQL connection gone, try to reconnect, host: %s, port: %s, user: %s, db: %s" % \
                    (self.host, self.port, self.user, self.db)
            Log.wEvent(event_msg)
            self.connect()

    def connect(self):
        try:
            self.conn = MySQLdb.connect(
                    host = self.host,
                    port = self.port,
                    user = self.user,
                    passwd = self.passwd,
                    db = self.db,
                    charset = self.charset
                    )
            self.cursor = self.conn.cursor()
        except Exception as e:
            error_msg ="error when connecting MySQL: %s" % e
            Log.wError(error_msg)

    def close(self):
        try:
            self.cursor.close()
            self.conn.close()
        except Exception as e:
            error_msg = "error when closing MySQL connection: %s" % e
            Log.wError(error_msg)

    def query(self, sql_cmd):
        try:
            self.reconnect()
            self.cursor.execute(sql_cmd)
            data = self.cursor.fetchall()
            self.conn.commit()
            result = Result(0)
            result.setItem('data', data)
            return result
        except Exception as e:
            error_msg = "error when quering MySQL: %s" % e
            Log.wError(error_msg)
            return Result(1).setInfo(error_msg)

    def execute(self, sql_cmd, value):
        try:
            self.reconnect()
            self.cursor.execute(sql_cmd, value)
            self.conn.commit()
            return Result(0)
        except Exception as e:
            error_msg = "error when executing MySQL command(single value): %s" % e
            Log.wError(error_msg)
            return Result(1).setInfo(error_msg)

    def executeMany(self, sql_cmd, values):
        try:
            self.reconnect()
            self.cursor.executemany(sql_cmd, values)
            self.conn.commit()
            return Result(0)
        except Exception as e:
            error_msg = "error when executing MySQL command(many values): %s" % e
            Log.wError(error_msg)
            return Result(1).setInfo(error_msg)

    @staticmethod
    def getConn(key):
        try:
            return MySQLConn.conn_pool[key]
        except Exception as e:
            error_msg = "error when getting connecion from MySQLConn: %s" % e
            Log.wError(error_msg)

    @staticmethod
    def InitConnPool(conf):
        try:
            for key, value in conf.items():
                inst_conf = json.loads(value)
                host = inst_conf['host']
                port = inst_conf['port']
                user = inst_conf['user']
                passwd = inst_conf['passwd']
                db = inst_conf['db']
                if 'charset' in inst_conf:
                    charset = inst_conf['charset']
                else:
                    charset = 'utf8'

                MySQLConn.conn_pool[key] = MySQLConn(host, port, user, passwd, db, charset)
        except Exception as e:
            error_msg = "error when initializing MySQL connection pool: %s" % str(e)
            Log.wError(error_msg)

    def getColumns(self, table_name):
        try:
            self.reconnect()
            sql_cmd = "select * from %s limit 1" % table_name
            self.cursor.execute(sql_cmd)
            self.conn.commit()
            column_names = [ i[0] for i in self.cursor.description]
            return column_names
        except Exception as e:
            strMsg = "error when getting mysql db columns: %s" % str(e)
            Log.wError(strMsg)

if __name__ == "__main__":
    db