import requests
from datetime import timedelta

ae=2
container=3
contentInstance=4

cse_payload = '''
{    "input": {
        "onem2m-primitive": [
           {
                "name": "CSE_ID",
                "value": "%s"
            },
            {
                "name": "CSE_TYPE",
                "value": "IN-CSE"
            }
        ]
    }
}
''' # % (cse_id)

ae_payload = '''
{
  any:
  [
	{"aei":"jb", "api":"jb", "apn":"jb2", "or":"http://hey/you" %s}
  ]
}
''' # % (attr_str)

_container_payload = '''
{
  any:
  [
    {
      "cr": "jb", 
      "mni": 1, 
      "mbs": 3, 
      "or": "http://hey/you"
	  %s
    }
  ]
}
''' # % (attr_str)

container_payload = '''
{
  any:
  [
    {
      "cr": "jb", 
      "or": "http://hey/you"
	  %s
    }
  ]
}
''' # % (attr_str)

contentInstance_payload = '''
{
  "any": [
    {
      "cnf": "1", 
      "or": "http://hey/you"
	  %s
    }
  ]
}
''' # % (attr_str)

def which_payload(restype):
	"""Return a template payload for the known datatypes."""
	if restype == ae:
		return ae_payload
	elif restype == container:
		return container_payload
	elif restype == contentInstance:
		return contentInstance_payload
	else:
		return ""

def _dig(r,k):
	"""Try to find the key 'k' in a response 'r'."""
	try:
		j = r.json()
		id = j['any'][0][k]
		return id
	except:
		return None

def name(r):
	"""Return the resource name in the response 'r'."""
	return _dig(r, "rn")

def id(r):
	"""Return the resource id in the response 'r'."""
	return _dig(r, "ri")

def parent(r):
	"""Return the parent resource id in the response 'r'."""
	return _dig(r, "pi")

def content(r):
	"""Return the content the response 'r'."""
	return _dig(r, "con")

def restype(r):
	"""Return the resource type the response 'r'."""
	return _dig(r, "rty")

def status(r):
	"""Return the protocol status code in the response 'r'."""
	try:
		return r.status_code
	except:
		return None

def headers(r):
	"""Return the protocol headers in the response 'r'."""
	try:
		return r.headers
	except:
		return None

def error(r):
	"""Return the error string in the response 'r'."""
	try:
		return r.json()['error']
	except:
		return None

def normal(id):
	if id != None:
		if id[0] == "/":
			return id[1:]
	return id

def attr2str(attr):
	"""Convert a dictionary into a string suitable for inclusion in a protocol payload."""
	content = ""
	if attr != None:
		content = ","
		n = len(attr)
		c = 1
		sep = ","
		for i in attr:
			if n == c:
				sep = ""
			n = str(attr[i])
			if i != "con" and n.isdigit():
				content = content + "'%s':%d%s" % (i, int(n), sep)
			else:
				content = content + "'%s':'%s'%s" % (i, n, sep)
			c = c + 1
	return content

class new:
	def __init__(self, server="localhost", base='InCSE1', auth=('admin','admin'), protocol="http"):
		"""Connect to a IoTDM server over-rideable defaults"""
		self.s = requests.Session()
		self.s.auth = auth
		#self.s.headers.update({'content-type': 'application/json', 'accept': 'application/json'})
		self.s.headers.update({'content-type': 'application/json'})
		self.timeout = (5,5)
		self.payload = cse_payload % (base)
		self.headers = {
			'content-type': 'application/json',
			'X-M2M-Origin': '//localhost:10000',
			'X-M2M-RI': '12345',
			'X-M2M-OT': 'NOW'
		}
		self.server = "http://" + server
		if base != None:
			self.url = self.server + ":8181/restconf/operations/onem2m:onem2m-cse-provisioning"
			self.r = self.s.post(self.url, data=self.payload, timeout=self.timeout)

	def create(self, parent, restype, name=None, attr=None):
		"""Create a new resource as a child of the given resource ID with the optional attribute name/value pair dictionary"""
		if parent == None:
			return None
		payload = which_payload(restype)
		payload = payload % (attr2str(attr))
		if name == None:
			self.headers['X-M2M-NM'] = None
		else:
			self.headers['X-M2M-NM'] = name
		parent = normal(parent)
		self.url = self.server + ":8282/%s?ty=%s&rcn=1" % (parent, restype)
		self.r = self.s.post(self.url, payload, timeout=self.timeout, headers=self.headers)
		#self.r = self.s.post(self.url, payload, timeout=self.timeout, headers={'X-M2M-NM': name})
		#print self.r.request.headers
		return self.r

	def retrieve(self, id):
		"""Retrieve resource ID"""
		if id == None:
			return None
		id = normal(id)
		self.url = self.server + ":8282/%s?rcn=5&drt=2" % (id)
		self.headers['X-M2M-NM'] = None
		self.r = self.s.get(self.url, timeout=self.timeout, headers=self.headers)
		return self.r

	def update(self, id, attr=None):
		"""Update resource ID with attribute name/value pairs in the provided dictionary"""
		if id == None:
			return None
		id = normal(id)
		return None

	def delete(self, id):
		"""Delete the resource with the provided ID"""
		if id == None:
			return None
		id = normal(id)
		self.url = self.server + ":8282/%s" % (id)
		self.headers['X-M2M-NM'] = None
		self.r = self.s.delete(self.url, timeout=self.timeout, headers=self.headers)
		#print "request-header-?", self.r.request.headers
		return self.r

	def tree(self):
		"""Get the resource tree"""
		self.url = self.server + ":8181/restconf/operational/onem2m:onem2m-resource-tree"
		self.r = self.s.get(self.url)
		return self.r

	def kill(self):
		"""Kill the tree."""
		self.url = self.server + ":8181/restconf/operations/onem2m:onem2m-cleanup-store"
		#         http://localhost:8181/restconf/operations/onem2m:onem2m-cleanup-store
		self.r = self.s.post(self.url)
		return self.r
