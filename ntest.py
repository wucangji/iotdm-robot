#!/usr/bin/env python

import nserver
import nparser
import time

n = nserver.server("localhost", 20000)
if n == None:
	print "can't create server"
	exit()

buffer = ""
timeout = 10
mark = time.time() + timeout
newtimeout = timeout

p = nparser.parse()

more = True
	
while True:
	now = time.time()
	if now > mark:
		break
	newtimeout = mark - now
	print "newtimeout", newtimeout
	(what, who, data) = n.wait(newtimeout)
	if what == "error":
		break
	#print what, who, data
	if what == "data":
		buffer = buffer + data
		more = p.process(data)
	if what == "timeout":
		print "timeout"
		break
	if more == False:
		p.show()
		#print "buffer => {"
		#print buffer
		#print "}"
		p.clean()
		break

n.close()
