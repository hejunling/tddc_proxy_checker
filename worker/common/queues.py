# -*- coding: utf-8 -*-
'''
Created on 2017年9月6日

@author: chenyitao
'''

from gevent.queue import Queue
from tddc.common.queues import PublicQueues


class ProxyCheckerQueues(PublicQueues):
    ## Proxy Checker
    # Useful Proxy Queue
    USEFUL_PROXY = Queue()
    # Source Proxy Queue
    HTTP_SOURCE_PROXY = Queue()
    HTTPS_SOURCE_PROXY = Queue()
