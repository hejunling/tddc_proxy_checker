# -*- coding: utf-8 -*-
'''
Created on 2017年4月17日

@author: chenyitao
'''

import requests
from lxml import html
from tddc import ExternBase


class LagouProxyChecker(ExternBase):
    '''
    classdocs
    '''

    platform = 'lagou'

    feature = 'lagou.lagou'

    version = '12312312'

    proxy_type = 'http'

    check_page = 'https://www.lagou.com/'

    def __init__(self, proxy):
        '''
        Constructor
        '''
        super(LagouProxyChecker, self).__init__()
        self.proxy = proxy
        self.useful = False
        proxies = {'https': proxy}
        headers = {'User-Agent': ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) '
                                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                                  'Chrome/56.0.2924.87 Safari/537.36'),
                   'X-Forwarded-For': proxies['https']}
        try:
            rsp = requests.get(self.check_page, proxies=proxies, timeout=5, headers=headers)
        except:
            pass
        else:
            if rsp.status_code != 200:
                return
            try:
                doc = html.document_fromstring(rsp.text)
            except:
                pass
            else:
                ret = doc.xpath('//*[@class="lg_tnav_wrap"]')
                if len(ret):
                    self.useful = True
