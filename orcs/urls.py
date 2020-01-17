#-*-coding:utf-8-*-
"""orcs URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
#from login import views
from apps.login import loginViews
from apps.domainManager import ManagerDomainViews

urlpatterns = [
    #url(r'^admin/', include(admin.site.urls)),
    #url(r'^login', views.login_on),
    url(r'^$',loginViews.index_on),
    url(r'^login', loginViews.login_on),
    #url(r'^index$', views.index_on),
    url(r'^index$', loginViews.index_on),
    url(r'^domain$', ManagerDomainViews.load_domain_data_index),
    url(r'^domain/domain_insert', ManagerDomainViews.domainManager_create),
    url(r'^tests', ManagerDomainViews.tests),
    #url(r'domain/list_domain/', ManagerDomainViews.list_table_page),
    url(r'^delDomain', ManagerDomainViews.del_domain_data_index),
    url(r'^subdomains',ManagerDomainViews.load_subdomain_data_index),
]
