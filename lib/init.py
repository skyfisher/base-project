#!/usr/bin/env python
# -*- coding:utf-8 -*-

# created by fanzeng 2014-01-15
# updated by liquannie 2018-03-20

import sys
from log import Log
from config import Config
from mysql_conn import MySQLConn
from cache import *

def init(conf_path, module, mode = ''):
    try:
        Config.load(conf_path)

        srv_log = Config.getItem('log_dir')
        Log.build(srv_log, module)

        if mode.lower() == 'debug':
            Log.openScrPrint()

        MySQLConn.InitConnPool(Config.getSubConf('db_conf'))
    except Exception as e:
        error_msg = "error when initializing: %s, module: %s" % (e, module)
        Log.wError(error_msg)
        raise Exception(e)
