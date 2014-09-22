#!/usr/bin/python

from chatroom import Chatroom
import time

receiver = Chatroom(5556, 2000)

while (True):
	msg = receiver.getMessage()
	time.sleep(0.2)