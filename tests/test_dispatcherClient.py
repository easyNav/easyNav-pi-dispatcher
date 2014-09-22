#!/usr/bin/python
# -*- coding: utf-8 -*-

# This file is part of easyNav-pi-dispatcher.
# https://github.com/easyNav/easyNav-pi-dispatcher

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2014 Joel Tong me@joeltong.org

## PLEASE ENSURE DAEMON IS RUNNING BEFORE RUNNING TEST CASE

from preggy import expect
from tests.base import TestCase

import logging
import smokesignal
import time

from easyNav_pi_dispatcher import DispatcherClient

class DaemonTestCase(TestCase):

    def test_generic(self):
		## Event handler.  Note the use of smokesignal label.
		@smokesignal.on('update')
		def doSomething(args):
			"""This is an event callback.  Payload data is passed 
			as args, and is a JSON object
			"""
			logging.info('Event triggered: Update!')
			logging.info('JSON output: %s' % args)


		@smokesignal.on('fun event')
		def doSomething(args):
			"""This is an event callback.  Payload data is passed 
			as args, and is a JSON object
			"""
			logging.info('Event triggered: A fun event!')
			logging.info('JSON output: %s' % args)


		## Create two clients.  One at 9001, the other 9002
		client1 = DispatcherClient(port=9001)
		client2 = DispatcherClient(port=9002)

		client1.start()
		client2.start()

		client1.send(9002, 'update', {"hello" : "world"})
		client1.send(9002, 'update', {"something" : "here"})
		client1.send(9002, 'fun event', {"count" : "counting numbers"})


		logging.info('finished sending.')

		## Keep clients alive for 5 seconds.  Note how both are unaffected by block.
		time.sleep(5)

		client1.stop()
		client2.stop()
		logging.info('Ended.  Goodbye!')
		pass
