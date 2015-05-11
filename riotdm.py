import iotdm
#import nserver
#import nparser
import time

ae = iotdm.ae
container = iotdm.container
contentInstance = iotdm.contentInstance

def connect_to_iotdm(host, user, pw, p):
	return iotdm.new(host, base="InCSE1", auth=(user, pw), protocol=p)

'''
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
'''

def create_resource(c, parent, restype, a=None):
	"""Create Resource"""
	restype = int(restype)
	if a == None:
		x = c.create(parent, restype)
	else:
		x = c.create(parent, restype, attr=a)
	if x == None:
		raise AssertionError('Cannot create this resource')
	elif hasattr(x, 'status_code'):
		if x.status_code < 200 or x.status_code > 299:
			raise AssertionError('Cannot create this resource [%d] : %s' % (x.status_code, x.text))
	return x

# this might not be necessary now that the library functions can take dicts

def create_subscription(c, parent, ip, port):
	"""Create Subscription"""
	uri = "http://%s:%d" % (ip, int(port))
	x = c.create(parent, "subscription", {"notificationURI": uri, "notificationContentType": "wholeResource"})
	if x == None:
		raise AssertionError('Cannot create this subscription')
	elif hasattr(x, 'status_code'):
		if x.status_code < 200 or x.status_code > 299:
			raise AssertionError('Cannot create subscription [%d] : %s' % (x.status_code, x.text))
	return x

def retrieve_resource(c, id):
	"""Retrieve Resource"""
	x = c.retrieve(id)
	if x == None:
		raise AssertionError('Cannot retrieve this resource')
	elif hasattr(x, 'status_code'):
		if x.status_code < 200 or x.status_code > 299:
			raise AssertionError('Cannot retrieve this resource [%d] : %s' % (x.status_code, x.text))
	return x

def update_resource(c, id, attr):
	"""Update Resource"""
	x = c.update(id, attr)
	if x == None:
		raise AssertionError('Cannot update this resource')
	elif hasattr(x, 'status_code'):
		if x.status_code < 200 or x.status_code > 299:
			raise AssertionError('Cannot update this resource [%d] : %s' % (x.status_code, x.text))
	return x

def delete_resource(c, id):
	"""Delete Resource"""
	x = c.delete(id)
	if x == None:
		raise AssertionError('Cannot delete this resource')
	elif hasattr(x, 'status_code'):
		if x.status_code < 200 or x.status_code > 299:
			raise AssertionError('Cannot delete this resource [%d] : %s' % (x.status_code, x.text))
	return x

def id(x):
	return iotdm.id(x)

def text(x):
	return x.text

def status_code(x):
	return x.status_code

def json(x):
	return x.json()

def elapsed(x):
	return x.elapsed.total_seconds()

def invalid_create_resource(c, parent, restype, dictionary=None):
    x = c.create(parent, restype, dictionary)
    if x == None:
        print "success error", c.error
        return "pass"
    else:
        raise AssertionError('Create the wrong resource, this resource should not be created!')
