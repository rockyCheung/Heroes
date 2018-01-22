# -*- coding:utf-8 -*-
from papa_office.models.MongoModels import Keys
COMMON_CONFIG = dict()
keys = Keys.objects.get({'status': 1,'sflag':0})

COMMON_CONFIG['user_key'] = keys.key

ROCKET_PROXY = {
              "http"  : "http://127.0.0.1:3128",
              "https" : "https://127.0.0.1:3128",
            }
ROCKET_SERVER_URL = 'http://chat.lianhehuishang.com'
BROKER_URL = 'mongodb://192.168.1.178:27017/cobra'
ELASTICSEARCH_URL = 'http://192.168.1.171:9200'