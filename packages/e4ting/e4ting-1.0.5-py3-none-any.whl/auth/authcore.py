#!/usr/bin/python
# -*- coding: utf-8 -*-

import os,sys
import json
import time
import random
import contextlib

from binascii import crc32
from pdb import set_trace as strace
from traceback  import format_exc as dumpstack

from common.mongo import (
        db_users,
        db_requests,
        db_login_record,
        db_data_token
    )
from common.utilredis import create_token_id,save_token,salt,default_status,default_role,key_

from jose import jwe
from flask         import redirect,request

from common import util

def alloc_key(salt="e4ting"):
    return util.baseconvert(util.md5(salt).upper(), 16, 94).zfill(16)[:16]

__key__ = alloc_key()
__timeout__ = 30 * 24 * 60 * 60
util.log(__key__)

def to_jwe(data):
    # key = alloc_key()
    ret = jwe.encrypt(json.dumps(data), __key__, algorithm='dir', encryption='A128GCM')
    return ret

def alloc_token(data):
    payload = {
          # "name": "dawsonenjoy",
          "now" : util.now(),
          "exp" : time.time() + __timeout__,   # 有效期7天
        }
    data.update(payload)
    token = to_jwe(data)
    return token.decode()

encode = alloc_token

def decode(token):
    return json.loads(jwe.decrypt(token, __key__).decode())

def password_encode(passwd):
    return util.md5(passwd + salt())

def check_passwd(user, passwd):
    if user not in db_users:
        util.log("用户不存在 {}".format(user))
        return False
    return util.md5(passwd + salt()) == db_users[user]["password"]

@contextlib.contextmanager
def check_and_set_code(code):

    key = key_("api", "acl", "login", "luosimao", code)
    ret = key in redis_temp_running
    data = {"ret" : ret}
    # if ret:
    #     ret = redis_temp_running[key].get(self.bindid, False)
    # 判断是否已验证过
    yield data

    if data["ret"] and ret == False:
        redis_temp_running.expire(key, 10 * 60)
    # 用一个字典来保存，以防接口被爆破， 暂时不做防护处理
    # if not self.bindid:
    #     return
    # redis_temp_running.add(key, self.bindid)
    # if not ret:
    #     redis_temp_running.expire(key, 10 * 60)

def check_input_avaliable(string):
    return True

def check_user_exists(user):
    return user in db_users

def create_user(user, passwd, ip="", code=""):
    db_users[user] = {
                        "user"  : user,
                        "password": password_encode(passwd),
                        "ip"      : ip,
                        "create_time": util.now(),
                        # "headimg" : "/img/{}.jpg".format(random.randint(1, 6)),
                        "status"  : default_status(),
                        "role"  : default_role(),
                    }
    return True


def check_code(code):

    # 留个自用code
    if code == "e4ting":
        return True
    refer = request.headers.get("Referer", "")

    if "e4ting.cn" in refer:
        api_key = "bf4db134f59c40436440163a013b643a"
    elif "e4ting.top" in refer:
        api_key = "c32a81c2b6437cd52074a4f9e18c1a55"
    else:
        util.log("不支持此站点 {} 做验证码校验".format(refer))
        return False

    with check_and_set_code(code) as result:
        if not result:
            url = "https://captcha.luosimao.com/api/site_verify"
            data = {
                # c32a81c2b6437cd52074a4f9e18c1a55
                "api_key": api_key,
                "response" : code,
            }
            ret = util.HTTP().post(url, data=data, headers={"Content-Type":"application/x-www-form-urlencoded"})
            util.log(ret)
            if ret["error"] != 0:
                # 验证失败，直接return  不记录redis
                ret = False
        ret = True
    return ret

class Token():
    def __init__(self, data=None, token=None):
        self.data = data
        self.token = token
        self.key = __key__

        self.result = None

    def encode(self):
        self._id = create_token_id()
        self.data = dict(self.data, _id=self._id)
        token = encode(self.data)
        self.data = dict(self.data, token=token)
        return token

    def save(self):
        self.dump_to_redis()
        self.save_to_db()

    def dump_to_redis(self):
        save_token(self.data, __timeout__)

    def save_to_db(self):
        _id = self.data["_id"]
        data = dict(self.data)
        del data["_id"]
        db_data_token[_id] = data

    def decode(self):
        self.result = decode(self.token)
        return self.result

    def is_expire(self):
        if not self.result:
            self.decode()
        return self.result["exp"] <= time.time()
        # {'now': '2021-07-18 15:40:48', 'exp': 1629186048.9487908, 'name': 'test'}

def auth_info():
    string = request.headers.get("Authorization", None)
    if not string:
        return False,{}
    try:
        token = Token(token=string)
        info = token.decode()
        ret  = token.is_expire()
    except:
        util.log(dumpstack())
        return False,{}
    return not ret,info


