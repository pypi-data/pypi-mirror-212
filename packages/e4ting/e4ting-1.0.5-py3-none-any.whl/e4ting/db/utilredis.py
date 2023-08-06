#!/bin/env python3
# -*- coding:utf-8 -*-
"""
    [模块名]
    Add By :antiy yuhai@antiy.cn 2023-05-18 14:34:21
"""
from redis import Redis
from e4ting import util
# from e4ting.etc import MyRds

# r = MyRds()

class RedisDB:
    def __init__(self, db, ip="", port=6379):
        self.ip = ip
        self.port = int(port)
        self.db = db
        self.r = Redis(host=self.ip, port=self.port, db=self.db)

    @util.redef_return(ret=None)
    def set(self, key, msg):
        return self.r.set(key, msg)

    @util.redef_return(ret=False)
    def delete(self, key):
        return self.r.delete(key)

    @util.redef_return(ret=None)
    def get(self, key):
        return self.r.get(key)

    @util.redef_return(ret=None)
    def hget(self,key, data):
        return self.r.hget(key, data)

    @util.redef_return(ret=False)
    def sadd(self,key, data):
        return self.r.sadd(key, data)

    @util.redef_return(ret=False)
    def sismember(self,key, data):
        return self.r.sismember(key, data)
    
