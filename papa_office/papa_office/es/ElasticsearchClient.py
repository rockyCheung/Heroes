# -*- coding:utf-8 -*-
from elasticsearch import Elasticsearch
from papa_office.conf.GlobleConfig import *

class EladsticsearchClient(object):

    def __init__(self):
        self.client = Elasticsearch(ELASTICSEARCH_URL)

    def search(self,index,docType,body):
        return self.client.search(index,docType,body)

class Query(object):
    @staticmethod
    def getMatchQuery(simpleConditions):
        query = {}
        matchCondition = Query.Match(simpleConditions)
        query['query'] = matchCondition.match
        return query

    class Match(object):
        def __init__(self,match):
            self.match = {}
            self.match['match'] = match

####################################example############################################
# clt = EladsticsearchClient()
#
# d = {}
# d['outputValue'] = u'金融借款合同纠纷'
# m = Query.getMatchQuery(d)
# print m
# res = clt.search(index="judicial",docType='judicialDishonesty', body=m)
# print res#['_source']
####################################example############################################