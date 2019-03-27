#!/usr/bin/env python
# -*- coding:utf8 -*-
"""
	项目工具类
"""

import time
from flask import current_app
from .config import DEFINE_ERRORS


class CustomFlaskErr(Exception):
    # 默认的返回码
    status_code = 400

    # 自己定义了一个 return_code，作为更细颗粒度的错误代码
    def __init__(self, return_code=None, status_code=200, payload=None):
        Exception.__init__(self)
        self.return_code = return_code
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    # 构造要返回的错误代码和错误信息的 dict
    def to_dict(self):
        rv = dict(self.payload or ())
        # 日志打印
        current_app.logger.error(DEFINE_ERRORS[self.return_code])
        # 增加 dict key: return code
        rv['return_code'] = self.return_code
        # 增加 dict key: message, 具体内容由常量定义文件中通过 return_code 转化而来
        rv['code'] = DEFINE_ERRORS[self.return_code]['code']
        rv['extra'] = DEFINE_ERRORS[self.return_code]['extra']
        rv['message'] = DEFINE_ERRORS[self.return_code]['info']
        return rv


# return 通用返回类
class ResponseCode:
    SUCCESS = 200
    WRONG_PARAM = 400
    MESSAGE = "ok!"

def generate_response(data=None,message=ResponseCode.MESSAGE,code=ResponseCode.SUCCESS):
    return {
        'message': message,
        'code': code,
        'data': data
    }


# 时间类
class timeTools():
    def __init__(self):
        pass    
    
    def getNowTime(self):
        return time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
