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


class Chatroom:

	def __init__(self, port):
		# super(DispatcherDaemon, self).__init__()
		self.port = int(port)

		self._socketOut = None
		self._socketIn = None

		self.setupSend()
		self.setupRcv()


	def setupSend(self):
		context = zmq.Context()
		self._socketOut = context.socket(zmq.PUB)
		self._socketOut.bind("tcp://*:%s" % self.port)
		time.sleep(0.1) 			## Needed for socket initialization
		logging.debug('socketOut initiated')


	def setupRcv(self):
		context = zmq.Context()
		self._socketIn = context.socket(zmq.SUB)
		self._socketIn.setsockopt(zmq.SUBSCRIBE, str(self.topicSource))


	def send(self, to, payload):
		payload["from"] = self.topicSource
		payload["to"] = to
		self._socketOut.send("%d %s" % (to, json.dumps(payload) ) )
		pass


	def getMessage(self):
		## This should be called every cycle during loop, to avoid multiprocesses.
		try:
			newData = self._socketIn.recv (flags=zmq.NOBLOCK)
			if (newData):
				print newData
				return newData

		## Socket is not ready
		except zmq.ZMQError as e:
			return False

		return False

	def attachEvent(event, callback):
		pass



def configLogging():
	logging.getLogger('').handlers = []

	logging.basicConfig(
	    # filename = "a.log",
	    # filemode="w",
	    level = logging.DEBUG)


if __name__ == '__main__':
	pass
