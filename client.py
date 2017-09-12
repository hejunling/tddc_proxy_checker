# -*- coding: utf-8 -*-
'''
Created on 2017年4月14日

@author: chenyitao
'''

import gevent.monkey
gevent.monkey.patch_all()
import os
os.remove('./worker.log')

from tddc.base import WorkerManager
from proxy_checker_site import ProxyCheckerSite
from tddc.common import TDDCLogging
from worker.proxy import ProxyManager
from worker.checker import Checker


class ProxyCheckerManager(WorkerManager):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        TDDCLogging.info('->Proxy Checker Is Starting')
        super(ProxyCheckerManager, self).__init__(ProxyCheckerSite)
        self._checker = Checker()
        self._proxy_manager = ProxyManager()
        TDDCLogging.info('->Proxy Checker Was Ready.')
    
    @staticmethod
    def start():
        ProxyCheckerManager()
        while True:
            gevent.sleep(15)


def main():
    if ProxyCheckerSite.WORKER_TYPE == 0:
        from worker.src_proxies_updater import ProxySourceUpdater
        ProxySourceUpdater().start()
    elif ProxyCheckerSite.WORKER_TYPE == 1:
        ProxyCheckerManager.start()

if __name__ == '__main__':
    main()
