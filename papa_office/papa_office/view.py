# -*- coding:utf-8 -*-
import sys
from django.shortcuts import render
from papa_office.security.UUIDTools import *
from papa_office.security.Pycrypt import Pycrypt
import time
from papa_office.models.MongoModels import User,Keys
from papa_office.conf.GlobleConfig import *
from django.utils.translation import ugettext as _
from django.http import HttpResponse

reload(sys)  # Python2.5 初始化后会删除 sys.setdefaultencoding 这个方法，我们需要重新载入
sys.setdefaultencoding('utf-8')

def hello(request):
    context = {}
    #test
    context['hello'] = _('msg.0003')
    return render(request, 'hello.html', context)
    # return HttpResponse("Hello world ! ")

def index(request):
    context = {}
    return render(request, 'login.html', context)
def login(request):
    email = ''
    password = ''
    if request.POST:
        email = request.POST['email']
        password = request.POST['password']
    user = User.objects.get({'_id': email})
    if user is None:
        context = {'resultMsg':'user does not exist','resultCode':_('msg.0001')}
        return render(request, 'login.html', context)

    crpt = Pycrypt(key=COMMON_CONFIG['user_key'], salt=user.salt)
    password = crpt.encrypt(password)
    if password == user.password:
        context ={'resultMsg':'login success','resultCode':'msg.0000','fname':user.fname,'email':user.email}
        return render(request, 'index.html', context)

def register(request):
    context = {}
    return render(request, 'register.html', context)
def registerSubmit(request):
    today = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    # keys = Keys.objects.get({'status': 1,'sflag':0})
    encrptKey = COMMON_CONFIG['user_key']
    salt = UUIDTools.generateUUID()
    crpt = Pycrypt(key=encrptKey, salt=salt.get_hex())
    password = crpt.encrypt(request.POST['password'])
    rpassword = crpt.encrypt(request.POST['rpassword'])
    if password != rpassword:
        context = {'resultMsg': 'Two inputted password inconsistencies', 'resultCode': 'msg.0002'}
        return render(request, 'login.html',context)
    else:
         User(request.POST['email'], request.POST['fname'], password, today, 0, salt, 0).save()
    context = {'fname':request.POST['fname'],'email':request.POST['email']}
    return render(request, 'index.html', context)

def my_view(request):
    output = _("Welcome to my site.")
    return HttpResponse(output)
# keys = Keys.objects.raw({'status': 1,'sflag':0})
#
# for key in keys:
#     print(key.key + '@@ ')
# from django.utils.translation import get_language_info
# li = get_language_info('en')
# print(li['name'], li['name_local'], li['bidi'])
# output = _("Welcome to my site.")
# print output
