#!/usr/bin/python3
from vcloud import vcloud
from db import ialab_db
import configparser

config = configparser.ConfigParser()
config.read('mac.conf')

db = ialab_db(config) 
vcloud = vcloud(config)
vapps = vcloud.getVappHrefs()
for vapp in vapps:
    vms = vcloud.getVMs(vapp)
    for vm in vms:
        mac = vcloud.getMAC(vm)
        print(vapp[0], mac[0], mac[1])
        db.insertMAC(vapp[0], mac[0], mac[1])