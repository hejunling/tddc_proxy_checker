# -*- coding: utf-8 -*-
'''
Created on 2017年4月17日

@author: chenyitao
'''

import requests
from lxml import html
from tddc import ExternBase


class Che300ProxyChecker(ExternBase):
    '''
    classdocs
    '''
    
    platform = 'che300'
    
    feature = 'che300.che300'

    version = '123123123'
    
    proxy_type = 'http'
    
    check_page = 'https://www.che300.com/buycar?from=bd_seo&city=0'

    def __init__(self, proxy):
        '''
        Constructor
        '''
        super(Che300ProxyChecker, self).__init__()
        self.proxy = proxy
        self.useful = False
        proxies = {'http': proxy}
        headers = {'User-Agent': ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) '
                                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                                  'Chrome/56.0.2924.87 Safari/537.36'),
                   'X-Forwarded-For': proxies['http']}
        try:
            rsp = requests.get(self.check_page, proxies=proxies, timeout=5, headers=headers)
        except Exception as e:
            pass
        else:
            if rsp.status_code != 200:
                return
            try:
                doc = html.document_fromstring(rsp.text)
            except Exception as e:
                pass
            else:
                ret = doc.xpath('//*[@class="list-item"]/a/@href')
                if len(ret):
                    self.useful = True
