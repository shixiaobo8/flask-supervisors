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

# 多对多配置 用户<--->用户组
# users = mysql_db.Table('users_groups',
#     mysql_db.Column('user_id', mysql_db.Integer, mysql_db.ForeignKey('fb_users.id')),
#     mysql_db.Column('userGroup_id', mysql_db.Integer, mysql_db.ForeignKey('fb_userGroups.id'))
#     )
#
#
# # 用户组
# class userGroup(mysql_db.Model):
#     __tablename__ = "fb_userGroups"
#     id = mysql_db.Column(mysql_db.Integer, primary_key=True,autoincrement=True)
#     # 多对多关联用户组
#     users = mysql_db.relationship('User', secondary=users,backref=mysql_db.backref('userGroup', lazy='dynamic'))
#     # 角色关联(一对多)
#     roles = mysql_db.relationship('Role', backref='userGroups',lazy='dynamic')
#     def __init__(self,userGroupName):
#         self.userGroupName = userGroupName
#
#     def __repr__(self):
#         return "<userGroup %r>" %self.userGroupName
#
# # 用户
# class User(mysql_db.Model):
#     __tablename__ = "fb_users"
#     id = mysql_db.Column(mysql_db.Integer, primary_key=True,autoincrement=True)
#     # 用户名
#     username = mysql_db.Column(mysql_db.String(80), unique=True,comment='用户名')
#     # 邮箱
#     email = mysql_db.Column(mysql_db.String(120), unique=True,comment='邮箱')
#     # 微信昵称
#     weixin_name = mysql_db.Column(mysql_db.String(120),  default='',comment='微信昵称')
#     # 逻辑删除
#     is_del = mysql_db.Column(mysql_db.Boolean,default=False,comment='逻辑删除')
#     # 创建时间
#     join_date = mysql_db.Column(mysql_db.DateTime,default=datetime.now())
#     # 用户组外键
#     userGroup_Id = mysql_db.Column(mysql_db.Integer,mysql_db.ForeignKey('fb_userGroups.id'),comment='关联一级用户组,多对一')
#
#     def __init__(self, username, email):
#         self.username = username
#         self.email = email
#
#     def __repr__(self):
#         return '<User %r>' % self.username
#
#
# class Nav(mysql_db.Model):
#     __tablename__ = "fb_navs"
#     id = mysql_db.Column(mysql_db.Integer,primary_key=True,autoincrement=True)
#     # 一级导航栏标题
#     navTitle = mysql_db.Column(mysql_db.String(120),unique=True,nullable=False,comment='一级导航栏标题')
#     # 一级导航栏url,可以为空,默认为空
#     navUrl = mysql_db.Column(mysql_db.String(120),nullable=True,default='',index=True,comment='一级导航栏url')
#     # 前后台导航栏分类
#     navType = mysql_db.Column(mysql_db.Boolean(),default=False,comment='导航栏分类,默认为后台导航栏')
#     # 逻辑删除
#     is_del = mysql_db.Column(mysql_db.Boolean(),default=False,comment='逻辑删除')
#     # 关联用户组权限
#     subnavs = mysql_db.relationship('subNav', backref='nav',lazy='dynamic')
#     # 角色外键
#     role_id = mysql_db.Column(mysql_db.Integer,mysql_db.ForeignKey('fb_roles.id'),comment='关联角色,多对一')
#     def __init__(self,navTitle,navUrl,navType,role_id):
#         self.navTitle = navTitle
#         self.navType = navType
#         self.navUrl = navUrl
#         self.role_id = role_id
#     def __repr__(self):
#         return "<Nav %r>" %self.navTitle
#
#
# # 二级导航栏
# class subNav(mysql_db.Model):
#     __tablename__ = "fb_subnavs"
#     id = mysql_db.Column(mysql_db.Integer,primary_key=True,autoincrement=True)
#     # 二级导航栏标题
#     title = mysql_db.Column(mysql_db.String(120),index=True,unique=True,nullable=False,default='#',comment='二级导航栏标题')
#     # 二级导航栏url
#     nav_url = mysql_db.Column(mysql_db.String(200),index=True,unique=True,nullable=False,default='#',comment='二级导航栏url')
#     # 一级导航栏外键
#     nav_Id = mysql_db.Column(mysql_db.Integer,mysql_db.ForeignKey('fb_navs.id'),comment='关联一级导航栏,多对一')
#     # 逻辑删除
#     is_del = mysql_db.Column(mysql_db.Boolean,default=False,comment='逻辑删除')
#
#     def __init__(self,title,nav_url):
#         self.title = title
#         self.nav_url = nav_url
#
#     def __repr__(self):
#         return "<subNav %r>" %self.title
#
#
# # 用户角色权限表
# class Role(mysql_db.Model):
#     __tablename__ = "fb_roles"
#     id = mysql_db.Column(mysql_db.Integer,primary_key=True,autoincrement=True)
#     # 角色名称
#     roleName = mysql_db.Column(mysql_db.String(120),unique=True,index=True,nullable=False,default='普通用户',comment='角色名称')
#     # 一级导航栏外键  一个角色有多个导航栏
#     navs = mysql_db.relationship('Nav', backref='role',lazy='dynamic')
#     # 用户组外键
#     fb_userGroup_Id = mysql_db.Column(mysql_db.Integer,mysql_db.ForeignKey('fb_userGroups.id'),comment='用户组权限外键')
#
#     def __init__(self,roleName):
#         self.roleName = roleName
#
#     def __repr__(self):
#         return "<Role %r>" %self.roleName


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


#  主机组表
class Group(mysql_db.Model):
    __tablename__ = "sv_groups"
    id = mysql_db.Column(mysql_db.Integer,primary_key=True,autoincrement=True)
    groupName = mysql_db.Column(mysql_db.String(120),unique=True,index=True,nullable=False)
    sv_groups = mysql_db.relationship('Host', backref='Group',lazy='dynamic')

    def __init__(self,groupName):
        self.groupName = groupName

    def __repr__(self):
        return "<Group %r>" %self.groupName


# 主机表
class Host(mysql_db.Model):
    __tablename__ = "sv_hosts"
    id = mysql_db.Column(mysql_db.Integer,primary_key=True,autoincrement=True)
    # 主机名称
    hostname = mysql_db.Column(mysql_db.String(120),unique=True,nullable=False,comment='主机名称')
    # 主机ip
    host_ip = mysql_db.Column(mysql_db.String(120),nullable=True,default='',index=True,comment='主机ip')
    # 主机端口
    sv_port = mysql_db.Column(mysql_db.Boolean(),default=False,comment='主机supervisor端口')
    # 逻辑删除
    is_del = mysql_db.Column(mysql_db.Boolean(),default=False,comment='逻辑删除')
    # 组外键
    sv_group_id = mysql_db.Column(mysql_db.Integer,mysql_db.ForeignKey('sv_groups.id'),comment='关联组,多对一')
    # 节点外键
    sv_node_id = mysql_db.Column(mysql_db.Integer,mysql_db.ForeignKey('sv_nodes.id'),comment='关联节点,多对一')
    def __init__(self,hostname,host_ip,sv_port,sv_group_id,sv_node_id):
        self.hostname = hostname
        self.host_ip = host_ip
        self.sv_port = sv_port
        self.sv_group_id = sv_group_id
        self.sv_node_id = sv_node_id
    def __repr__(self):
        return "<Host %r>" %self.hostname


# 用户
class User(mysql_db.Model,UserMixin):
    __tablename__ = "sv_users"
    id = mysql_db.Column(mysql_db.Integer, primary_key=True,autoincrement=True)
    # 用户名
    username = mysql_db.Column(mysql_db.String(80), unique=True,comment='用户名')
    # 头像
    avatar = mysql_db.Column(mysql_db.String(120), unique=True, comment='头像')
    # 邮箱
    email = mysql_db.Column(mysql_db.String(120), unique=True,comment='邮箱')
    # 微信昵称
    weixin_name = mysql_db.Column(mysql_db.String(120),  default='',comment='微信昵称')
    # 手机号
    phone = mysql_db.Column(mysql_db.String(11), default='',unique=True, comment='手机号')
    # 逻辑删除
    is_del = mysql_db.Column(mysql_db.Boolean,default=False,comment='逻辑删除')
    # 创建时间
    join_date = mysql_db.Column(mysql_db.DateTime,default=datetime.now())
    # 最近修改时间
    last_modify = mysql_db.Column(mysql_db.DateTime, default=datetime.now())
    # 密码
    password_hash = mysql_db.Column(mysql_db.String(255))
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

    def __init__(self, id,username, email):
        self.id = id
        self.username = username
        self.email = email

    def login(self):
        login_user(self)

    def __repr__(self):
        return '<User %r>' % self.username