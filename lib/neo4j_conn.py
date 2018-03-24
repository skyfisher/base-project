#!/usr/bin/env python
#-*- encoding=utf8

# create by liquan.nie : 2017-11-02
# update by liquan.nie ：2018-03-24

from py2neo import Node, Relationship, Graph
import json
from log import Log
import sys
from config import Config
import subprocess
import traceback
from result import Result

class Neo4jHandler():
    def __init__(self, host, port,username, passwd):
        try:
            self.username = username
            self.password = passwd
            self.host = host
            self.port = port
            self.connect()
        except Exception as e:
            Log.wEvent("init neo4j error %s" % str(e))

    def connect(self):
        try:
            self.graph = Graph(host=self.host, port=self.port, user=self.username, password=self.password)
        except Exception as e:
            Log.wEvent("connect neo4j error %s" % str(e))
            raise Exception(e)

    def cypherQuery(self,query, param=None):
        try:
            result = Result(0)
            result.setItem("data",self.graph.run(query,parameters=param).data())

            return result
        except Exception as e:
            Log.wEvent("cypher query %s error %s" % (query, str(e)))
            result = Result(-1)
            result.setItem("status_info", str(e))
            return result

    def truncateTable(self):
        self.graph.delete_all()

    @staticmethod
    def importData(strNodeFile, strEdgeFile,strNeo4jHome):
        strCmd = 'neo4j-admin import --nodes "%s" --relationships "%s"' % (strNodeFile, strEdgeFile)

        try:
            subprocess.call("neo4j stop",shell=True)
            subprocess.call('rm -rf %s/data/databases/graph.db' % strNeo4jHome, shell=True)
            subprocess.call(strCmd, shell=True)
            subprocess.call('neo4j start', shell=True)
            objResult = Result(0)
            return objResult
        except Exception as e:
            Log.wEvent("importData error %s" % str(e) )
            objResult = Result(-1)
            objResult.setItem("status_info", str(e))
            return objResult

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: %s config_file" % sys.argv[1])
        sys.exit(-1)
    Config.load(sys.argv[1])
    username = Config.getItem("username")
    password = Config.getItem("password")
    host = Config.getItem("host")
    port = Config.getItem("port")
    handle = Neo4jHandler(host,port,username,password)

    cypher_query = ''' match (n:IP)-[:Login]-(m:IP{bg:"WXG微信事业群", is_sense_area:1})
                       where n.ip in {ip_list} 
                       return m;'''
    #                  match (n)-[:Login]-(m:IP{bg:"WXG微信事业群", is_sense_area:1})
    #                  return n;'''

    result = handle.cypherQuery(cypher_query, {"ip_list":["10.123.98.23"]})
