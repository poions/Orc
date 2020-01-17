#!/usr/bin/python2.7
#-*-config:utf-8-*-
import requests
import threading
import Queue
import time,datetime
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

    def _GET(self,domain):
        if 'http' not in domain:
            url = 'http://'+ str(domain)
            try:
                load_response_data = requests.get(url=url,headers={},verify=self.verify,timeout=self.timeout)
                domain_status = load_response_data.status_code
                load_response_data.encoding = 'utf-8'
                soup = BeautifulSoup(load_response_data.text, 'lxml')
                domain_title = soup.title.text
                self.load_index_data.client_mongodb_update_domainStatus(domain,"online",domain_title,domain_status)
                print(json.dumps({"url":url,"status":"online"}))
            except Exception as e:
                self.load_index_data.client_mongodb_update_domainStatus(domain,"offline","",0)
                print(url,e)


class worker(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue
        self.thread_stop = False

    def run(self):
        while not self.thread_stop:
            try:
                task = q.get(block = True, timeout = 20)
            except Queue.Empty:
                self.thread_stop = True
                break
            for i in task:
                http_response = checkDomainHttpResponse()
                http_response._GET(i)
            q.task_done()
            res = q.qsize()
            if res > 0:
                print(res)

    def stop(self):
        self.thread_stop = True


def load_url_data():
    load_index_data = UseMongoData(load_mongodb_host,load_mongodb_port,load_mongodb_user,load_mongodb_pass)
    domain_data = [i['subdomains'] for i in load_index_data.client_mongodb_load_domain_index()]
    return domain_data






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


if __name__=="__main__":
    while True:
        now_times = datetime.datetime.now()
        if now_times.hour == 12 and now_times.minute == 12:
            t = MonitorSubdomains()
            t.riskiq_scan()
        elif now_times.hour== 23 and now_times.minute == 12:
            t = MonitorSubdomains()
            t.riskiq_scan()
        else:
            url = load_url_data()
            q = Queue.Queue(20)
            worker = worker(q)
            worker.start()
            q.put(url,block=True,timeout=None)
            q.join()
            time.sleep(1800)
