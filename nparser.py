def ishex(c):
	if c >= '0' and c <= '9':
		return True
	elif c >= 'A' and c <= 'F':
		return True
	elif c >= 'a' and c <= 'f':
		return True
	return False

def hextodec(c):
	return int(c, 16)

# states
# 0 = look for 1st \r
# 1 = look for 1st \n
# response done
# 2 = look for 2nd \r
# 3 = look for 2nd \n
# 4 = look for 3rd \r
# 5 = look for 3rd \n
# header done
# if Transfer-Encoding: chunked
# get hex digits then \r\n
# then read that # bytes and repeat until 0\r\n
# else should get content-length

class step(object):
	RESP0 = 0
	RESP1 = 1

	HEAD0 = 2
	HEAD1 = 3
	HEAD2 = 4
	HEAD3 = 5
	
	HEX0 = 6
	HEX1 = 7
	HEX2 = 8

	EAT0 = 9

class parse:
	def clean(self):
		self.state = step.RESP0
		self.ignore = 0
		self.response = ""
		self.head = []
		self.temp = ""
		self.body = ""

	def __init__(self):
		#print "parse.__init__"
		self.clean()

	def _process(self, c):
		##### look for 1st \r\n = RESPONSE
		if self.state == step.RESP0:
			if c == '\r':
				self.state = step.RESP1
			else:
				self.response = self.response + c
		elif self.state == step.RESP1:
			if c == '\n':
				#print "response done"
				self.state = step.HEAD0
				self.temp = ""
			else:
				self.state = step.RESP0
		##### look for 2nd & 3rd \r\n = HEAD
		elif self.state == step.HEAD0:
			if c == '\r':
				self.state = step.HEAD1
			else:
				self.temp = self.temp + c
		elif self.state == step.HEAD1:
			if c == '\n':
				self.head.append(self.temp.lower())
				self.temp = ""
				self.state = step.HEAD2
			else:
				self.state = step.HEAD0
		elif self.state == step.HEAD2:
			if c == '\r':
				self.state = step.HEAD3
			else:
				self.temp = self.temp + c
				self.state = step.HEAD0
		elif self.state == step.HEAD3:
			if c == '\n':
				#print "header done"
				# look at header for chunked or content-length here
				for i in range(0,len(self.head)):
					#print i, self.head[i]
					if self.head[i].find("content-length") >= 0:
						#print "FOUND CONTENT-LENGTH"
						self.state = step.EAT0
						self.ignore = 0 # get len from header BAD
						break
					#                     transfer-encoding
					if self.head[i].find("transfer-encoding") >= 0:
						#print "FOUND transfer-encoding"
						#                     chunked
						if self.head[i].find("chunked"):
							#print "CHUNKED"
							self.state = step.HEX0
							self.ignore = 0
			else:
				self.state = step.HEAD0
		elif self.state == step.HEX0:
			if ishex(c):
				#print "C", c
				self.ignore = hextodec(c) + self.ignore * 16
			else:
				# badly assume this character was \r
				self.state = step.HEX2
		elif self.state == step.HEX1:
			if c == '\r':
				self.state = step.HEX2
		elif self.state == step.HEX2:
			if c == '\n':
				#print "chunk done", self.ignore
				if self.ignore <= 0:
					#print "body done"
					return False
				self.state = step.EAT0
		##### ignore everything until we've read self.ignore characters
		elif self.state == step.EAT0:
			self.body = self.body + c
			self.ignore = self.ignore - 1
			if self.ignore <= 1:
				self.ignore = 0
				self.state = step.HEX0
		return True

	def process(self, data):
		#print "parse.process"
		for i in range(0,len(data)):
			if self._process(data[i]) == False:
				return False

	def show(self):
		print "RESP =>", self.response
		print "HEAD =>", self.head
		print "BODY =>"
		print self.body
