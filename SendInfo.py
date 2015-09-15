#!/usr/bin/python

import criotdm
import ciotdm
import psutil
import threading

# Set varibles
httphost = "localhost"
httpuser = "admin"
httppass = "admin"
rt_ae              = 2
rt_container       = 3
rt_contentInstance = 4

def sendCon():
    threading.Timer(1.0,sendCon).start()
    cpu = psutil.cpu_percent(interval=None)
    attr = conattr + ":" + '\"%s\"' %(cpu)
    print conattr
    conIn_resp = connect.create("InCSE1/TemContainer", rt_contentInstance, attr)
    print conIn_resp.text

connect = criotdm.connect_to_iotdm(httphost, httpuser, httppass, "http")
attr = '"mni":1'
#attr=""
container_resp = connect.create("InCSE1", rt_container, attr, "TemContainer")
print(container_resp.text)

conattr = '"con"'

sendCon()


