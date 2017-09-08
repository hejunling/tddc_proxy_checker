# -*- coding: utf-8 -*-
'''
Created on 2017年9月6日

@author: chenyitao
'''

from tddc.common.models.exception.base import ExceptionModelBase


class ExceptionType(object):

    class ProxyChecker(object):
        CLIENT = 3101
        STORAGE_FAILED = 3301
        STORAGER_EXCEPTION = 3302
        NO_SRC_PROXY = 3601
        CHECKE_FAILED = 3701


class ProxyCheckerClientException(ExceptionModelBase):

    EXCEPTION_TYPE = ExceptionType.ProxyChecker.CLIENT


class ProxyCheckerSrorageFailedException(ExceptionModelBase):

    EXCEPTION_TYPE = ExceptionType.ProxyChecker.STORAGE_FAILED


class ProxyCheckerStoragerException(ExceptionModelBase):

    EXCEPTION_TYPE = ExceptionType.ProxyChecker.STORAGER_EXCEPTION


class ProxyCheckerNoSrcProxyException(ExceptionModelBase):

    EXCEPTION_TYPE = ExceptionType.ProxyChecker.NO_SRC_PROXY


class ProxyCheckerCheckeFailedException(ExceptionModelBase):

    EXCEPTION_TYPE = ExceptionType.ProxyChecker.CHECKE_FAILED
