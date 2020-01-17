#-*-coding:utf8-*-
from pymongo import MongoClient
import time,datetime

class UseMongoData(object):
    def __init__(self,host,port,user,passwd):
        mongo_uri = "mongodb://%s:%s/" % (host,port)
        self.client = MongoClient(mongo_uri)
        self.client.MonitorSubdomains.authenticate(user,passwd,mechanism='SCRAM-SHA-1')
        self.now_str_time = time.strftime('%Y-%m-%d %H:%M:%S')
        self.now_datetime = datetime.datetime.now()
        self.Yesterday_datetime = datetime.datetime.now()-datetime.timedelta(days=1)

    def client_mongodb_load_domain_all(self):
        load_all_domain_data = []
        db = self.client['MonitorSubdomains']
        collection = db['domain_list']
        for i in collection.find():
            load_all_domain_data.append(i)
        return load_all_domain_data

    def client_mongodb_load_domain_index(self):
        #return self.client['MonitorSubdomains']['Subdomains'].find({"create_time":{"$gte":self.Yesterday_datetime}})
        return self.client['MonitorSubdomains']['Subdomains'].find({})

    def client_mongodb_insert_domain(self,owner,domain,mark):
        return self.client['MonitorSubdomains']['domain_list'].insert({"owner":owner,"domain":domain,"insert_time":self.now_str_time,"mark":mark,"create_time":self.now_datetime})

    def client_mongodb_del_domain(self,domain):
        return self.client['MonitorSubdomains']['domain_list'].remove({"domain":domain})

    def client_mongodb_insert_Subdomains(self,subdomains,data_source):
        return self.client['MonitorSubdomains']['Subdomains'].insert({"subdomains":subdomains,"insert_time":self.now_str_time,"source":data_source,"create_time":self.now_datetime})

    def client_mongodb_update_Subdomains(self,subdomains):
        return self.client['MonitorSubdomains']['Subdomains'].update_one({"subdomains":subdomains},{"$set":{"create_time":self.now_datetime,"source" : "riskiq"}})

    def client_mongodb_update_domainStatus(self,subdomains,data_status,domainTitle,domainStatus):
        return self.client['MonitorSubdomains']['Subdomains'].update_one({"subdomains":subdomains},{"$set":{"create_time":self.now_datetime,"domain_status":data_status,"domain_info.title":domainTitle,"domain_info.status":domainStatus,"domain_info.ctime":self.now_str_time}})

    def client_mongodb_find_Subdomains(self,subdomains):
        return self.client['MonitorSubdomains']['Subdomains'].find_one({"subdomains":subdomains})
  
    def client_mongodb_find_all_Sudbmains(self,page):
        return self.client['MonitorSubdomains']['Subdomains'].find({}).limit(25).skip(25*int(page-1)+1)

    def client_mongodb_load_online_Subdomains(self,page):
        return self.client['MonitorSubdomains']['Subdomains'].find({"domain_status" : "online"}).limit(25).skip(25*int(page-1)+1)

    def client_mongodb_find_sSubdomains(self,subdomains):
        return self.client['MonitorSubdomains']['Subdomains'].find({"subdomains":subdomains})

    def client_mongodb_countSubdomains(self):
        return self.client['MonitorSubdomains']['Subdomains'].find({}).count()
