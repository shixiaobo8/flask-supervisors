#!/usr/bin/env python
# -*- coding:utf8 -*-
"""
    flask - mongo model 类
"""
from .. import mongo_db
from marshmallow_mongoengine import ModelSchema,fields

class Operation(mongo_db.EmbeddedDocument):
    # 操作时间
    operator_time = mongo_db.DateTimeField()
    # 操作者
    operator_user = mongo_db.StringField()
    # 操作方式
    operator_type = mongo_db.StringField()
    # 操作对象
    operator_object = mongo_db.StringField()


class OperationSchema(ModelSchema):
    operator_time = fields.DateTime()
    operator_user = fields.String()
    operator_type = fields.String()
    operator_object = fields.String()
    class Meta:
        model = Operation


class serviceOperation(mongo_db.Document):
    # 服务名
    service_name = mongo_db.StringField()
    # 版本号
    version = mongo_db.StringField()
    # 服务操作事件
    # service_operator_event = mongo_db.ReferenceField(Operation)
    service_operator_event = mongo_db.EmbeddedDocumentField(Operation)


class serviceOperationSchema(ModelSchema):
    service_name = fields.String()
    version = fields.String()
    service_operator_event = fields.Nested(OperationSchema,many=True)
    class Meta:
        model = serviceOperation