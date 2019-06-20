#!/usr/bin/env python
# -*- coding:utf8 -*-
"""
	restful api route 类和类注册文件
"""
import json
from flask import current_app,request,session
from flask_restful import Resource,reqparse
from flask_supervisor import mysql_db
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkecs.request.v20140526.DescribeInstancesRequest import DescribeInstancesRequest
from ..supervisor.models import Host

class EcsListApi(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('currentPage', type = int, default=1, location='args',help='第几个分页')
        self.reqparse.add_argument('page_size', type = int, default=10 , location='args',help='每页显示多少')
        self.reqparse.add_argument('username', type = str, default=session.get("username") , location='args',help='用户名')
        # 获取request json 参数
        self.json_args = request.json
        self.args = self.reqparse.parse_args()
        self.client = AcsClient(current_app.config['ACCESSKEYID'], current_app.config['ACCESSSECRET'], "cn-beijing")


    def get(self):
        username = self.args['username']
        page_index = self.args['currentPage']
        page_size = self.args['page_size']
        request = DescribeInstancesRequest()
        request.set_accept_format('json')
        response = self.client.do_action_with_exception(request)
        response = json.loads(str(response, encoding='utf-8'))
        response["PageNumber"] = page_index
        response["PageNumber"] = page_index
        response["Instances"]["Instance"] = response["Instances"]["Instance"][(page_index-1)*page_size:page_size*page_index]
        response["PageSize"] = page_size
        return  response


class HostListApi(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('currentPage', type = int, default=1, location='args',help='第几个分页')
        self.reqparse.add_argument('page_size', type = int, default=10 , location='args',help='每页显示多少')
        self.reqparse.add_argument('username', type = str, default=session.get("username") , location='args',help='用户名')
        # 获取request json 参数
        self.json_args = request.json
        self.args = self.reqparse.parse_args()
        self.client = AcsClient(current_app.config['ACCESSKEYID'], current_app.config['ACCESSSECRET'], "cn-beijing")


    def get(self):
        username = self.args['username']
        page_index = self.args['currentPage']
        page_size = self.args['page_size']
        request = DescribeInstancesRequest()
        request.set_accept_format('json')
        response = self.client.do_action_with_exception(request)
        response = json.loads(str(response, encoding='utf-8'))
        response["PageNumber"] = page_index
        response["PageNumber"] = page_index
        response["Instances"]["Instance"] = response["Instances"]["Instance"][(page_index-1)*page_size:page_size*page_index]
        response["PageSize"] = page_size
        return  response


    # 同步一个aliyun的主机到数据库
    def post(self):
        username = self.args['username']
        page_index = self.args['currentPage']
        page_size = self.args['page_size']
        host_name = self.json_args['InstanceName']
        instance_id = self.json_args['HostName']
        host_inner_ip = self.json_args['NetworkInterfaces']['NetworkInterface'][0]['PrimaryIpAddress']
        host_public_ip = self.json_args['PublicIpAddress']['IpAddress']
        host_info = self.json_args['OSType'] + "/" + self.json_args['OSName'] + "/" + str(self.json_args['Cpu']) + "/" + str(self.json_args['Memory']) + "M"
        print(host_info)
        try:
            new_host = Host(host_name,host_info,"".join(host_inner_ip),"".join(host_public_ip),22,1,1)
            mysql_db.session.add(new_host)
            mysql_db.session.commit()
            return {'code': 20000, 'message': "更新成功!"}
        except Exception as e:
            return {'code': 20002, 'message': str(e)}