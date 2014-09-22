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

	def __init__(self, daemonPort=9000, port=1):
		# super(DispatcherDaemon, self).__init__()

		self.DAEMON_PORT = int(daemonPort)
		self.PORT = int(port)

		self._socketOut = None
		self._socketIn = None

		self._active = False
		self._threadListen = None


	def start(self):
		"""Starts the client daemon. 
		"""
		self.register()
		self.setupSocketIn()
		print 'here'
		self._active = True
		self._threadListen = threading.Thread(target=self.runThread)
		self._threadListen.start()


	def stop(self):
		"""Stops the client daemon. 
		"""
		self._active = False
		self._threadListen.join()



	def runThread(self):
		while(self._active):
			self.listen()
			time.sleep(0.01)


	def register(self):
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
		context = zmq.Context()
		socket = context.socket(zmq.SUB)
		socket.setsockopt(zmq.SUBSCRIBE, '')
		socket.connect ("tcp://localhost:%s" % self.PORT)
		self._socketIn = socket
		time.sleep(0.01)			## Needed for socket initialization
		logging.debug('listening at %s' % self.PORT)
		pass


	def send(self, toPort, event='NORMAL', payload={}):
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


	def listen(self):
		try:
			data = self._socketIn.recv(flags=zmq.NOBLOCK)
			if (data):
				logging.debug('I received data %s' % data)
				dataJson = json.loads(data)
				smokesignal.emit(dataJson.get('event'), dataJson)

		## Socket is not ready
		except zmq.ZMQError as e:
			pass








def configLogging():
	logging.getLogger('').handlers = []

	logging.basicConfig(
	    # filename = "a.log",
	    # filemode="w",
	    level = logging.DEBUG)


if __name__ == '__main__':

	@smokesignal.on('update')
	def doSomething(args):
		logging.info('Event triggered: Update!')
		logging.info(args)

	configLogging()
	client = DispatcherClient(port=9001)
	client.start()
	time.sleep(1)
	client.send(9001, 'update', {"hello" : "world"})
	time.sleep(2)
	client.stop()
