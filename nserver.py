#!/usr/bin/env python

import select
import socket
import sys
import Queue

def internal_create(ip,port):
	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server.setblocking(0)
	server_address = (ip, port)
	server.bind(server_address)
	server.listen(5)
	return server


class server:
	def __init__(self, ip="localhost", port=10000):
		self.canned_header = "HTTP/1.0 %s\r\nServer: iotdm-robot\r\nContent-Length: %d\r\nConnection: close\r\nContent-Type: %s\r\n\r\n%s"
		self.canned_bare = "ok"
		self.canned_okay = self.canned_header % ("200 OK", len(self.canned_bare), "text/plain", self.canned_bare)

		self.server = internal_create(ip, port)

		self.inputs = [ self.server ]
		self.outputs = []
		self.message_queues = {}

	# (what,who,data)
	# ("timeout", None, None)
	# ("read", (ip, port), data)

	def wait(self, secs):
		what = None
		rdata = None
		rwho = None
		readable, writable, exceptional = select.select(self.inputs, self.outputs, self.inputs, secs)
		if not (readable or writable or exceptional):
			#print >>sys.stderr, 'timed out'
			return ("timeout", None, None)
		for s in readable:
			if s is self.server:
				connection, client_address = s.accept()
				#print >>sys.stderr, 'new connection from', client_address
				connection.setblocking(0)
				self.inputs.append(connection)
				# Give the connection a queue for data we want to send
				self.message_queues[connection] = Queue.Queue()
				# stuff response into queue
				self.message_queues[connection].put(self.canned_okay)
			else:
				data = s.recv(4096)
				if data:
					what = "data"
					if rdata == None:
						rdata = data
					else:
						rdata = rdata + data
					rwho = s.getpeername()
					#print >>sys.stderr, 'received %d bytes from %s' % (len(data), s.getpeername())
					#self.message_queues[s].put(data)
					# Add output channel for response
					if s not in self.outputs:
						self.outputs.append(s)
				else:
					# Interpret empty result as closed connection
					if s in self.outputs:
						self.outputs.remove(s)
					self.inputs.remove(s)
					s.close()
					del self.message_queues[s]

		for s in writable:
			try:
				next_msg = self.message_queues[s].get_nowait()
			except Queue.Empty:
				#print >>sys.stderr, 'output queue for', s.getpeername(), 'is empty'
				self.outputs.remove(s)
			else:
				#print >>sys.stderr, 'sending %d bytes to %s' % (len(next_msg), s.getpeername())
				s.send(next_msg)

		# Handle "exceptional conditions"
		for s in exceptional:
			# Stop listening for input on the connection
			self.inputs.remove(s)
			if s in self.outputs:
				self.outputs.remove(s)
			s.close()

			# Remove message queue
			del self.message_queues[s]

		return (what, rwho, rdata)

#while inputs:
#	print "::", wait(30)
