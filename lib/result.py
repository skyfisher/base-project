#!/usr/bin/env python
# created by fanzeng 2013-05-31
# updated by fanzeng 2017-01-14

import json
from log import Log

class Result:
    def __init__(self, status_code):
        self.items = {}
        self.items['status_code'] = status_code
        if status_code == 0:
            self.items['status_info'] = 'success'
        else:
            self.items['status_info'] = 'fail'

    def setInfo(self, info):
        self.items['status_info'] = info
        return self

    def setItem(self, key, value):
        if key != 'status_code':
            self.items[key] = value

    def getCode(self):
        return self.items['status_code']

    def getInfo(self):
        return self.items['status_info']

    def getItem(self, key):
        if key in self.items:
            return self.items[key]

    def toJson(self):
        try:
            return json.dumps(self.items, sort_keys = True)
        except Exception as e:
            Log.wError('error when converting result to json: %s' % e)
            raise Exception(e)

def loadResult(json_res):
    try:
        items = json.loads(json_res)
        result = Result(0)
        result.items = items
        return result
    except Exception as e:
        Log.wError('error when loading json result: %s' % e)
        raise Exception(e)
