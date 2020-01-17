from __future__ import unicode_literals

from django.shortcuts import render,redirect
from functools import wraps
# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import json
import math
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
import sys,os

o_path = os.getcwd()
sys.path.append(o_path+"/apps/login")
from loginViews import *


@check_login
def domainManager(request):
    return render(request,"domainManager.html")

@check_login
@csrf_exempt
def domainManager_create(request):
    if request.method == "POST":
        domain_name = request.POST.get("domainName")
        domain_owner = request.POST.get("domainOwner")
        domain_mark = request.POST.get("domainMark")
        load_index_data.client_mongodb_insert_domain(domain_owner,domain_name,domain_mark)
        return redirect('/domain?page=1')
    return redirect('/index')

@check_login
def load_domain_data_index(request):
    if request.method == "GET" and request.GET.get('page'):
        use_domain_data_index = load_index_data.client_mongodb_load_domain_all()
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

@check_login
def load_subdomain_data_index(request):
    page = request.GET.get('page')
    count_subdomain_num = load_index_data.client_mongodb_countSubdomains()
    if request.GET.get('limit') == 'all':
        next_page = 1+1
        use_domain_data_index = load_index_data.client_mongodb_find_all_Sudbmains(1)
        use_online_data_index = load_index_data.client_mongodb_load_online_Subdomains(1)
        load_subdomains_data = [i for i in use_domain_data_index]
        load_online_subdomains_data = [i for i in use_online_data_index]
        counts = math.ceil(int(count_subdomain_num)/25)
        return render(request,"subdomainsMonitors.html", {'contacts': load_subdomains_data,'online':load_online_subdomains_data,'counts':int(counts),'previous':1,'next_page':next_page})
    else:
        previous_page = int(page) - 1
        if previous_page <= 0:
            previous_page = 1
        next_page = int(page) + 1
        use_domain_data_index = load_index_data.client_mongodb_find_all_Sudbmains(int(page))
        use_online_data_index = load_index_data.client_mongodb_load_online_Subdomains(int(page))
        load_subdomains_data = [i for i in use_domain_data_index]
        load_online_subdomains_data = [i for i in use_online_data_index]
        counts = math.ceil(int(count_subdomain_num)/25)
        return render(request,"subdomainsMonitors.html", {'contacts': load_subdomains_data, 'online':load_online_subdomains_data ,'counts': int(counts),'previous':previous_page,'next_page':next_page})
         

