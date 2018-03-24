#!/usr/bin/env python
# -*- coding:utf-8 -*-

# created by fanzeng 2013-05-31
# updated by fanzeng 2017-01-02
# updated by liquan.nie 2018-03-20

import time
import os

class Log():
    __built = False
    __dir = ''
    __errorpath = ''
    __eventpath = ''
    __scr_print = False

    def __init__(self):
        pass

    @staticmethod
    def build(dir, pre):
        if not Log.__built:
            if not os.path.isdir(dir):
                os.mkdir(dir)
                print("Created log directory: %s" % dir)
            Log.__dir = dir
            Log.__built = True
            Log.__errorpath = "%s/%s_error.log" % (dir, pre)
            Log.__eventpath = "%s/%s_event.log" % (dir, pre)
        else:
            print("Log rebuilding not allowed")

    @staticmethod
    def printInfo():
        if Log.__built:
            print("Log built in %s" % Log.__dir)
            print("Error log: %s" % Log.__errorpath)
            print("Event Log: %s" % Log.__eventpath)
        else:
            print("Log has not been built yet")

    @staticmethod
    def openScrPrint():
        Log.__scr_print = True

    @staticmethod
    def closeScrPrint():
        Log.__scr_print = False

    @staticmethod
    def __write(msg, path, mode):
        if Log.__scr_print or not Log.__built:
            print(msg)
        if Log.__built:
            try:
                fp = open(path, mode)
                if fp:
                    fp.write(msg)
                else:
                    raise Exception()
            except:
                print("*** Fital error: can not write log ***")
            finally:
                if fp:
                    fp.close()

    @staticmethod
    def wError(msg, location = ''):
        tm_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        if location:
            loc_str = "error occurred at %s" % location
        else:
            loc_str = ''

        content = '[' + tm_str + ']' + os.linesep
        content += msg + os.linesep
        if loc_str:
            content += loc_str + os.linesep

        Log.__write(content, Log.__errorpath, 'a')

    @staticmethod
    def wEvent(msg):
        tm_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        content = '[' + tm_str + ']' + os.linesep
        content += msg + os.linesep
        Log.__write(content, Log.__eventpath, 'a')

if __name__ == "__main__":
    strLogDir = "../log"
    strModule = "base_porject"
    objLog = Log.build(strLogDir, strModule)
    Log.openScrPrint()
    Log.printInfo()
    Log.wEvent("write event info")


