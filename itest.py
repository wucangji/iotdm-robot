#!/usr/bin/env python

import iotdm

c = iotdm.connect_to_ddm("localhost:8282", "admin", "admin", "http")
n = iotdm.new_notification_server("localhost", 20000)
ae = iotdm.create_resource(c, "InCSE1", "AE")
co = iotdm.create_resource(c, ae, "container")
iotdm.create_subscription(c, co, "localhost", 20000)
iotdm.create_resource(c, co, "contentInstance", {"contents": "a value"})
d = iotdm.read_notifications(n, 10)
iotdm.close_notification_server(n)
print d

c = iotdm.connect_to_ddm("localhost:8181", "admin", "admin", "restconf")
n = iotdm.new_notification_server("localhost", 30000)
ae = iotdm.create_resource(c, "InCSE1", "AE")
co = iotdm.create_resource(c, ae, "container")
iotdm.create_subscription(c, co, "localhost", 30000)
iotdm.create_resource(c, co, "contentInstance", {"contents": "a value"})
d = iotdm.read_notifications(n, 10)
iotdm.close_notification_server(n)
print d
