# -*- coding: utf-8 -*-
'''
Created on 2017年4月17日

@author: chenyitao
'''

import requests
from lxml import html
from tddc import ExternBase


class CheokProxyChecker(ExternBase):
    '''
    classdocs
    '''
    
    platform = 'cheok'
    
    feature = 'cheok.cheok'

    version = '12312312'
    
    proxy_type = 'http'
    
    check_page = 'http://www.cheok.com/'

    def __init__(self, proxy):
        '''
        Constructor
        '''
        super(CheokProxyChecker, self).__init__()
        self.proxy = proxy
        self.useful = False
        proxies = {'http': 'http://{}'.format(proxy),
                   'https': 'https://{}'.format(proxy)}
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
            except:
                pass
            else:
                ret = doc.xpath('//*[@data-name="index"]')
                if len(ret):
                    self.useful = True
