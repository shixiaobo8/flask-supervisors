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
# 导入 sqlAlchemy python orm 模块
from flask_sqlalchemy import SQLAlchemy
# 导入 sqlAlchemy mongo orm 模块
from flask_mongoalchemy import MongoAlchemy
# 导入 falsk_migrate
from flask_migrate import Migrate
# 导入flask restfull api
from flask_restful import Api
# 导入配置文件全局环境变量
from flask_supervisor.config import flask_env_config
import os

# 初始化mysql数据库连接
mysql_db = SQLAlchemy()
# 初始化mongo数据库连接
mongo_db = MongoAlchemy()
migrate = Migrate()

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
    # 初始化mysql据库migrate
    migrate.init_app(app,mysql_db,directory=os.path.abspath(os.path.dirname(__file__))+os.sep+"migrations")
    # 导入自定义蓝图模块
    from .supervisor import supervisor as supervisor_bp
    # 注册蓝图
    app.register_blueprint(supervisor_bp,url_prefix='/supervisor')
    app.add_url_rule('/',endpoint='supervisor.index')
    from .backend import backend as backend_bp
    app.register_blueprint(backend_bp,url_prefix='/houtai')
    return app
