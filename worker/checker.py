# -*- coding: utf-8 -*-
'''
Created on 2017年4月17日

@author: chenyitao
'''

import gevent

from tddc import TDDCLogger, CacheManager, ExternManager

from config import ConfigCenterExtern


class Checker(TDDCLogger):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        super(Checker, self).__init__()
        self.info('Checker Is Starting.')
        self.proxy_conf = ConfigCenterExtern().get_proxies()
        self.concurrent = self.proxy_conf.concurrent
        self._init_rules()
        for i in range(self.concurrent):
            gevent.spawn(self._check, i, 'http')
            gevent.sleep()
        for i in range(self.concurrent):
            gevent.spawn(self._check, i, 'https')
            gevent.sleep()
        self.info('Checker Was Started.')

    def _init_rules(self):
        self._rules_moulds = {'http': {}, 'https': {}}
        modules = ExternManager().get_all_modules()
        for platform, _module in modules.items():
            for _, cls in _module.items():
                self._rules_moulds[cls.proxy_type][platform] = cls

    def _check(self, tag, proxy_type):
        cnt = 0
        gevent.sleep(5)
        while True:
            try:
                if not len(self._rules_moulds[proxy_type]):
                    gevent.sleep(10)
                    continue
                proxy = CacheManager().get_random('%s:%s' % (self.proxy_conf.source_key, proxy_type))
                if not proxy:
                    if not cnt % 6 and tag == 1:
                        self.warning('No Proxy(%s).' % proxy_type)
                    cnt += 1
                    gevent.sleep(10)
                    continue
                for platform, cls in self._rules_moulds[proxy_type].items():
                    ret = cls(proxy)
                    if ret.useful:
                        CacheManager().set('%s:%s' % (self.proxy_conf.pool_key, platform),
                                           proxy)
                        self.debug('[%s:%s:%s]' % (proxy_type,
                                                   platform,
                                                   proxy))
            except Exception as e:
                self.exception(e)
