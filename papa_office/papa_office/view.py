import sys

from django.http import HttpResponse
from django.shortcuts import render
from papa_office.security.UUIDTools import *
from papa_office.security.Pycrypt import Pycrypt
import time
from papa_office.models.MongoModels import User,Keys


def hello(request):
    context = {}
    context['hello'] = 'Hello World!'
    return render(request, 'hello.html', context)
    # return HttpResponse("Hello world ! ")

def index(request):
    context = {}
    return render(request, 'login.html', context)
def login(request):
    if request.POST:
        email = request.POST['email']
        password = request.POST['password']
        print email,'@@@@@@@@@@@@@@@@',password
    context = {}
    return render(request, 'index.html', context)
def register(request):
    print '###############'
    context = {}
    return render(request, 'register.html', context)
def registerSubmit(request):
    today = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print '@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@'
    keys = Keys.objects.get({'status': 1,'sflag':0})
    encrptKey = keys.key
    salt = UUIDTools.generateUUID()
    crpt = Pycrypt(key=encrptKey, salt=salt.get_hex())
    password = crpt.encrypt(request.POST['password'])
    rpassword = crpt.encrypt(request.POST['rpassword'])
    if password != rpassword:
        return render(request, 'login.html')
    else:
         User(request.POST['email'], request.POST['fname'], password, today, 0, salt, 0).save()
    context = {'fname':request.POST['fname'],'email':request.POST['email']}
    return render(request, 'index.html', context)

# keys = Keys.objects.raw({'status': 1,'sflag':0})
#
# for key in keys:
#     print(key.key + '@@ ')