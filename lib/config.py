#!/usr/bin/env python
# -*- coding:utf-8 -*-

# created by fanzeng 2013-05-31
# updated by liquan.nie 2018-3-20

from log import Log

class Config:
    __items = {}
    @staticmethod
    def load(path):
        Config.__items = Config.getConf(path)

    @staticmethod
    def getConf(path):
        try:
            fp = None
            config = {}
            fp = open(path, 'r')
            for line in fp:
                if line.startswith('#'):
                    continue
                pair = line.split('=')
                if len(pair) < 2:
                    continue
                key = pair[0].strip()
                value = pair[1].strip()
                config[key] = value
            return config
        except Exception as e:
            Log.wError("error when getting config: %s" % e)
            raise Exception(e)
        finally:
            if fp:
                fp.close()

    @staticmethod
    def getItem(key):
        try:
            return Config.__items[key]
        except Exception as e:
            Log.wError("error when getting config item: %s" % e)
            raise Exception(e)

    @staticmethod
    def getSubConf(key):
        try:
            sub_conf_path = Config.__items[key]
            return Config.getConf(sub_conf_path)
        except Exception as e:
            Log.wError("error when getting sub config: %s" % e)
            raise Exception(e)

    @staticmethod
    def display():
        for key, value in Config.__items.items():
            print("%s = %s" % (key, value))

if __name__ == "__main__":
    pass
