#!/usr/bin/env python
# -*- coding:utf-8 -*-

# created by liquan.nie : 2017-4-12
# update by liquan.nie : 2018-3-20
import time
import socket
import struct
import math

class Util():
    def __init__(self):
        pass

    @staticmethod
    def sigmoid(x):
        return 1 / (1 + math.exp(-x))

    @staticmethod
    def getDateKey(ts=0):
        if not ts:
            ts = time.time()
        return time.strftime('%Y%m%d',time.localtime(float(ts)))

    @staticmethod
    def from_unixtime(ts=0):
        if not ts:
            ts = time.time()
        return time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(float(ts)))

    @staticmethod
    def unix_timestamp(t_str=None):
        if not t_str:
            return int(time.time())
        return int(time.mktime(time.strptime(t_str, '%Y-%m-%d %H:%M:%S')))

    @staticmethod
    def dateSub(date_key, n):
        return time.strftime('%Y%m%d',\
            time.localtime(time.mktime(time.strptime(date_key, '%Y%m%d'))-n*3600*24))

    @staticmethod
    def agentid2ip(agentid):
        return socket.inet_ntoa(struct.pack("!I",socket.htonl(long(agentid))))

    @staticmethod
    def ip2agentid(ip):
        return struct.unpack("I",socket.inet_aton(str(ip)))[0]

    @staticmethod
    def getStartTimeOfDay(time_str):
        subStr = time_str.split(" ")
        time_str ="%s 00:00:00" % subStr[0]
        time_stamp = int(time.mktime(time.strptime("%s 00:00:00"%subStr[0], "%Y-%m-%d %H:%M:%S")))
        return time_stamp

if __name__ == "__main__":
    print(Util.from_unixtime(Util.getStartTimeOfDay("2017-04-12 12:12:00")))

    print()