#!/usr/bin/env python
# -*- coding:utf8 -*-
"""
    flask - mongo model 类
"""
from .. import mongo_db

class Operation(mongo_db.Document):
    # 操作时间
    operator_time = mongo_db.DateTimeField()
    # 操作者
    operator_user = mongo_db.StringField()
    # 操作事件
    event = mongo_db.StringField()


class serviceOperation(mongo_db.Document):
    # 服务名
    service_name = mongo_db.StringField()
    # 版本号
    version = mongo_db.StringField()
    # 服务操作事件
    service_operator_event = mongo_db.DocumentField(Operation)