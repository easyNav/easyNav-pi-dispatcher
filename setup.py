#!/usr/bin/python
# -*- coding: utf-8 -*-

# This file is part of easyNav-pi-dispatcher.
# https://github.com/easyNav/easyNav-pi-dispatcher

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2014 Joel Tong me@joeltong.org


from setuptools import setup, find_packages
from easyNav_pi_dispatcher import __version__, dispatcherClient, dispatcherDaemon

tests_require = [
    'mock',
    'nose',
    'coverage',
    'yanc',
    'preggy',
    'tox',
    'ipdb',
    'coveralls',
    'sphinx',
]

setup(
    name='easyNav-pi-dispatcher',
    version=__version__,
    description='Dispatcher daemon, and listener module, for inter-process ',
    long_description='''
Dispatcher daemon, and listener module, for inter-process 
''',
    keywords='easyNav pi navigation inter-process communication',
    author='Joel Tong',
    author_email='me@joeltong.org',
    url='https://github.com/easyNav/easyNav-pi-dispatcher',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: Unix',
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: Implementation :: PyPy",
        'Operating System :: OS Independent',
    ],
    packages=find_packages(),
    include_package_data=False,
    install_requires=[
        # add your dependencies here
        # remember to use 'package-name>=x.y.z,<x.y+1.0' notation (this way you get bugfixes)
        'smokesignal>=0.5',
        'pyzmq>=14.3.1'
    ],
    extras_require={
        'tests': tests_require,
    },
    entry_points={
        'console_scripts': [
            # add cli scripts here in this form:
            # 'easyNav-pi-dispatcher=easyNav_pi_dispatcher.cli:main',
            'easyNav-pi-dispatcher=easyNav_pi_dispatcher.dispatcherDaemon:main'
        ],
    },
)
