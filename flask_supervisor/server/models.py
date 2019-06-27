#!/usr/bin/env python
# -*- coding:utf8 -*-
"""
    flask - mongo model 类
"""
from .. import mongo_db

class Operation(mongo_db.Document):
    operator_time = mongo_db.DateTimeField()
    operator_user = mongo_db.StringField()
    event = mongo_db.StringField()


class serviceOperation(mongo_db.Document):
    service_name = mongo_db.StringField()
    service_operator_event = mongo_db.DocumentField(Operation)