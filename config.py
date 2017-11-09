# -*- coding: utf-8 -*-
"""
Created on 2017年8月31日

@author: chenyitao
"""

from tddc import ConfigCenter


class ConfigCenterExtern(ConfigCenter):

    @staticmethod
    def tables():
        return dict(ConfigCenter.tables(),
                    **{'proxies': {'source_key': 'TEXT',
                                   'pool_key': 'TEXT',
                                   'source': 'TEXT',
                                   'concurrent': 'INTEGER'}})

    def get_proxies(self):
        return self._get_info('proxies')
