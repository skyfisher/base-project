#!/usr/bin/env python
# -*- coding:utf-8 -*-
# create by liquannie 2018-03-20

# description : 支持跨线程的cache

import multiprocessing
import threading
def updateCache():
    print("in update Cache")
    global timer
    timer = threading.Timer(2, updateCache)
    timer.start()
    Cache.dictData = {}

class Cache():
    dictData = {}

    def __init__(self):
        pass

    @staticmethod
    def init():
        Cache.dictData = multiprocessing.Manager().dict()

    @staticmethod
    def getItem(key):
        if key in Cache.dictData:
            return Cache.dictData[key]
    @staticmethod
    def setItem(key, value):
        Cache.dictData[key] = value

    @staticmethod
    def printInfo():
        print(Cache.dictData)

if __name__ == "__main__":
        timer = threading.Timer(2, updateCache)
        timer.start()
        while(True):
            print()


