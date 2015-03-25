#!/usr/bin/env python

import nserver

n = nserver.server()

a = ""

while n.inputs:
	(what, who, data) = n.wait(5)
	if what == "data":
		a = a + data
	if what == "timeout":
		break

print a
