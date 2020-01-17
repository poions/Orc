import os,sys
import ConfigParser
from UseMongoDBManager import UseMongoData

def load_conf_setting(tname,cname):
    cf = ConfigParser.ConfigParser()
    #print(os.path.abspath('.')+"/conf/setting.conf")
    cf.read(os.path.abspath(os.path.abspath('../../')+"/conf/setting.conf"))
    load_conf_data = str(cf.get(tname, cname))
    return load_conf_data



load_mongodb_host = load_conf_setting("mongodb_client","mongodb_hosts")
load_mongodb_port = load_conf_setting("mongodb_client","mongodb_port")
load_mongodb_user = load_conf_setting("mongodb_client","mongodb_username")
load_mongodb_pass = load_conf_setting("mongodb_client","mongodb_password")
load_index_data = UseMongoData(load_mongodb_host,load_mongodb_port,load_mongodb_user,load_mongodb_pass)

