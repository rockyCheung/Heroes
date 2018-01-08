# -*- coding:utf-8 -*-
# from django.contrib.auth.base_user import AbstractBaseUser
from django.shortcuts import render
from django.utils.translation import ugettext as _
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
import logging
from papa_office.models.MongoModels import User
from papa_office.security.Pycrypt import Pycrypt
from papa_office.conf.GlobleConfig import *

logger = logging.getLogger(name='PaUser')

class PaUser(object):
    def __init__(self,email,fname,password,cdate,status,salt,remember):
        self.email = email
        self.fname = fname
        self.password = password
        self.cdate = cdate
        self.status = status
        self.salt = salt
        self.remember = remember

def check_user(func):
    def inner(request,login_url='/login'):
        print 'login_url:',login_url
        print dict(request.session)
        try:
            user = request.session.get('_auth_user_login_status',default=None)
        except KeyError:
            context = {'resultMsg': 'user does not exist', 'resultCode': _('msg.0000')}
            return HttpResponseRedirect(login_url)
        if user is None or user is False:
            #this user not login
            context = {'resultMsg': 'user does not exist', 'resultCode': _('msg.0000')}
            return HttpResponseRedirect(login_url)
        else:
            pass
        return func(request)

    return inner

def login_before(request):
    logger.info(" login before")
    email = ''
    password = ''
    if request.POST:
        email = request.POST['email']
        password = request.POST['password']
    logger.info('user login ,login name: %s,login password: %s', email, password)
    try:
        user = User.objects.get({'_id': email})
        if user is None:
            context = {'resultMsg': 'user does not exist', 'resultCode': _('msg.0001')}
            logger.info('user is None!')
            return render(request, 'login.html', context)
        crpt = Pycrypt(key=COMMON_CONFIG['user_key'], salt=user.salt)
        password = crpt.encrypt(password)
        if password != user.password:
            logger.info('password error!')
            context = {'resultMsg': 'password error', 'resultCode': _('msg.0004'), 'fname': user.fname,
                       'email': user.email}
            return render(request, 'login.html', context)
    except User.DoesNotExist:
        logger.info('the user does not exist!')
        context = {'resultMsg': 'user does not exist', 'resultCode': _('msg.0001')}
        return render(request, 'login.html', context)
    request.session['_auth_user_email'] = user.email
    request.session['_auth_user_login_name'] = user.fname
    request.session['_auth_user_login_status'] = True


def login_after(request):
    userEmail = request.session.get('_auth_user_email', default=None)
    userName = request.session.get('_auth_user_login_name', default=None)
    logger.info('the user :%s, email: %s,login succeed',userName,userEmail)

def login_filter(before_func, after_func):
    def outer(main_func):
        def wrapper(request):

            before_result = before_func(request)
            if (before_result != None):
                return before_result;

            main_result = main_func(request)
            if (main_result != None):
                return main_result;

            after_result = after_func(request)
            if (after_result != None):
                return after_result;

        return wrapper

    return outer

def before(request, kargs):
    print 'before'


def after(request, kargs):
    print 'after'


def filter(before_func, after_func):
    def outer(main_func):
        def wrapper(request, kargs):

            before_result = before_func(request, kargs)
            if (before_result != None):
                return before_result;

            main_result = main_func(request, kargs)
            if (main_result != None):
                return main_result;

            after_result = after_func(request, kargs)
            if (after_result != None):
                return after_result;

        return wrapper

    return outer


@filter(before, after)
def Index(request, kargs):
    print 'index'

@check_user
def test(request, arg2):
    print 'ssss'
    print request,arg2

# test('1','2')

def deco(func):
    def _deco(a,b):
        print a, b
        print("before myfunc() called.")
        func(a,b)
        print("  after myfunc() called.")

        # 不需要返回func，实际上应返回原函数的返回值

    return _deco


@deco
def myfunc(a,b):
    print a,b
    print(" myfunc() called.")
    return 'ok'


# myfunc('1','2')
# myfunc('3','4')

