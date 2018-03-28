# -*- coding: utf-8 -*-
"""
Created on 2017年8月31日

@author: chenyitao
"""
from sqlalchemy import Column, Integer, String

from tddc import Base, engine


class ProxyModel(Base):
    __tablename__ = 'proxy_info'

    id = Column(Integer, primary_key=True)
    source_key = Column(String(32))
    pool_key = Column(String(32))
    source = Column(String(1024))
    concurrent = Column(Integer)


class ADSLModel(Base):
    __tablename__ = 'adsl_info'

    id = Column(Integer, primary_key=True)
    host = Column(String(32))
    port = Column(Integer)
    username = Column(String(32))
    passwd = Column(String(32))


Base.metadata.create_all(engine)
