import ddm
import nserver
import nparser
import time

def connect_to_ddm(host, user, pw, p):
	return ddm.connect(host, user, pw, protocol=p)

def new_notification_server(ip, port):
	return nserver.server(ip, int(port))

def read_notifications(n, timeout):
	p = nparser.parse()
	timeout = float(timeout)
	mark = time.time() + timeout
	more = True
	while True:
		now = time.time()
		if now > mark:
			break
		newtimeout = mark - now
		(what, who, data) = n.wait(newtimeout)
		if what == "error":
			return
		if what == "data":
			more = p.process(data)
			if more == False:
				break
		if what == "timeout":
			break
		if more == False:
			break
	return p.body

def close_notification_server(n):
	n.close()

def create_resource(c, parent, restype, attr=None):
	"""Create Resource"""
	if attr == None:
		x = c.create(parent, restype)
	else:
		x = c.create(parent, restype, attr)
	if x == None:
		print "error", c.error, c.head, c.body
		raise AssertionError('Cannot create this resource')
	return ddm.id(x)

# this might not be necessary now that the library functions can take dicts

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

def update_resource(c, id, attr):
	"""Update Resource"""
	x = c.update(id, attr)
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
	
