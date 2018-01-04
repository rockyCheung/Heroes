# -*- coding:utf-8 -*-
from pymongo import MongoClient,cursor

class MongodbClient:

    # 初始化数据库客户端
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.client = MongoClient(self.ip, self.port)
    ############################################
    # 获取数据库链接，dataBaseName为数据库名称
    ############################################
    def getConnection(self,dataBaseName):
        return self.client[dataBaseName]

    ############################################
    # 插入数据
    ############################################
    def insertItem(self,dataBaseName,collectionName,list):
        db = self.getConnection(dataBaseName=dataBaseName)
        db[collectionName].insert(list)