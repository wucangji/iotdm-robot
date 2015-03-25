import ddm
import nserver

def connect_to_ddm(host, user, pw, p):
	return ddm.connect(host, user, pw, protocol=p)

def new_notification_server(ip,port):
	return nserver.server(ip, int(port))

def read_notifications(n, howlong):
	a = ""
	while n.inputs:
		(what, who, data) = n.wait(int(howlong))
		if what == "data":
			a = a + data
		if what == "timeout":
			break
	return a

def create_resource(c, parent, restype, key=None, val=None):
	"""Create Resource"""
	x = None
	if key == None or val == None:
		x = c.create(parent, restype)
	else:
		x = c.create(parent, restype, {key: val})
	if x == None:
		print "error", c.error
		raise AssertionError('Cannot create this resource')
	return ddm.id(x)


def create_subscription(c, parent, ip, port):
	"""Create Subscription"""
	uri = "http://%s:%d" % (ip, int(port))
	x = c.create(parent, "subscription", {"notificationURI": uri, "notificationContentType": "wholeResource"})
	if x == None:
		print "error", c.error
		raise AssertionError('Cannot create subscription')
	return ddm.id(x)

def retrieve_resource(c, id):
	"""Retrieve Resource"""
	x = c.retrieve(id)
	if x == None:
		print "error", c.error
		raise AssertionError('Cannot retrieve this resource')
	return x

def update_resource(c, id, key, val):
	"""Update Resource"""
	x = c.update(id, {key: val})
	if x == None:
		print "error", c.error
		raise AssertionError('Cannot update this resource')
	return x

def delete_resource(c, id):
	"""Delete Resource"""
	x = c.delete(id)
	if x == None:
		print "error", c.error
		raise AssertionError('Cannot delete resource')
	return x
	
