#!/usr/bin/python2.7
#-*-config:utf-8-*-
import requests
from bs4 import BeautifulSoup
from domainMonitor.riskiq_api import do,RiskIQ 
import os,sys
import json

sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "../common")))
from UseMongoDBManager import UseMongoData
from client import *


class checkDomainHttpResponse(object):
    def __init__(self):
        self.timeout = 2
        self.verify = True
        self.load_index_data = UseMongoData(load_mongodb_host,load_mongodb_port,load_mongodb_user,load_mongodb_pass)

    def _GET(self):
        for load_domain in self.load_index_data.client_mongodb_load_domain_index():
            domain = load_domain['subdomains']
            if 'http' not in domain:
                url = 'http://'+ str(domain)
                try:
                    load_response_data = requests.get(url=url,headers={},verify=self.verify,timeout=self.timeout)
                    domain_status = load_response_data.status_code
                    load_response_data.encoding = 'utf-8' 
                    soup = BeautifulSoup(load_response_data.text, 'lxml')
                    domain_title = soup.title.text
                    self.load_index_data.client_mongodb_update_domainStatus(domain,"online",domain_title,domain_status)
                except Exception as e:
                    self.load_index_data.client_mongodb_update_domainStatus(domain,"offline","",0)


class MonitorSubdomains(object):
    def __init__(self):
        self.load_index_data = UseMongoData(load_mongodb_host,load_mongodb_port,load_mongodb_user,load_mongodb_pass) 
 
    def riskiq_scan(self):
        for domain in self.load_index_data.client_mongodb_load_domain_all():
            for i in do(domain['domain']):
                if self.load_index_data.client_mongodb_find_Subdomains(i) == None:
                    self.load_index_data.client_mongodb_insert_Subdomains(i,"riskiq")
                else:
                    self.load_index_data.client_mongodb_update_Subdomains(i)

t = MonitorSubdomains()
http_response = checkDomainHttpResponse()
http_response._GET()
#t.riskiq_scan()


