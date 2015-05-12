#!/usr/bin/env python

import riotdm

def show(r):
	print r
	try:
		print r.text
	except:
		print "?"

c = riotdm.connect_to_iotdm("localhost", "admin", "admin", "http")
#n = riotdm.new_notification_server("localhost", 20000)
application = riotdm.create_resource(c, "InCSE1", riotdm.application)
show(application)
co = riotdm.create_resource(c, riotdm.id(application), riotdm.container)
show(co)
#riotdm.create_subscription(c, co, "localhost", 20000)
ci = riotdm.create_resource(c, riotdm.id(co), riotdm.contentInstance, {"con": "val"})
show(ci)
#d = riotdm.read_notifications(n, 10)
#riotdm.close_notification_server(n)
#print d
