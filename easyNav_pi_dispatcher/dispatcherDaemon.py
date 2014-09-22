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

	def __init__(self, port=9000):
		# super(DispatcherDaemon, self).__init__()

		self.PORT = port

		## Private vars
		self._socketOut = {}
		self._socketIn = None

		self.setupRep()
		self.setupSend()


	def start(self):
	    while(True):
	    	self.tick()
		pass


	def setupRep(self):
		context = zmq.Context()
		self._socketIn = context.socket(zmq.REP)
		self._socketIn.bind('tcp://127.0.0.1:%s' % int(self.PORT))
		# print 'setup here'
		# self._socketIn.setsockopt(zmq.SUBSCRIBE, "")
		pass


	def setupSend(self):
		pass


	def tick(self):
		try:
			newData = self._socketIn.recv (flags=zmq.NOBLOCK)
			if (newData):
				print newData
				self._socketIn.send('Echo: received')
				self.processData(newData)
			pass

		## Socket is not ready
		except zmq.ZMQError as e:
			pass

		time.sleep(0.2)


	def pushNewSocket(self, port):
		context = zmq.Context()
		sock = context.socket(zmq.PUB)

		if port in self._socketOut.keys():
			self._socketOut[port].close() 
			time.sleep(0.01)
		sock.bind("tcp://*:%d" % int(port))
		self._socketOut[port] = sock
		logging.debug('Socket connected, len: %s' % len(self._socketOut))


	def sendSocket(self, port, payload):
		logging.info('sending')
		try:
			sock = self._socketOut[port]
			sock.send(json.dumps(payload))
			logging.info('Sent payload: %s' % json.dumps(payload))
		except KeyError, e:
			logging.error('I tried to send payload but failed. TO: %s' % port)
		finally:
			pass


	def processData(self, data=''):
		dataJson = json.loads(data)

		if dataJson.get('opr') == 'register':
			self.pushNewSocket(dataJson.get('port'))

		elif dataJson.get('opr') == 'send':
			self.sendSocket(dataJson.get('to'), dataJson)
			pass

		## Send ACK signal, to prevent pending
		self._socketIn.send('ACK')





	def stop(self):
		# self._socketIn.close()
		pass


def configLogging():
	logging.getLogger('').handlers = []

	logging.basicConfig(
	    # filename = "a.log",
	    # filemode="w",
	    level = logging.DEBUG)


if __name__ == '__main__':
	configLogging()
	daemon = DispatcherDaemon()
	daemon.start()
