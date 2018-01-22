# -*- coding:utf-8 -*-
from elasticsearch import Elasticsearch
from papa_office.conf.GlobleConfig import *
es = Elasticsearch(ELASTICSEARCH_URL)
# data = es.get(index="judicial", doc_type="judicialDishonesty", id='1gL7w14BmAAgcahOcziX')['_source']
# print data
res = es.search(index="judicial",doc_type='judicialDishonesty', body={"query": {"match_all": {}}})#"outputValue":'金融借款合同纠纷'
print res