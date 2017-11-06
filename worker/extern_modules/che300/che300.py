# -*- coding: utf-8 -*-
'''
Created on 2017年4月17日

@author: chenyitao
'''

import requests
from lxml import html


class Che300ProxyChecker(object):
    '''
    classdocs
    '''
    
    platform = 'che300'
    
    feature = 'che300.che300'
    
    proxy_type = 'http'
    
    check_page = 'http://www.che300.com/buycar?from=bd_seo&city=0'

    def __init__(self, info):
        '''
        Constructor
        '''
        self._info = info
        self.useful = False
        proxies = {'http': info.ip_port}
        headers = {'User-Agent': ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) '
                                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                                  'Chrome/56.0.2924.87 Safari/537.36'),
                   'X-Forwarded-For': proxies['http'],
                   'X-Real-IP': proxies['http'],
                   'HTTP_CLIENT_IP': proxies['http'],
                   'HTTP_X_FORWARD_FOR': proxies['http']}
        try:
            rsp = requests.get(self.check_page, proxies=proxies, timeout=5, headers=headers)
        except Exception, e:
            pass
        else:
            if rsp.status_code != 200:
                return
            try:
                doc = html.document_fromstring(rsp.text)
            except:
                pass
            else:
                ret = doc.xpath('//*[@class="list-item"]/a/@href')
                if len(ret):
                    self.useful = True
