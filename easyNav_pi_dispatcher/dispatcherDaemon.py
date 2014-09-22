#!/usr/bin/python
# -*- coding: utf-8 -*-

# This file is part of easyNav-pi-dispatcher.
# https://github.com/easyNav/easyNav-pi-dispatcher

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2014 Joel Tong me@joeltong.org

import zmq
import time
import json
import logging


class DispatcherDaemon:
	"""The DispatcherDaemon is an interprocess standalone daemon for 
	easyNav.
	"""

	def __init__(self, port=9000):
		"""Initialize the daemon.
		@type port: int 
		@param port: The port to initialize daemon on.

		@return: None
		"""
		self.PORT = port
		## Private vars
		self._socketOut = {}
		self._socketIn = None

		self.setupRep()


	def start(self):
		""" Starts the daemon, as an indefinite process.

		@return: None
		"""
		while(True):
			self.tick()
		pass


	def setupRep(self):
		"""Sets up response socket.  Do not call externally!!

		@return: None
		"""
		context = zmq.Context()
		self._socketIn = context.socket(zmq.REP)
		self._socketIn.bind('tcp://127.0.0.1:%s' % int(self.PORT))
		pass


	def tick(self):
		"""tick function, called when running daemon.  Do not call externally!!
		"""
		try:
			newData = self._socketIn.recv (flags=zmq.NOBLOCK)
			if (newData):
				## Send ACK signal, to avoid response pending
				self._socketIn.send('ACK')
				self.processData(newData)

		## Socket is not ready
		except zmq.ZMQError as e:
			pass

		time.sleep(0.1)


	def pushNewSocket(self, port):
		"""When dispatcherClient#register is called, this is executed.

		Do not call externally!
		@type port: int 
		@param port: The new port to push to list

		@return: None
		"""
		context = zmq.Context()
		sock = context.socket(zmq.PUB)

		if port in self._socketOut.keys():
			self._socketOut[port].close() 
			time.sleep(0.01)
		sock.bind("tcp://*:%d" % int(port))
		self._socketOut[port] = sock
		logging.debug('Socket connected, len: %s' % len(self._socketOut))


	def sendSocket(self, port, payload):
		"""Forwards payload information to socket concerned, when told by a client.
		Do not call externally!

		@type port: int 
		@param port: The port to forward information to. 
		@type payload: JSON
		@param payload: A JSON object containing payload data.
		"""
		try:
			sock = self._socketOut[port]
			sock.send(json.dumps(payload))
			logging.debug('Sent payload: %s' % json.dumps(payload))
		except KeyError, e:
			logging.error('I tried to send payload but failed. TO: %s' % port)
		finally:
			pass


	def processData(self, data=''):
		"""Process data from socket, when message is received.  Do not call externally!!

		@type data: str
		@param data: Data to process
		"""
		dataJson = json.loads(data)

		if dataJson.get('opr') == 'register':
			self.pushNewSocket(dataJson.get('port'))

		elif dataJson.get('opr') == 'send':
			self.sendSocket(dataJson.get('to'), dataJson)
			pass




######################################################
## This is the main function, to show example code.
######################################################


if __name__ == '__main__':
	def configLogging():
		logging.getLogger('').handlers = []

		logging.basicConfig(
		    # filename = "a.log",
		    # filemode="w",
		    level = logging.DEBUG)

	configLogging()
	daemon = DispatcherDaemon()
	daemon.start()
