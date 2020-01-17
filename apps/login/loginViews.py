# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,redirect
from functools import wraps
# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
#from readConf import load_conf_setting
#from core.UseMongoDBManager import UseMongoData 
import json
from django.core.paginator import Paginator

import os,sys
sys.path.append("apps/common")
from utils import load_conf_setting
from UseMongoDBManager import UseMongoData
from utils import *




#load_mongodb_host = load_conf_setting("mongodb_client","mongodb_hosts")
#load_mongodb_port = load_conf_setting("mongodb_client","mongodb_port")
#load_mongodb_user = load_conf_setting("mongodb_client","mongodb_username")
#load_mongodb_pass = load_conf_setting("mongodb_client","mongodb_password")
load_index_data = UseMongoData(load_mongodb_host,load_mongodb_port,load_mongodb_user,load_mongodb_pass)


def check_login(f):
    @wraps(f)
    def inner(request,*arg,**kwargs):
        if request.session.get('is_login')=='1':
            return f(request,*arg,**kwargs)
        else:
            return redirect('/login')
    return inner

@check_login
def index_on(request):
    return render(request,"index.html")


@csrf_exempt
def login_on(request):
    # 如果是POST请求，则说明是点击登录按扭 FORM表单跳转到此的，那么就要验证密码，并进行保存session
    if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        #if username == "admin" and password == "e2d4ef144dee4b1f897e013d99657db7":
        if username == "admin" and password == load_conf_setting("admin_login","admin_password"):
            request.session['is_login']='1'
            #request.session['user_id']=user[0].id
            return redirect('/index')
    # 如果是GET请求，就说明是用户刚开始登录，使用URL直接进入登录页面的
    return render(request,'login.html')

'''
 
@check_login
def load_domain_data_index(request):
    if request.method == "GET" and request.GET.get('page'):
        use_domain_data_index = load_index_data.client_mongodb_load_domain_all()
        #return render(request,"domainManager.html",{'result':use_domain_data_index})
        paginator = Paginator(use_domain_data_index, 10)
        page = request.GET.get('page')
        contacts = paginator.page(int(page))
        return render(request,"domainManager.html",{'contacts':contacts})
    else:
        return render(request,"domainManager.html")

@check_login
def del_domain_data_index(request):
    if request.method == "GET" and request.GET.get('domain_data'):
        del_domain_data_index = load_index_data.client_mongodb_del_domain(request.GET.get('domain_data'))
        return redirect('/domain?page=1')
    else:
        return render(request,"domainManager.html")

def list_table_page(request):
    if 'page' in request.GET:
        page = request.GET['page']
        if page == "1":
            message = {"code": 0,"message":"","data":{"item":[{"id":1,"domainOwner":"虎牙","listDomain":"huya.com","insertTime":"2019-12-24 15:18","mark":"test"}]}}
            return HttpResponse(json.dumps(message,ensure_ascii=False),content_type="application/json,charset=utf-8")
'''

def tests(request):
    if request.method == "GET":
        return render(request,"base_up.html",{"title":"subdomains","result":[{"subdomain":"admin.baidu.com","create_time":"2019-12-27 19:04","source":"riskiq"}]})





