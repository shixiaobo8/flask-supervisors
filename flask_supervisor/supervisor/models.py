#!/usr/bin/env python
# -*- coding:utf8 -*-
"""
    mysql model 类
"""
from .. import mysql_db
from datetime import datetime


# 多对多配置 用户<--->用户组
users = mysql_db.Table('users_groups',
    mysql_db.Column('user_id', mysql_db.Integer, mysql_db.ForeignKey('fb_users.id')),
    mysql_db.Column('userGroup_id', mysql_db.Integer, mysql_db.ForeignKey('fb_userGroups.id'))
    )


# 用户组
class userGroup(mysql_db.Model):
    __tablename__ = "fb_userGroups"
    id = mysql_db.Column(mysql_db.Integer, primary_key=True,autoincrement=True)
    # 多对多关联用户组
    users = mysql_db.relationship('User', secondary=users,backref=mysql_db.backref('userGroup', lazy='dynamic'))
    # 角色关联(一对多)
    roles = mysql_db.relationship('Role', backref='userGroups',lazy='dynamic')
    def __init__(self,userGroupName):
        self.userGroupName = userGroupName

    def __repr__(self):
        return "<userGroup %r>" %self.userGroupName

# 用户
class User(mysql_db.Model):
    __tablename__ = "fb_users"
    id = mysql_db.Column(mysql_db.Integer, primary_key=True,autoincrement=True)
    # 用户名
    username = mysql_db.Column(mysql_db.String(80), unique=True,comment='用户名')
    # 邮箱
    email = mysql_db.Column(mysql_db.String(120), unique=True,comment='邮箱')
    # 微信昵称
    weixin_name = mysql_db.Column(mysql_db.String(120),  default='',comment='微信昵称')
    # 逻辑删除
    is_del = mysql_db.Column(mysql_db.Boolean,default=False,comment='逻辑删除')
    # 创建时间
    join_date = mysql_db.Column(mysql_db.DateTime,default=datetime.now())
    # 用户组外键
    userGroup_Id = mysql_db.Column(mysql_db.Integer,mysql_db.ForeignKey('fb_userGroups.id'),comment='关联一级用户组,多对一')

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.username


class Nav(mysql_db.Model):
    __tablename__ = "fb_navs"
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
    role_id = mysql_db.Column(mysql_db.Integer,mysql_db.ForeignKey('fb_roles.id'),comment='关联角色,多对一')
    def __init__(self,navTitle,navUrl,navType,role_id):
        self.navTitle = navTitle
        self.navType = navType
        self.navUrl = navUrl
        self.role_id = role_id
    def __repr__(self):
        return "<Nav %r>" %self.navTitle


# 二级导航栏
class subNav(mysql_db.Model):
    __tablename__ = "fb_subnavs"
    id = mysql_db.Column(mysql_db.Integer,primary_key=True,autoincrement=True)
    # 二级导航栏标题
    title = mysql_db.Column(mysql_db.String(120),index=True,unique=True,nullable=False,default='#',comment='二级导航栏标题')
    # 二级导航栏url
    nav_url = mysql_db.Column(mysql_db.String(200),index=True,unique=True,nullable=False,default='#',comment='二级导航栏url')
    # 一级导航栏外键
    nav_Id = mysql_db.Column(mysql_db.Integer,mysql_db.ForeignKey('fb_navs.id'),comment='关联一级导航栏,多对一')
    # 逻辑删除
    is_del = mysql_db.Column(mysql_db.Boolean,default=False,comment='逻辑删除')

    def __init__(self,title,nav_url):
        self.title = title
        self.nav_url = nav_url

    def __repr__(self):
        return "<subNav %r>" %self.title


# 用户角色权限表
class Role(mysql_db.Model):
    __tablename__ = "fb_roles"
    id = mysql_db.Column(mysql_db.Integer,primary_key=True,autoincrement=True)
    # 角色名称
    roleName = mysql_db.Column(mysql_db.String(120),unique=True,index=True,nullable=False,default='普通用户',comment='角色名称')
    # 一级导航栏外键  一个角色有多个导航栏
    navs = mysql_db.relationship('Nav', backref='role',lazy='dynamic')
    # 用户组外键
    fb_userGroup_Id = mysql_db.Column(mysql_db.Integer,mysql_db.ForeignKey('fb_userGroups.id'),comment='用户组权限外键')

    def __init__(self,roleName):
        self.roleName = roleName

    def __repr__(self):
        return "<Role %r>" %self.roleName

