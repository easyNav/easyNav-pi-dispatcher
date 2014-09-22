#!/usr/bin/python
# -*- coding: utf-8 -*-

# This file is part of easyNav-pi-dispatcher.
# https://github.com/easyNav/easyNav-pi-dispatcher

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2014 Joel Tong me@joeltong.org


import logging

logging.getLogger('').handlers = []

logging.basicConfig(
	# filename = "a.log",
	# filemode="w",
	level = logging.INFO)


from easyNav_pi_dispatcher.dispatcherDaemon import DispatcherDaemon
from easyNav_pi_dispatcher.dispatcherClient import DispatcherClient

