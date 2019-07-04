#!/usr/bin/env python
# -*- coding:utf8 -*-
"""
	restful api route 类和类注册文件
"""
import json,configparser,os,time,werkzeug,datetime,traceback
from flask import current_app,request,session,flash,redirect,jsonify
from werkzeug.utils import secure_filename
from .models import  Operation,serviceOperation,OperationSchema,serviceOperationSchema
from flask_supervisor import mysql_db,mongo_db
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkecs.request.v20140526.DescribeInstancesRequest import DescribeInstancesRequest
from ..supervisor.models import Host,Node,Service,User
from flask_restful import abort,Resource,reqparse,fields,marshal_with,marshal
from .paramiko_util import SSHConnection,operation_logger
from shutil import copyfile


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
        self.reqparse.add_argument('is_detail', type = int, default=10 , location='args',help='是否加载详情')
        self.reqparse.add_argument('username', type = str, default=session.get("username") , location='args',help='用户名')
        # 获取request json 参数
        self.json_args = request.json
        self.args = self.reqparse.parse_args()


    def get(self):
        username = self.args['username']
        page_index = self.args['currentPage']
        page_size = self.args['page_size']
        is_detail = self.args['is_detail']
        hosts = []
        # 查询node 下的节点所有服务器
        if not is_detail:
            # hosts = mysql_db.session.query(Host).filter(Host.is_del == 0).join(Node,Node.id == Host.sv_node_id, isouter=True).all()
            hosts = mysql_db.session.query(Host).filter(Host.is_del == 0).join(Node,Node.id == Host.sv_node_id).all()
            page_hosts = hosts[(page_index - 1) * page_size:page_size * page_index]
            return {'code': 0, 'count': len(hosts), 'cureent_page': page_index, "page_size": page_size,
                    'data': marshal(page_hosts, host_fields)}
        elif is_detail:
            hosts = mysql_db.session.query(Host.hostname,Host.host_inner_ip,Host.host_public_ip).filter(Host.is_del == 0).all()
            return {'code': 0, 'count': len(hosts), 'cureent_page': page_index, "page_size": page_size,
                    'data': hosts}



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



# 输出字段

shost_fields = {
    "hostname":fields.String(attribute='hostname'),
    "host_inner_ip": fields.String(attribute='host_inner_ip'),
    "host_public_ip": fields.String(attribute='host_public_ip'),
}

sdevops_fields = {
    "username":fields.String(attribute='username'),
}

class getServiceHosts(fields.Raw):
    def format(self, value):
        return [ marshal(v,shost_fields)  for v in value ]

class getServiceDevUser(fields.Raw):
    def format(self, value):
        return [ marshal(v,sdevops_fields) for v in value ]


class getServicePorts(fields.Raw):
    def format(self, value):
        return value



service_fields = {
    'id':fields.Integer(attribute="id"),
    'service_name':fields.String(attribute='service_name'),
    'service_detail':fields.String(attribute='service_detail'),
    'service_mathines':getServiceHosts(attribute='services_hosts'),
    'service_developers':getServiceDevUser(attribute='services_developers'),
    'service_cmd':fields.String(attribute='service_start_cmd'),
    'service_ports':getServicePorts(attribute='service_ports'),
}


# 服务列表 api
class ServiceListApi(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('currentPage', type=int, default=1, location='args', help='第几个分页')
        self.reqparse.add_argument('page_size', type=int, default=10, location='args', help='每页显示多少')
        self.reqparse.add_argument('username', type=str, default=session.get("username"), location='args', help='用户名')
        # 获取request json 参数
        self.json_args = request.json
        self.args = self.reqparse.parse_args()


    def get(self):
        username = self.args['username']
        page_index = self.args['currentPage']
        page_size = self.args['page_size']
        servives = mysql_db.session.query(Service).filter(Service.is_del == 0).all()
        page_services = servives[(page_index - 1) * page_size:page_size * page_index]
        return {'code':0,'count':len(servives),'cureent_page':page_index,"page_size":page_size,'data':marshal(page_services,service_fields)}


    def post(self):
        pass

    def delete(self):
        pass

    def put(self):
        pass


# 服务api
class ServiceApi(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('currentPage', type=int, default=1, location='args', help='第几个分页')
        self.reqparse.add_argument('page_size', type=int, default=10, location='args', help='每页显示多少')
        self.reqparse.add_argument('username', type=str, default=session.get("username"), location='args', help='用户名')
        # 获取request json 参数
        self.json_args = request.json
        self.args = self.reqparse.parse_args()

    def get(self):
        pass

    def post(self):
        username = self.args['username']
        service_name = self.json_args["service_name"]
        service_detail = self.json_args["service_detail"]
        service_developers = self.json_args['service_developers']
        service_cmd = self.json_args['service_cmd']
        service_mathines = self.json_args['service_mathines']
        service_ports = self.json_args['service_ports']
        # 判断是否存在对应的服务名
        exists_service = Service.query.filter_by(service_name=service_name).first()
        if exists_service:
            return {'code': 20002, "message":"服务名已存在"}
        else:
            for user in service_developers:
                new_service = Service(service_name, service_detail, service_cmd, ",".join(service_ports))
                eu = User.query.filter_by(username=user).first()
                new_service.services_developers.append(eu)
                for host in service_mathines:
                    eh = Host.query.filter_by(hostname=host.split("/")[0]).first()
                    new_service.services_hosts.append(eh)
                mysql_db.session.add(new_service)
                mysql_db.session.commit()
            return {'code': 20000, "message": "更新成功"}

    def delete(self):
        service_id = self.json_args['id']
        if service_id:
            service = Service.query.filter_by(id=service_id).first()
            service.is_del = 1
            mysql_db.session.commit()
            return {"code":"20000","message":"删除成功!"}
        else:
            return {"code":"20002","message":"缺少参数"}

    def put(self):
        pass


# AnsibleManagerApi  ansible管理主机
class AnsibleManagerApi(Resource):
    def __init__(self):
        self.ansible_conf = current_app.config["ANSIBLE_CONFIG_FILE"]
        self.cf = configparser.ConfigParser()

    def get(self):
        self.cf.read(self.ansible_conf,encoding='gbk')


    def post(self):
        pass

    def delete(self):
        pass

    def put(self):
        pass


# 服务器文件上传api ServerFileApi
class ServerFileApi(Resource):
    def __init__(self):
        self.upload_version_file_dir = current_app.config["UPLOAD_VERSION_FILE_DIR"]
        self.service_backup_file_dir = current_app.config["SERVICE_BACKUP_FILE_DIR"]
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('currentPage', type=int, default=1, location='args', help='第几个分页')
        self.reqparse.add_argument('page_size', type=int, default=10, location='args', help='每页显示多少')
        self.reqparse.add_argument('username', type=str, default=session.get("username"), location='args', help='用户名')
        self.reqparse.add_argument('service', type=str, location='args', help='服务名')
        # 获取request json 参数
        self.json_args = request.json
        self.args = self.reqparse.parse_args()

    # 文件列表 一次返回服务器发布/备份/回滚的所有文件
    def get(self):
        service_name = self.args.get("service")
        res = dict()
        all_files = [self.upload_version_file_dir, self.service_backup_file_dir]
        for dir_step in range(0,len(all_files)):
            if not os.path.exists(all_files[dir_step] + "/" + service_name):
                os.makedirs(all_files[dir_step] + "/" + service_name)
            if not os.path.exists(all_files[dir_step]):
                return {"message":"服务器目录不存在,请联系服务器管理人员!",'code':'20002'}
            if dir_step == 0:
                res['uploads'] = []
            if dir_step == 1:
                res['backups'] = []
            if dir_step == 2:
                res['rollbacks'] = []
            service_files = os.listdir(all_files[dir_step] + "/" + service_name)
            for file in service_files:
                file_obj = {}
                file_obj['file_path'] = all_files[dir_step] + "/" + service_name + "/" + file
                file_obj['file_size'] = str(os.path.getsize(all_files[dir_step] + "/" + service_name + "/" + file)/1024/1024) + "M"
                file_obj['file_ctime'] =  time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(os.path.getctime(all_files[dir_step] + "/" + service_name + "/" + file)))
                file_obj['file_mtime'] =  time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(os.path.getmtime(all_files[dir_step] + "/" + service_name + "/" + file)))
                if dir_step == 0:
                    res['uploads'].append(file_obj)
                if dir_step == 1:
                    res['backups'].append(file_obj)
                if dir_step == 2:
                    res['rollbacks'].append(file_obj)
        return res


    # 文件上传
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('file', type=werkzeug.datastructures.FileStorage, location='files')
        user_name = request.form.get('username')
        service_name = request.form.get('service_name')
        store_path = current_app.config['UPLOAD_VERSION_FILE_DIR'] + os.sep + service_name
        message = "文件上传成功!"
        code = '20000'
        # 上传文件
        try:
        # check if the post request has the file part
            if 'file' not in request.files:
                flash('No file part')
                message = 'No file part'
                return redirect(request.url)
            file = request.files['file']
            # if user does not select file, browser also
            # submit an empty part without filename
            if file.filename == '':
                flash('No selected file')
                message = 'No selected file'
            if file:
                filename = secure_filename(file.filename)
            if not os.path.exists(store_path):
                os.mkdir(store_path)
            t_now = time.strftime('%Y_%m_%d_%H_%M_%S',time.localtime(time.time()))
            version = ''
            n_file_name = ''
            if filename.endswith(".tar.gz"):
                version = filename.replace(".tar.gz",'') + "-" + t_now
                n_file_name = version + ".tar.gz"
            if filename.endswith(".tgz"):
                version = filename.replace(".tgz",'') + "-" + t_now
                n_file_name = version + ".tgz"
            if filename.endswith(".zip"):
                version = filename.replace(".zip",'') + "-" + t_now
                n_file_name = version + ".zip"
            store_file_name = store_path + os.sep + n_file_name
            file.save(store_file_name)
            op = Operation(operator_time=datetime.datetime.now(),operator_user=user_name,operator_type="上传",operator_object="新文件  "+store_file_name)
            sop = serviceOperation(service_name=service_name,version=version,service_operator_event=op)
            op.save()
            sop.save()
        except Exception as e:
            traceback.print_exc()
            print(e)
            code = '20002'
            message = "文件上传失败!"
        return jsonify({"code": code, 'message': message})


    def put(self):
        pass


    def delete(self):
        pass


# 版本控制VersionControllsApi
class VersionControllsApi(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('currentPage', type=int, default=1, location='args', help='第几个分页')
        self.reqparse.add_argument('page_size', type=int, default=10, location='args', help='每页显示多少')
        self.reqparse.add_argument('username', type=str, default=session.get("username"), location='args', help='用户名')
        self.reqparse.add_argument('service_name', type=str, location='args', help='服务名')
        # 获取request json 参数
        self.json_args = request.json
        self.args = self.reqparse.parse_args()


    #  一次返回服务器发布历史记录服务历史
    def get(self):
        service_name = self.args.get("service_name")
        sobj = serviceOperation.objects.filter(service_name=service_name).all()
        return json.loads(sobj.to_json())

    # 远程操作api
    def post(self):
        user_name = self.args.get('username')
        service_name = self.args.get('service_name')
        operation = self.json_args['operation']
        select_operation_pkg = self.json_args['select_operation_pkg']
        select_hosts = self.json_args['select_hosts']
        operation_logger.info("=====开始执行远程操作======.....")
        operation_logger.info("获取到远程操作参数:"+str(self.args) + "  " + str(self.json_args))
        # 判断参数完整性
        if not operation or not service_name or not user_name or not select_operation_pkg or not select_hosts:
            return jsonify({"code":'20003','message':"参数不完整!"})
        # 获取远程主机信息
        for host in select_hosts:
            try:
                # 获取内网ip
                host_publicip = host.split("/")[-1]
                host_innerip = host.split("/")[-2]
                exec_host = Host.query.filter_by(host_inner_ip=host_innerip).first()
                # 建立ssh 连接
                ssh_client = SSHConnection({"host":exec_host.host_inner_ip,"port":exec_host.sv_port,"username":"root","pwd":"123456"})
                # ssh_client = SSHConnection({"host":'10.0.0.4',"port":exec_host.sv_port,"username":"root","pwd":"123456"})
                operation_logger.info("正在尝试连接服务器"+host_publicip+"/"+host_innerip+"   请稍后....")
                ssh_client.connect()
                local_upload_dir = current_app.config['UPLOAD_VERSION_FILE_DIR']
                local_backup_dir = current_app.config['SERVICE_BACKUP_FILE_DIR']
                # 远程执行命令
                # 先管理系统内部进行备份
                # 发布
                if operation == 'upload':
                    pass
                # 备份
                elif operation == 'backup':
                    pkg = select_operation_pkg
                    bpkg = pkg.replace(".tar.gz","_backup.tar.gz").replace(".zip","_backup.zip").replace(".tgz","_backup.tgz")
                    orign_backup_pkg = local_upload_dir + service_name + "/" + pkg
                    backup_pkg = local_backup_dir + service_name + "/"  + bpkg
                    operation_logger.info("正在本机进行程序备份..."+pkg +" 备份后的文件名是:" + backup_pkg)
                    copyfile(orign_backup_pkg,backup_pkg)
                    operation_logger.info("本地文件"+orign_backup_pkg+"备份完成..正在远程备份.....请稍后..")
                    ssh_client.upload(backup_pkg,"/im_backup_pkgs/",bpkg)
                    operation_logger.info("本地文件"+orign_backup_pkg+"在远程机器"+host+"上备份完成!.")
                    return jsonify({"code": '20000', 'message': "ok!"})
                # 回滚
                elif operation == 'rollback':
                    pass
            except Exception as e:
                print(e)
                traceback.print_exc(file=open(operation_logger.handlers[0].baseFilename,"a+",encoding='UTF-8'))
                operation_logger.error("服务器连接失败....请登陆服务器或联系管理员....")
                return jsonify({"code": '20000', 'message': "服务器内部错误!"})
        return jsonify({"code": '20000', 'message': self.json_args})


    def put(self):
        pass


    def delete(self):
        pass