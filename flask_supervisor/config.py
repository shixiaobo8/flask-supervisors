#!/usr/bin/env python
# -*- coding:utf8 -*-
"""
	配置文件(官方文档中提倡的有效配置文件写法)
	     参考:https://dormousehole.readthedocs.io/en/latest/config.html
	     使用config.py 对象的规则:
		1. app加载的时候使用 app.config.from_object('configmodule.ProductionConfig')
	  	2. Config 对象中必须的变量名称必须大写开头
"""
from logging.config import dictConfig
import os
import time
import logging
 
basedir = os.path.abspath(os.path.dirname(__file__))
log_path = basedir+os.sep+'logs'+ os.sep
if not os.path.exists(log_path):
    os.makedirs(log_path)

# 日志格式配置
dictConfig({
        'version': 1,
            'formatters': {
                'default': {
                            'format': '%(asctime)s [%(threadName)s:%(thread)d in %(module)s:] [task_id:%(name)s] [%(name)s:%(lineno)d] [%(levelname)s]- %(message)s'
                 },
                'file_access': {
                            'format': '%(asctime)s [%(threadName)s:%(thread)d in %(module)s:] [task_id:%(name)s] [%(name)s:%(lineno)d] [%(levelname)s]- %(message)s'
                 },
                'file_error': {
                            'format': '%(asctime)s [%(threadName)s:%(thread)d in %(module)s:] [task_id:%(name)s] [%(name)s:%(lineno)d] [%(levelname)s]- %(message)s'
                 },
            },
            'handlers': {
                        'wsgi': {
                            'class': 'logging.StreamHandler',
                            'stream': 'ext://flask.logging.wsgi_errors_stream',
                            'formatter': 'default'
                            },
                        'file_access_handler':{
                            'class': 'logging.handlers.RotatingFileHandler', # 自动切割
                            'maxBytes': 1024 * 1024 * 20, # 20m 一个日志文件
                            'filename': os.path.join(log_path, time.strftime('%Y_%m_%d',time.localtime())+"_access.log"),  # 日志文件
                            'backupCount': 50, # 最多备份几个
                            'level': 'DEBUG',
                            'formatter': 'file_access', 
                            'encoding': 'utf8'
                            },
                        'file_error_handler':{
                            'class': 'logging.handlers.RotatingFileHandler', # 自动切割
                            'maxBytes': 1024 * 1024 * 20, # 20m 一个日志文件
                            'filename': os.path.join(log_path, time.strftime('%Y_%m_%d',time.localtime())+"_error.log"),  # 日志文件
                            'backupCount': 50, # 最多备份几个
                            'level': 'ERROR',
                            'formatter': 'file_error', 
                            'encoding': 'utf8'
                        }
            },
            'root': {
                    'level': 'DEBUG',
                    'handlers': ['wsgi','file_access_handler','file_error_handler']
            }
})

class Config:
    SQLALCHEMY_RECORD_QUERIES = True
    SQLALCHEMY_NATIVE_UNICODE = 'utf8'  


# 生产环境配置
class ProductionConfig(Config):
    ENV = 'production'
    # 调试模式
    DEBUG = False
    # 测试模式
    TESTING = False
    # mongodb 连接
    MONGOALCHEMY_CONNECTION_STRING='mongodb://127.0.0.1:27017/flask_blog'
    MONGOALCHEMY_DATABASE = 'flask_blog'
    # mysql 连接
    SQLALCHEMY_DATABASE_URI='mysql+pymysql://root:123456@localhost:3306/flask_blog'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    # 域名配置
    SERVER_NAME = 'demo.devops89.cn'
    # 方便apache 部署
    USE_X_SENDFILE = False
    # cookie 会话的安全签名
    SECRET_KEY = b'ab#_2L"3dQ8zc-\xcc]/'
    # 邮件配置
    MAIL_SERVER = 'smtp.yikaobang.com.cn'
    MAIL_PORT = 465 
    MAIL_USE_SSL = True
    MAIL_USERNAME = 'devops@yikaobang.com.cn'
    MAIL_PASSWORD = 'Ykbmail89!@#'
    AA = '2323'
    SECRET_KEY = b'233#_2L"3dQ8zc-\xcc]/'


# 开发环境配置
class DevelopmentConfig(Config):
    ENV = 'development'
    # 调试模式
    DEBUG = True
    # 测试模式
    TESTING = False
    # mongodb 连接
    MONGOALCHEMY_CONNECTION_STRING='mongodb://127.0.0.1:27017/flask_blog'
    MONGOALCHEMY_DATABASE = 'flask_blog'
    # mysql 连接
    SQLALCHEMY_DATABASE_URI="mysql+pymysql://root:123456@127.0.0.1:3306/flask_blog"
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    # 域名配置 正式环境必须配置这个参数
    #SERVER_NAME = 'blog.devops89.cn'
    # 方便apache 部署
    USE_X_SENDFILE = False
    # cookie 会话的安全签名
    SECRET_KEY = b'ab#_2L167dQ8zc-\xcc2c'
    # 邮件配置
    MAIL_SERVER = 'smtp.yikaobang.com.cn'
    MAIL_PORT = 465 
    MAIL_USE_SSL = True
    MAIL_USERNAME = 'devops@yikaobang.com.cn'
    MAIL_PASSWORD = 'Ykbmail89!@#'
    SECRET_KEY = b'ab#_2L"3dQ8zc-\xcc]/'


# 测试配置
class TestingConfig(Config):
    TESTING = True


# 在这里可以配置部署的是生产环境还是开发环境
flask_env_config = {
    'development': DevelopmentConfig,
    'production' : ProductionConfig,
# 开发环境打开这条注释
    'default': DevelopmentConfig
# 生产环境打开这条注释
#    'default': ProductionConfig,
}


# api 通用错误返回码

DEFINE_ERRORS = {
    'UserAlreadyExists': { 
        'code': 401,
        'info' : '用户已经存在',
        'extra': "请检查参数"
    },
    'vAlreadyExistsError1': {
        'info': "导航栏信息已存在",
        'code': 402,
        'extra': "请检查参数"
    },  
    'NavAlreadyExistsError2': {
        'info': "二级导航栏信息已存在",
        'code': 403,
        'extra': "请检查参数"
    },  
    'ServerError': {
        'info':"服务器存在bug!",
        'code': 501,
        'extra':'请联系管理员!'
    }
}
