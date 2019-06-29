#!/usr/bin/env python
# -*- coding:utf8 -*-
"""
	flask 启动参数
"""
# 导入Falsk 应用
from flask import Flask, jsonify
# 导入模板应用
from flask import render_template
# 导入falsk bootstrap 应用
from flask_bootstrap import Bootstrap
# 导入 flask_sqlalchemy orm 模块
from flask_sqlalchemy import SQLAlchemy
# 导入 sqlAlchemy mongo orm 模块
from flask_mongoengine import MongoEngine
# 导入 falsk_migrate
from flask_migrate import Migrate
# 导入flask-socketio
from flask_socketio import SocketIO
# 导入flask restfull api
from flask_restful import Api
# 导入配置文件全局环境变量
from flask_supervisor.config import flask_env_config
import os
# 登陆会话
from flask_login import LoginManager
from flask import session
from datetime import timedelta


# 初始化socketio
async_mode = None
socketio = SocketIO()
# 初始化mysql数据库连接
mysql_db = SQLAlchemy()
# 初始化mongo数据库连接
mongo_db = MongoEngine()
migrate = Migrate()
login_manager = LoginManager()
#登陆认证的处理视图
login_manager.login_view='backend.index'
#登陆提示信息
login_manager.login_message=u'对不起，您还没有登录'
login_manager.login_message_category='info'
# 登陆会话保护
login_manager.session_protection = "strong"
#

# 定义一个创建app应用并且初始化的方法
def create_app(flask_env='default'):
    # 创建flask应用
    app = Flask(__name__)
    app.config.from_object(flask_env_config[flask_env])
    # 初始化bootstrap
    Bootstrap(app)
    # 初始化mysql数据库连接
    mysql_db.init_app(app)
    # 初始化mongo数据库连接
    mongo_db.init_app(app)
    # 初始化socketio
    socketio.init_app(app,async_mode=async_mode)
    # 初始化 登陆
    login_manager.init_app(app)
    # 初始化mysql据库migrate
    migrate.init_app(app,mysql_db,directory=os.path.abspath(os.path.dirname(__file__))+os.sep+"migrations")
    # 导入自定义蓝图模块
    from .supervisor import supervisor as supervisor_bp
    # session 会话期限设置
    app.permanent_session_lifetime = timedelta(hours=1)
    # cookie 有限期设置
    # login_manager._update_remember_cookie()
    # 注册蓝图
    app.register_blueprint(supervisor_bp,url_prefix='/supervisor')
    app.add_url_rule('/',endpoint='supervisor.index')
    from .backend import backend as backend_bp
    app.register_blueprint(backend_bp,url_prefix='/houtai')
    from .server import server as server_bp
    app.register_blueprint(server_bp, url_prefix='/server')
    return app