#!/usr/bin/env python
# -*- coding:utf8 -*-
from flask import Blueprint

backend = Blueprint('backend',__name__)

from . import views,api_resources
from flask import make_response
from flask_restful import Resource,Api
from .api_resources import LoginApi,UserApi,UserTouXiangApi
from .api_resources import NavApi,NavListApi,LoginApi,UserListApi
import json

# 注册蓝图api
api = Api(backend,catch_all_404s=True)

# 添加api 可插拔式路由
api.add_resource(NavApi,'/Nav','NavApi')
api.add_resource(NavListApi,'/NavList','NavListApi')
api.add_resource(LoginApi,'/Login','LoginApi')
api.add_resource(UserApi,'/user/info','UserApi')
api.add_resource(UserListApi,'/user/userList','UserListApi')
api.add_resource(UserTouXiangApi,'/user/info/touxiang','UserTouXiangApi')