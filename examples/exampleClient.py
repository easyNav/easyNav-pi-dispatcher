#!/usr/bin/python
"""Example Script for using client.

In this example, client 9001 sends a message to client 9002.  Different
Events are triggered.
"""

import logging
import smokesignal
import sys

from easyNav_pi_dispatcher import DispatcherClient


## Configuring logging
def configLogging():
	logging.getLogger('').handlers = []

	logging.basicConfig(
	    # filename = "a.log",
	    # filemode="w",
	    level = logging.DEBUG)
configLogging()


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

client.stop()
logging.info('Ended.  Goodbye!')
