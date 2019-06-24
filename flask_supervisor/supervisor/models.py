#!/usr/bin/env python
# -*- coding:utf8 -*-
"""
    mysql model 类
"""
from .. import mysql_db
from flask_login import UserMixin,login_user
from flask_supervisor import login_manager
from datetime import datetime
import six
from werkzeug.security import generate_password_hash,check_password_hash#转换密码用到的库

# # 多对多配置 用户<--->用户组
# users = mysql_db.Table('users_groups',
#     mysql_db.Column('user_id', mysql_db.Integer, mysql_db.ForeignKey('sv_users.id')),
#     mysql_db.Column('userGroup_id', mysql_db.Integer, mysql_db.ForeignKey('sv_userGroups.id'))
#     )


# # 用户组
class userGroup(mysql_db.Model):
    __tablename__ = "sv_userGroups"
    id = mysql_db.Column(mysql_db.Integer, primary_key=True,autoincrement=True)
    # # 多对多关联用户组
    # users = mysql_db.relationship('User', secondary=users,backref=mysql_db.backref('userGroup', lazy='dynamic'))
    # 角色关联(一对多)
    roles = mysql_db.relationship('Role', backref='userGroups',lazy='dynamic')
    def __init__(self,userGroupName):
        self.userGroupName = userGroupName

    def __repr__(self):
        return "<userGroup %r>" %self.userGroupName


class Nav(mysql_db.Model):
    __tablename__ = "sv_navs"
    id = mysql_db.Column(mysql_db.Integer,primary_key=True,autoincrement=True)
    # 一级导航栏标题
    navTitle = mysql_db.Column(mysql_db.String(120),unique=True,nullable=False,comment='一级导航栏标题')
    # 一级导航栏url,可以为空,默认为空
    navUrl = mysql_db.Column(mysql_db.String(120),nullable=True,default='',index=True,comment='一级导航栏url')
    # 前后台导航栏分类
    navType = mysql_db.Column(mysql_db.Boolean(),default=False,comment='导航栏分类,默认为后台导航栏')
    # 逻辑删除
    is_del = mysql_db.Column(mysql_db.Boolean(),default=False,comment='逻辑删除')
    # 关联用户组权限
    subnavs = mysql_db.relationship('subNav', backref='nav',lazy='dynamic')
    # 角色外键
    role_id = mysql_db.Column(mysql_db.Integer,mysql_db.ForeignKey('sv_roles.id'),comment='关联角色,多对一')
    def __init__(self,navTitle,navUrl,navType,role_id):
        self.navTitle = navTitle
        self.navType = navType
        self.navUrl = navUrl
        self.role_id = role_id
    def __repr__(self):
        return "<Nav %r>" %self.navTitle


# # 二级导航栏
class subNav(mysql_db.Model):
    __tablename__ = "sv_subnavs"
    id = mysql_db.Column(mysql_db.Integer,primary_key=True,autoincrement=True)
    # 二级导航栏标题
    title = mysql_db.Column(mysql_db.String(120),index=True,unique=True,nullable=False,default='#',comment='二级导航栏标题')
    # 二级导航栏url
    nav_url = mysql_db.Column(mysql_db.String(200),index=True,unique=True,nullable=False,default='#',comment='二级导航栏url')
    # 一级导航栏外键
    nav_Id = mysql_db.Column(mysql_db.Integer,mysql_db.ForeignKey('sv_navs.id'),comment='关联一级导航栏,多对一')
    # 逻辑删除
    is_del = mysql_db.Column(mysql_db.Boolean,default=False,comment='逻辑删除')

    def __init__(self,title,nav_url):
        self.title = title
        self.nav_url = nav_url

    def __repr__(self):
        return "<subNav %r>" %self.title


# # 用户角色权限表
class Role(mysql_db.Model):
    __tablename__ = "sv_roles"
    id = mysql_db.Column(mysql_db.Integer,primary_key=True,autoincrement=True)
    # 角色名称
    roleName = mysql_db.Column(mysql_db.String(120),unique=True,index=True,nullable=False,default='普通用户',comment='角色名称')
    # 一级导航栏外键  一个角色有多个导航栏
    navs = mysql_db.relationship('Nav', backref='role',lazy='dynamic')
    # 用户组外键
    sv_userGroup_Id = mysql_db.Column(mysql_db.Integer,mysql_db.ForeignKey('sv_userGroups.id'),comment='用户组权限外键')

    def __init__(self,roleName):
        self.roleName = roleName

    def __repr__(self):
        return "<Role %r>" %self.roleName


#  主机节点表
class Node(mysql_db.Model):
    __tablename__ = "sv_nodes"
    id = mysql_db.Column(mysql_db.Integer,primary_key=True,autoincrement=True)
    nodeName = mysql_db.Column(mysql_db.String(120),unique=True,index=True,nullable=False,comment='节点名称')
    sv_nodes = mysql_db.relationship('Host', backref='node',lazy='dynamic')
    def __init__(self,nodeName):
        self.nodeName = nodeName

    def __repr__(self):
        return "<Node %r>" %self.nodeName


# 主机表
class Host(mysql_db.Model):
    __tablename__ = "sv_hosts"
    id = mysql_db.Column(mysql_db.Integer,primary_key=True,autoincrement=True)
    # 主机名称
    hostname = mysql_db.Column(mysql_db.String(120),unique=True,nullable=False,comment='主机名称')
    # 主机信息instance_id
    host_info = mysql_db.Column(mysql_db.String(120), nullable=False, comment='主机信息')
    # 阿里云实例id
    ali_instance_id = mysql_db.Column(mysql_db.String(120), unique=True, nullable=False, comment='阿里云实例id')
    # 主机内网ip
    host_inner_ip = mysql_db.Column(mysql_db.String(120),nullable=True,default='',index=True,comment='主机内网ip')
    # 主机公网ip
    host_public_ip = mysql_db.Column(mysql_db.String(120), nullable=True, default='', index=True, comment='主机公网ip')
    # 主机ssh端口
    sv_port = mysql_db.Column(mysql_db.Integer,default=22,comment='主机ssh端口')
    # 逻辑删除
    is_del = mysql_db.Column(mysql_db.Boolean(),default=False,comment='逻辑删除')
    # 节点外键
    sv_node_id = mysql_db.Column(mysql_db.Integer,mysql_db.ForeignKey('sv_nodes.id'),comment='关联节点,多对一')


    def __init__(self,hostname,host_info,host_inner_ip,host_public_ip,sv_node_id,ali_intance_id="",sv_port=22):
        self.hostname = hostname
        self.host_info = host_info
        self.ali_instance_id = ali_intance_id
        self.host_inner_ip = host_inner_ip
        self.host_public_ip = host_public_ip
        self.sv_port = sv_port
        self.sv_node_id = sv_node_id
    def __repr__(self):
        return "<Host %r>" %self.hostname


# 多对多 服务与主机
service_hosts = mysql_db.Table("services_hosts",
                          mysql_db.Column("service_id",mysql_db.Integer,mysql_db.ForeignKey("sv_services.id")),
                          mysql_db.Column("host_id", mysql_db.Integer, mysql_db.ForeignKey("sv_hosts.id")),
                          )

# 多对多  服务与用户
user_service = mysql_db.Table("services_users",
                          mysql_db.Column("service_id",mysql_db.Integer,mysql_db.ForeignKey("sv_services.id")),
                          mysql_db.Column("user_id", mysql_db.Integer, mysql_db.ForeignKey("sv_users.id")),
                          )

# 服务表
class Service(mysql_db.Model):
    __tablename__ = "sv_services"
    id = mysql_db.Column(mysql_db.Integer, primary_key=True, autoincrement=True)
    # 服务名称
    service_name = mysql_db.Column(mysql_db.String(120), unique=True, index=True,nullable=False, comment='服务名称')
    # 服务部署路径
    service_deploy_dir = mysql_db.Column(mysql_db.String(120), index=True, nullable=False, comment='服务部署路径')
    # 服务详情描述
    service_detail = mysql_db.Column(mysql_db.String(120), index=True, nullable=False, comment='服务详情描述')
    # 服务启动命令
    service_start_cmd = mysql_db.Column(mysql_db.String(120), nullable=True, default='', index=True, comment='服务启动命令')
    # 服务端口号
    service_ports = mysql_db.Column(mysql_db.String(120), nullable=True, default='', index=True, comment='服务端口号')
    # 开发/维护人员(外键)
    devops_user_id =  mysql_db.Column(mysql_db.Integer, mysql_db.ForeignKey('sv_users.id'), comment='关联用户,多对多')
    # 部署机器(外键)
    deploy_host_id = mysql_db.Column(mysql_db.Integer, mysql_db.ForeignKey('sv_hosts.id'), comment='关联主机,多对多')
    # 逻辑删除
    is_del = mysql_db.Column(mysql_db.Boolean(), default=False, comment='逻辑删除')

    def __init__(self,service_name,service_detail,service_start_cmd,service_ports,devops_user_id,deploy_host_id,is_del=0,service_deploy_dir=''):
        self.service_name = service_name
        self.service_detail = service_detail
        self.service_start_cmd = service_start_cmd
        self.service_ports = service_ports
        self.deploy_host_id = deploy_host_id
        self.devops_user_id = devops_user_id
        self.is_del = is_del
        self.service_deploy_dir = service_deploy_dir

    def __repr__(self):
        return "<Host %r>" %self.service_name


# 用户
class User(mysql_db.Model,UserMixin):
    __tablename__ = "sv_users"
    id = mysql_db.Column(mysql_db.Integer, primary_key=True,autoincrement=True)
    # 用户名
    username = mysql_db.Column(mysql_db.String(80), unique=True,comment='用户名')
    # 头像
    avatar = mysql_db.Column(mysql_db.String(120),default='img/users/default.jpg',comment='头像')
    # 邮箱
    email = mysql_db.Column(mysql_db.String(120), unique=True,comment='邮箱')
    # 微信昵称
    weixin_name = mysql_db.Column(mysql_db.String(120),unique=True,comment='微信昵称')
    # 手机号
    phone = mysql_db.Column(mysql_db.String(11), unique=True, comment='手机号')
    # 逻辑删除
    is_del = mysql_db.Column(mysql_db.Boolean,default=False,comment='逻辑删除')
    # 创建时间
    join_date = mysql_db.Column(mysql_db.DateTime,default=datetime.now())
    # 最近修改时间
    last_modify = mysql_db.Column(mysql_db.DateTime, default=datetime.now())
    # 密码
    password_hash = mysql_db.Column(mysql_db.String(255))
    # 关联用户组
    userGroup_Id = mysql_db.Column(mysql_db.Integer,mysql_db.ForeignKey('sv_userGroups.id'),comment='关联一级用户组,多对一')

    @property
    def password(self):
        raise AttributeError("密码不允许读取")

    # 转换密码为hash存入数据库
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    # 检查密码
    def check_password_hash(self, password):
        return check_password_hash(self.password_hash, password)

    # 下面这4个方法是flask_login需要的4个验证方式
    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    @property
    def get_id(self):
        print(self.id)
        return self.id
        # return six.text_type(self.id)

    def __init__(self,username,email,password):
        self.username = username
        self.email = email
        self.password_hash = password

    def login(self):
        login_user(self)

    def __repr__(self):
        return '<User %r>' % self.username