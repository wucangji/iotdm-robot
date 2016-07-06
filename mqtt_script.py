#!/usr/bin/python

import criotdm
import ciotdm
import paho.mqtt.subscribe as subscribe
import json

# Set varibles
httphost = "localhost"
httpuser = "admin"
httppass = "admin"
rt_container       = 3
rt_contentInstance = 4



def create_container(container_name):
	attr = '"rn":%s' %(container_name)
	container_resp = connect.create("InCSE1", rt_container, attr)
	# print container_resp.text

def create_cin(path, payload):
	payload1 = json.dumps(payload)
	attr = '"con":%s' %(payload1)
	conIn_resp = connect.create(path, rt_contentInstance, attr)
	# print conIn_resp.text

def on_message_print(client, userdata, message):
	print("%s %s" % (message.topic, message.payload))
	payload = json.loads(message.payload)
	# print(payload['deviceName'])
	create_container(payload['deviceName'])
	path = "InCSE1/" + payload['deviceName']
	create_cin(path, message.payload)

connect = criotdm.connect_to_iotdm(httphost, httpuser, httppass, "http")
subscribe.callback(on_message_print, "/tdf/test", hostname="168.128.108.105")