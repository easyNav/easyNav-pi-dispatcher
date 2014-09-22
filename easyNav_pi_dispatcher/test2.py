#!/usr/bin/python

from chatroom import Chatroom
import time

sender = Chatroom(5556, 1000)

while (True):
	msg = sender.send(2000, {"hello": "world"})
	time.sleep(0.2)