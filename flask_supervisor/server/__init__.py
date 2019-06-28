#!/usr/bin/env python
# -*- coding:utf8 -*-
from flask import Blueprint

server = Blueprint('server',__name__)

from . import views,api_resources
from flask_restful import Api
from .api_resources import EcsListApi,HostListApi,ServiceApi,ServiceListApi,AnsibleManagerApi,ServerFileApi,VersionControllsApi

# 注册蓝图api
api = Api(server,catch_all_404s=True)

# 添加api 可插拔式路由
api.add_resource(EcsListApi,'/ali/EcsList','EcsListApi')
api.add_resource(HostListApi,'/HostList','HostListApi')
api.add_resource(ServiceApi,'/Service','ServiceApi')
api.add_resource(ServerFileApi,'/ServerFile','ServerFileApi')
api.add_resource(VersionControllsApi,'/VersionControlls','VersionControllsApi')
api.add_resource(ServiceListApi,'/ServiceList','ServiceListApi')
api.add_resource(AnsibleManagerApi,'/Ansible','AnsibleManagerApi')