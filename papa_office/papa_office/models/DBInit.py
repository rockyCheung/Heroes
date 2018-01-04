# -*- coding:utf-8 -*-
from papa_office.models.MongoModels import Keys,User
import datetime

# today =  time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
keys = Keys('a!sxzd12$oknde#s',datetime.datetime.now(),1,0).save()
keys = Keys.objects.get({'status': 1,'sflag':0})
print keys.key
