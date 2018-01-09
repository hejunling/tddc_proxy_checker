# -*- coding: utf-8 -*-
"""
Created on 2017年8月31日

@author: chenyitao
"""

from tddc import WorkerConfigCenter


class ConfigCenterExtern(WorkerConfigCenter):

    @staticmethod
    def tables():
        return dict(WorkerConfigCenter.tables(),
                    **{'proxies': {'source_key': {'field_type': 'TEXT'},
                                   'pool_key': {'field_type': 'TEXT'},
                                   'source': {'field_type': 'TEXT'},
                                   'concurrent': {'field_type': 'INTEGER'}},
                       'adsl': {'host': {'field_type': 'TEXT'},
                                'port': {'field_type': 'INTEGER'},
                                'username': {'field_type': 'TEXT'},
                                'password': {'field_type': 'INTEGER'}}})

    def get_adsl(self):
        return self._get_info('adsl')

    def get_proxies(self):
        return self._get_info('proxies')
