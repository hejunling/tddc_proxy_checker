# -*- coding: utf-8 -*-
'''
Created on 2017年4月14日

@author: chenyitao
'''

import os
import setproctitle

import gevent.monkey
gevent.monkey.patch_all()

from tddc import WorkerManager
from config import ConfigCenterExtern
from worker.checker import Checker


class ProxyCheckerManager(WorkerManager):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        super(ProxyCheckerManager, self).__init__()
        self.info('Proxy Checker Is Starting')
        self._checker = Checker()
        self.info('Proxy Checker Was Ready.')

    @staticmethod
    def start():
        if os.path.exists('./worker.log'):
            os.remove('./worker.log')
        ConfigCenterExtern()
        ProxyCheckerManager()
        while True:
            gevent.sleep(100)


def main():
    worker_type = 1
    worker_tables = {1: 'proxy_source_updater',
                     2: 'proxy_checker'}
    setproctitle.setproctitle(worker_tables[worker_type])
    if worker_type == 1:
        from worker.proxies_source_updater import ProxySourceUpdater
        ProxySourceUpdater().start()
    elif worker_type == 2:
        ProxyCheckerManager.start()


if __name__ == '__main__':
    main()
