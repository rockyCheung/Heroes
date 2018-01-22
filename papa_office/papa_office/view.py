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
import logging
from papa_office.security.PaUser import *
# from django.contrib.auth.decorators import login_required
from papa_office.celery.Tasks import *
from papa_office.models.ESModels import M

reload(sys)  # Python2.5 初始化后会删除 sys.setdefaultencoding 这个方法，我们需要重新载入
sys.setdefaultencoding('utf-8')
logger = logging.getLogger(name='view')

# @login_required
@check_user
def hello(request):
    context = {}
    #test
    context['hello'] = _('msg.0003')
    logger.info('say hello')
    return render(request, 'hello.html', context)

def index(request):
    # M(1,'aaa','dddd','vvv').save()
    q = M.es.all()#search('3308211963',facets=['IDcard'])
    print q
    context = {}
    return render(request, 'login.html', context)

@login_filter(login_before,login_after)
def login(request):
    userEmail = request.session.get('_auth_user_email', default=None)
    userName = request.session.get('_auth_user_login_name', default=None)
    context = {'resultMsg': 'login success', 'resultCode': _('msg.0000'), 'fname': userEmail, 'email': userName}
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

def receiveEmail(request):
    mail_receive.delay('zhangpenghong@pengpengw.com')
    output = _("User email receive worker start.")
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
