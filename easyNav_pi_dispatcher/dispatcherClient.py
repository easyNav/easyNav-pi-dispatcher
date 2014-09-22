#!/usr/bin/python
# -*- coding: utf-8 -*-

# This file is part of easyNav-pi-dispatcher.
# https://github.com/easyNav/easyNav-pi-dispatcher

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2014 Joel Tong me@joeltong.org

import zmq
import time
import logging
import json
import threading
import smokesignal


class DispatcherClient:
	"""The Event Dispatcher client is an inter-process communications module
	for easyNav.  It utilizies the TCP/IP layer to send event-triggered messages. 

	The client can be embedded in your code, and is non-blocking.

	Please run the Event Dispatcher Server before using the client. 

	Examples are given in the #main function below.

	"""

	def __init__(self, daemonPort=9000, port=1):
		"""Initializes the client. 

		@type daemonPort: int
		@param daemonPort: The port number of Dispatcher Daemon to use. 
		@type port: int 
		@param port: The port identification number, of the client being created.

		@return: None

		"""
		self.DAEMON_PORT = int(daemonPort)
		self.PORT = int(port)

		self._socketOut = None
		self._socketIn = None

		self._active = False
		self._threadListen = None


	def start(self):
		"""Starts the client daemon.  Note that this does not block!

		@return: None
		"""
		self.register()
		self.setupSocketIn()
		self._active = True

		def runThread():
			while(self._active):
				self.listen()
				time.sleep(0.01)

		self._threadListen = threading.Thread(target=runThread)
		self._threadListen.start()


	def stop(self):
		"""Stops the client daemon.

		@return: None
		"""
		self._active = False
		self._threadListen.join()


	def send(self, toPort, event='NORMAL', payload={}):
		"""Sends data to another process, given by a port ID 

		@type toPort: int 
		@param toPort: The Port ID to send to. 
		@type payload: JSON 
		@param payload: A proper JSON object (not a string!) containing data to send.

		@return: None
		"""
		# socketOut.send("%d %s" % (self.DAEMON_TOPIC, json.dumps(payload)))
		payload = {
			'opr': 'send',
			'from': self.PORT,
			'to': toPort,
			'event': event,
			'payload': json.dumps(payload)
		}
		self._socketOut.send(json.dumps(payload))
		## Pend until ACK signal is received
		self._socketOut.recv()


	def register(self):
		"""Attempts to register the client on the daemon.  Do not call externally!!
		"""
		context = zmq.Context()
		self._socketOut = context.socket(zmq.REQ)
		self._socketOut.connect('tcp://127.0.0.1:%s' % self.DAEMON_PORT)
		time.sleep(0.01)			## Needed for socket initialization
		payload = {
			'opr': 'register',
			'port': self.PORT
		}
		logging.debug('socket initiated')
		self._socketOut.send(json.dumps(payload))
		## Pend until ACK signal is received
		# TODO: Insert acknowledgement signal here
		self._socketOut.recv()


	def setupSocketIn(self):
		"""Sets up socket that receives information from daemon.  Do not call
		externally!
		"""
		context = zmq.Context()
		socket = context.socket(zmq.SUB)
		socket.setsockopt(zmq.SUBSCRIBE, '')
		socket.connect ("tcp://localhost:%s" % self.PORT)
		self._socketIn = socket
		time.sleep(0.01)			## Needed for socket initialization
		logging.debug('listening at %s' % self.PORT)
		pass


	def listen(self):
		"""Listener for new socket mail from daemon.  Do not call externally!!
		"""
		try:
			data = self._socketIn.recv(flags=zmq.NOBLOCK)
			if (data):
				logging.debug('I received data %s' % data)
				dataJson = json.loads(data)
				smokesignal.emit(dataJson.get('event'), dataJson)

		## Socket is not ready
		except zmq.ZMQError as e:
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

	@smokesignal.on('update')
	def doSomething(args):
		"""This is an event callback.  Payload data is passed 
		as args, and is a JSON object
		"""
		logging.info('Event triggered: Update!')
		logging.info(args)

	## Create client with port 9001, and daemon at default 9000.
	client = DispatcherClient(port=9001)
	client.start()
	time.sleep(1)
	client.send(9001, 'update', {"hello" : "world"})
	## Keep client alive for 2 seconds.
	time.sleep(2) 			
	client.stop()
