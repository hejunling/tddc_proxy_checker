# -*- coding: utf-8 -*-
'''
Created on 2017年4月17日

@author: chenyitao
'''
import logging
import gevent

from config import ProxyModel
from tddc import CacheManager, ExternManager, DBSession

log = logging.getLogger(__name__)


class Checker(object):
    '''
    代理更新控制
    '''

    def __init__(self):
        '''
        Constructor
        '''
        super(Checker, self).__init__()
        log.info('Checker Is Starting.')
        self.proxy_conf = DBSession.query(ProxyModel).get(1)
        self.concurrent = self.proxy_conf.concurrent
        self._init_rules()
        for i in range(self.concurrent):
            gevent.spawn(self._check, i, 'http')
            gevent.sleep()
        for i in range(self.concurrent):
            gevent.spawn(self._check, i, 'https')
            gevent.sleep()
        log.info('Checker Was Started.')

    def _init_rules(self):
        """
        初始化需要使用代理的平台检测模块
        """
        self._rules_moulds = {'http': {}, 'https': {}}
        modules = ExternManager().get_all_modules()
        ExternManager().update_success_callback.append(self._init_rules)
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
                        log.warning('No Proxy(%s).' % proxy_type)
                    cnt += 1
                    gevent.sleep(10)
                    continue
                for platform, cls in self._rules_moulds[proxy_type].items():
                    ret = cls(proxy)
                    if ret.useful:
                        CacheManager().set('%s:%s' % (self.proxy_conf.pool_key, platform),
                                           proxy)
                        log.debug('[%s:%s:%s]' % (proxy_type,
                                                  platform,
                                                  proxy))
            except Exception as e:
                log.exception(e)
