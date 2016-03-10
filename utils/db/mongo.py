#!/usr/bin/env python
#! -*- coding:UTF-8 -*-

from pymongo import MongoClient
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

class GenMongo:
    client = ''

    def __init__(self, host, port):
        try:
            self.client = MongoClient(host, port)
        except:
            print "not exsit mongodb"


    def get_database(self, dbname):
        db = self.client[dbname]
        if not db:
            return False
        else:
            return db


    def get_collection(self, dbname, collection):
        collection = self.client[dbname][collection]
        if not collection:
            return False
        else:
            return collection



