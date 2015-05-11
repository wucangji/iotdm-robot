#!/usr/bin/env python
import ddm
c = ddm.connect("localhost:8282", "admin", "admin", protocol="http")

ae = ddm.id(c.create("InCSE1", "AE"))
if ae == None:
	print "!ae", c.error
cr = ddm.id(c.create(ae, "container"))
if cr == None:
	print "!cr", c.error
x = c.create(cr, "subscription", {"notificationURI":"http://localhost:20000", "notificationContentType":"wholeResource"})
if x == None:
	print "!su", c.error
su = ddm.id(x)
ci = ddm.id(c.create(cr, "contentInstance", {"content": "102"}))
if ci == None:
	print "!ci", c.error

print ddm.AE, ae
print ddm.CR, cr
print ddm.CI, ci
print "su", ci

exit()

def huh(x):
	if x == None:
		print "c.error", c.error
	else:
		print "x", x

x = c.update(ae, {"labels":"100"})
huh(x)

x = c.update(cr, {"labels":"101"})
huh(x)

x = c.retrieve(ci)
huh(x)
