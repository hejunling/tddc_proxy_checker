# -*- coding: utf-8 -*-
'''
Created on 2017年4月17日

@author: chenyitao
'''

import gevent.monkey
import gevent.pool

from worker.fetch_ip_form_vps import FetchIPFromVPS

gevent.monkey.patch_all()

import requests
import socket
import json
import setproctitle

from tddc import TDDCLogger, CacheManager

from config import ConfigCenterExtern


class ProxySourceUpdater(TDDCLogger):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        super(ProxySourceUpdater, self).__init__()
        self.proxy_conf = ConfigCenterExtern().get_proxies()
        self.info('[TDDC_PROXY_SOURCE_UPDATER] Proxy Source Updater Is Starting.')
        self._src_apis = [{'platform': 'kuaidaili',
                           'api': ('http://dev.kuaidaili.com/api/getproxy/'
                                   '?orderid=999310215091675&num=100&'
                                   'b_pcchrome=1&b_pcie=1&b_pcff=1&'
                                   'protocol=1&method=1&an_an=1&'
                                   'an_ha=1&sp1=1&sp2=1&sp3=1&f_pr=1'
                                   '&format=json&sep=1'),
                           'parse_mould': self._parse_kuaidaili}]
        adsl = ConfigCenterExtern().get_adsl()
        self.adsl_server = FetchIPFromVPS(adsl.host, adsl.port, adsl.username, adsl.password)
        self.adsl_proxy = self._get_adsl_proxy()
        self.switching = False
        self.info('->[TDDC_PROXY_SOURCE_UPDATER] Proxy Source Updater Was Started.')

    def start(self):
        cnt = 0
        while True:
            if cnt % 3 == 0:
                gevent.spawn(self._update_adsl)
                gevent.sleep()
            elif cnt % 10 == 0:
                gevent.spawn(self._update_src)
                gevent.sleep()
            gevent.sleep(1)
            cnt += 1

    def _update_adsl(self):
        proxy = CacheManager().get_random('tddc:proxy:adsl', False)
        if proxy or self.switching:
            return
        self.switching = True
        try:
            self.adsl_proxy = self._redial_adsl_proxy()
            if self.adsl_proxy:
                self.info('ADSL Proxy(%s) Was Updated.' % self.adsl_proxy)
        except Exception as e:
            self.warning(e.message)
        self.switching = False

    def _get_adsl_proxy(self):
        while True:
            try:
                ip = self.adsl_server.get_ip()
            except Exception as e:
                self.warning(e.message)
            else:
                proxy = '%s:52460' % ip
                CacheManager().set('tddc:proxy:adsl', proxy)
                return proxy

    def _redial_adsl_proxy(self):
        while True:
            try:
                ip = self.adsl_server.redial()
            except Exception as e:
                self.warning(e.message)
            else:
                if not ip:
                    continue
                proxy = '%s:52460' % ip
                CacheManager().set('tddc:proxy:adsl', proxy)
                return proxy

    def _update_src(self):
        for info in self._src_apis:
            try:
                platform = info.get('platform')
                api = info.get('api')
                parse_mould = info.get('parse_mould')
                rsp = requests.get(api)
                if not rsp:
                    self.error('Exception(%s): ' % platform + api)
                    continue
                if not parse_mould:
                    self.error('Exception: parse_mould is None.')
                    continue
                all_ips = parse_mould(rsp.text)
                http_ips = self._proxy_active_check(all_ips.get('HTTP', []))
                CacheManager().smadd('%s:http' % self.proxy_conf.source_key, http_ips)
                self.info('Proxies To HTTP Was Growth：%d' % len(http_ips))
                https_ips = self._proxy_active_check(all_ips.get('HTTPS', []))
                CacheManager().smadd('%s:https' % self.proxy_conf.source_key, https_ips)
                CacheManager().smadd('%s:http' % self.proxy_conf.source_key, https_ips)
                self.info('Proxies To HTTPS Was Growth：%d' % len(https_ips))
            except Exception as e:
                self.error('Exception[IP_SOURCE]:')
                self.exception(e)

    @staticmethod
    def _proxy_active_check(ips):
        active_ips = []

        def _checker(ip):
            try:
                _ip, _port = ip.split(':')
                _s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                _s.settimeout(5)
                _s.connect((_ip, int(_port)))
                _s.close()
            except:
                pass
            else:
                active_ips.append(ip)

        p = gevent.pool.Pool(16)
        p.map(_checker, ips)
        p.join()
        return active_ips

    def _parse_kuaidaili(self, data):
        proxies = {'HTTP': [], 'HTTPS': []}
        infos = json.loads(data)
        if infos.get('code'):
            return proxies
        proxy_list = infos.get('data').get('proxy_list', [])
        for proxy_info in proxy_list:
            proxy, proxy_type = proxy_info.split(',')
            proxies[proxy_type].append(proxy)
        return proxies


def main():
    setproctitle.setproctitle('proxy_source_updater')
    ProxySourceUpdater().start()


if __name__ == '__main__':
    main()
