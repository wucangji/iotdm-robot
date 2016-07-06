#!/usr/bin/env python

import select
import socket
import sys
import Queue

def internal_create(ip,port):
	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	server.setblocking(0)
	server_address = (ip, port)
	server.bind(server_address)
	server.listen(5)
	return server

def internal_close(s):
	try:
		s.shutdown(socket.SHUT.RDWR)
	except:
		pass
		#print "ic:s[0]", s
	try:
		s.close()
	except:
		pass
		#print "ic:c[1]", s

class server:
	def __init__(self, ip="localhost", port=10000, bsize=4096):
		try:
			self.server = internal_create(ip, port)
		except:
			return
		self.header = "HTTP/1.0 %s\r\nServer: iotdm-robot\r\nContent-Length: %d\r\nConnection: close\r\nContent-Type: %s\r\n\r\n%s"
		self.body = "ok"
		self.response = self.header % ("200 OK", len(self.body), "text/plain", self.body)
		self.inputs = [ self.server ]
		self.outputs = []
		self.message_queues = {}
		self.bsize = bsize

	def close(self):
		if hasattr(self, 'inputs'):
			for i in range(0, len(self.inputs)):
				internal_close(self.inputs[i])
		if hasattr(self, 'outputs'):
			for i in range(0, len(self.outputs)):
				internal_close(self.outputs[i])

	# what wait() returns
	# (what,      who,        data)
	# ("timeout", None,       None)
	# ("read",    (ip, port), data)

	def wait(self, secs):
		if not hasattr(self, 'inputs'):
			return ("error", None, None)
		what = None
		who = None
		data = None
		readable, writable, exceptional = select.select(self.inputs, self.outputs, self.inputs, secs)
		if not (readable or writable or exceptional):
			return ("timeout", None, None)

		# handle socket input
		for s in readable:
			if s is self.server:
				# we have a new client
				connection, client_address = s.accept()
				# make non-blocking since we don't know how much to read/recv
				connection.setblocking(0)
				# put this socket in the input list for select
				self.inputs.append(connection)
				
				if True:
					# make a queue for outgoing data
					self.message_queues[connection] = Queue.Queue()
					# put OK response into queue (in this case, it's a full HTTP response)
					self.message_queues[connection].put(self.response)
				else:
					s.send(self.response)

			else:
				# receive data from existing client
				d = s.recv(self.bsize)
				if d:
					# accumulate data
					what = "data"
					if data == None:
						data = d
					else:
						data = data + d
					who = s.getpeername()
					# make sure this socket is in the output array for select
					if s not in self.outputs:
						self.outputs.append(s)
				else:
					# if recv failed, the socket is probably closed, so clean-up
					if s in self.outputs:
						self.outputs.remove(s)
					self.inputs.remove(s)
					s.close()
					del self.message_queues[s]

		# handle socket output
		for s in writable:
			try:
				# see if there's any queued data present/remaining
				next_msg = self.message_queues[s].get_nowait()
			except Queue.Empty:
				# when the queue is empty, clean-up
				self.outputs.remove(s)
			else:
				# this is where the queue stuff gets sent to client
				s.send(next_msg)

		# handle select "exceptions"
		for s in exceptional:
			# clean-up
			self.inputs.remove(s)
			if s in self.outputs:
				self.outputs.remove(s)
			s.close()
			del self.message_queues[s]

		return (what, who, data)
