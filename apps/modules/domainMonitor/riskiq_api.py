#-*-coding:utf-8-*-
import requests
from setting import *
import time

class RiskIQ(object):
    def __init__(self, domain):
        self.addr = 'https://api.passivetotal.org/v2/enrichment/subdomains'
        self.user = riskiqApiName
        self.key =  riskiqApiKey
        self.domain = domain

    def query(self):
        subdomain_data = []
        params = {'query': self.domain}
        for name,key in zip(self.user,self.key):
            resp = requests.get(url=self.addr,params=params,auth=(name, key))
            data = resp.json()
            try:
                if data['status'] != 429:
                    for subdomains in data['subdomains']:
                        subdomain_data.append(str(subdomains)+"."+str(self.domain))
                    break
                else:
                    continue
            except Exception as e:
                for subdomains in data['subdomains']:
                    subdomain_data.append(str(subdomains)+"."+str(self.domain))
                break
        return subdomain_data

def do(domain):  # 统一入口名字 方便多线程调用
    query = RiskIQ(domain)
    result = query.query()
    return result

