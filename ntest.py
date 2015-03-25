#!/usr/bin/env python

import nserver
import nparser
import time

n = nserver.server()
buffer = ""
timeout = 10
mark = time.time() + timeout

p = nparser.parse()

while n.inputs:
	more = True
	newtimeout = timeout
	now = time.time()
	if now > mark:
		break
	newtimeout = mark - now
	#print "newtimeout", newtimeout
	(what, who, data) = n.wait(newtimeout)
	if what == "data":
		buffer = buffer + data
		for i in range(0,len(data)):
			more = p.process(data[i])
			if more == False:
				break
	if what == "timeout":
		print "timeout"
		break
	if more == False:
		p.show()
		print "buffer => {"
		print buffer
		print "}"
		p.clean()
