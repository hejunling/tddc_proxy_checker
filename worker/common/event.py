# -*- coding: utf-8 -*-
'''
Created on 2017年9月6日

@author: chenyitao
'''

from tddc.common.models.events_model.event_base import EventBase


class EventType(object):

    NONE = None

    class ProxyChecker(object):
    
        BASE_DATA = 3001
 
        MODULE = 3002
        
        SOURCE = 3003


class ProxyCheckerModuleEvent(EventBase):

    event_type = EventType.ProxyChecker.MODULE


class ProxyCheckerSourceAPIEvent(EventBase):

    event_type = EventType.ProxyChecker.SOURCE
