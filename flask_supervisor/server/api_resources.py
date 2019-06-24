#!/usr/bin/env python
# -*- coding:utf8 -*-
"""
	restful api route 类和类注册文件
"""
import json
from flask import current_app,request,session
from flask_supervisor import mysql_db
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkecs.request.v20140526.DescribeInstancesRequest import DescribeInstancesRequest
from ..supervisor.models import Host,Node
from flask_restful import abort,Resource,reqparse,fields,marshal_with,marshal

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
        response["PageSize"] = page_size
        # 排除数据库中未写入的host数据
        instances_not_in_db = [ instance_id for instance_id in response["Instances"]["Instance"] if not Host.query.filter_by(ali_instance_id=instance_id['InstanceId']).first() ]
        response["Instances"]["Instance"] = instances_not_in_db
        return  response



class getHostModeName(fields.Raw):
    def format(self, value):
        return mysql_db.session.query(Node.nodeName).filter_by(id=value).first()[0]

# 输出字段

host_fields = {
    'id':fields.Integer(attribute="id"),
    'host_name':fields.String(attribute='hostname'),
    'node_name':getHostModeName(attribute='sv_node_id'),
    'host_info':fields.String(attribute='host_info'),
    'ali_instance_id':fields.String(attribute='ali_instance_id'),
    'host_inner_ip':fields.String(attribute='host_inner_ip'),
    'host_public_ip':fields.String(attribute='host_public_ip'),
    'sv_port':fields.Integer(attribute='sv_port'),
}

node_fields = {
    'node_name':fields.String(attribute='nodeName'),
    'hosts': fields.List(fields.Nested(host_fields,allow_null=True,default=''),default=''),
}

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
        # 查询node 下的节点所有服务器
        # hosts = mysql_db.session.query(Host).filter(Host.is_del == 0).join(Node,Node.id == Host.sv_node_id, isouter=True).all()
        hosts = mysql_db.session.query(Host).filter(Host.is_del == 0).join(Node,Node.id == Host.sv_node_id).all()
        page_hosts = hosts[(page_index - 1) * page_size:page_size * page_index]
        return {'code':0,'count':len(hosts),'cureent_page':page_index,"page_size":page_size,'data':marshal(page_hosts,host_fields)}


    # 同步一个aliyun的主机到数据库
    def post(self):
        username = self.args['username']
        page_index = self.args['currentPage']
        page_size = self.args['page_size']
        host_name = self.json_args['InstanceName']
        instance_id = self.json_args['InstanceId']
        host_inner_ip = self.json_args['NetworkInterfaces']['NetworkInterface'][0]['PrimaryIpAddress']
        host_public_ip = self.json_args['PublicIpAddress']['IpAddress']
        host_info = self.json_args['OSType'] + "/" + self.json_args['OSName'] + "/" + str(self.json_args['Cpu']) + "c/" + str(self.json_args['Memory']) + "M"
        try:
            if instance_id:
                new_host = Host(host_name,host_info,"".join(host_inner_ip),"".join(host_public_ip),1,instance_id)
            else:
                new_host = Host(host_name, host_info, "".join(host_inner_ip), "".join(host_public_ip), 1)
            mysql_db.session.add(new_host)
            mysql_db.session.commit()
            return {'code': 20000, 'message': "更新成功!"}
        except Exception as e:
            return {'code': 20002, 'message': str(e)}