#!/usr/bin/env python
# -*- coding:utf-8 -*-
from flask import jsonify,make_response,request,g,session,redirect,url_for,flash
from flask_supervisor import create_app
from flask_script import Manager,Server,Shell
from flask_supervisor.commands import Hello
from flask_migrate import MigrateCommand
from flask import current_app
# 导入自定义错误类
from flask_supervisor.utils import CustomFlaskErr
# 导入所有migrate需要操作的model 类
from flask_supervisor.supervisor.models import *
import os
import werkzeug

def _make_context(app):
    return dict(app=app)


# 创建一个flask app 应用 并初始化
supervisor_app = create_app(flask_env=os.getenv('FLASK_ENV') or 'default')


#初始化shell
def _make_context():
    return dict(app=supervisor_app)


manager = Manager(supervisor_app)
# 添加shell 命令交互器
manager.add_command("shell", Shell(make_context=_make_context),user_ipython=True)
# 添加hello 打印命令测试
manager.add_command("hello", Hello())
# 添加执行server命令
manager.add_command("runserver",Server())
# 添加数据 migrate 工具
manager.add_command('db',MigrateCommand)


# 自定义错误
@supervisor_app.errorhandler(CustomFlaskErr)
def handle_flask_error(error):
    # response 的 json 内容为自定义错误代码和错误信息
    response = jsonify(error.to_dict())
    # response 返回 error 发生时定义的标准错误代码
    response.status_code = error.status_code
    return response


# 404  错误
@supervisor_app.errorhandler(404)
def not_found(error):
         return make_response(jsonify({'error': 'Not found'}), 404)


#  500 错误
@supervisor_app.errorhandler(500)
def inter_server_error(e):
    supervisor_app.logger.error('error 500: %s', e)
    return make_response(jsonify({'error': 'server internet error'}), 500)


# 应用情景
# session 会话过期
@supervisor_app.before_request
def checkSession():
    if not session.get('username'):
        flash("session会话过期,请手动刷新重新登陆!")


# 第一次请求的时候做初始化导航栏nav数据
# @supervisor_app.before_first_request
# def print_request_info():
#     supervisor_app.logger.info("启动项目中,正在初始化导航栏nav....")
#     navs = Nav.query.all()
#     g.navs= navs
#     print("=====")
#     print(navs)


#def get_db():
#    if 'db' not in g:
#        g.db = connect_to_database()
#    return g.db

#@supervisor_app.teardown_appcontext
#def teardown_db():
#    db = g.pop('db', None)
#    if db is not None:
#        db.close()


if __name__ == "__main__":
    manager.run()
