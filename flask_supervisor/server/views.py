#!/usr/bin/env python
# -*- coding:utf8 -*-
from flask import render_template,session
from . import server
from flask_login import login_required
from flask_supervisor import socketio,mysql_db
from flask_socketio import emit,send,Namespace
from flask import request,current_app
from flask_supervisor.config import dictConfig
from flask_supervisor.supervisor.models import services_developers,Service,User
from threading import Lock
import logging
thread = None
thread_lock = Lock()



# 主机列表管理
@login_required
@server.route('/serverList')
def index():
    return render_template("server/index.html")


# 服务列表管理
@login_required
@server.route('/serviceList')
def serverList():
    return render_template("server/services.html")


# app 版本管理
@login_required
@server.route('/appVersion.html')
def appVersion():
    return render_template("server/appVersion.html")


# ansible分组管理
@login_required
@server.route('/ansible/manage')
def anisble():
    return render_template("server/ansible_manage.html")


# 发布管理
@login_required
@server.route('/ci-cd')
def cicd():
    return render_template("server/cicd.html")


# webscoket 连接
@socketio.on('connect', namespace='/runtime_logging')
def test_connect():
    print("客户端连接了..")
    # emit('my_response', "client ，你好....")
    operation_log = logging.getLogger("operation_logger").handlers[0].baseFilename
    global thread
    with thread_lock:
        if thread_lock:
            thread = socketio.start_background_task(target=background_thread,logfile=operation_log)

@socketio.on('disconnect',namespace='/runtime_logging')
def test_disconnect():
    print('Client disconnected')

@socketio.on('my_response',namespace='/runtime_logging')
def handle_my_response_runtime_logging_event(data):
    print(data)
    global thread
    with thread_lock:
        if thread_lock:
            thread = socketio.start_background_task(target=background_thread)

@login_required
@server.route("/runtime_logging")
def websockettest():
    # print(logging.getLogger("operation_logger").handlers[0].baseFilename)
    return render_template("server/runtime_logging.html")


# socketio的start_background_task函数用于新建一个线程，处理业务，在线程中在请求上下文中调用收发功能函数
def background_thread(logfile=None):
    """Example of how to send server generated events to clients."""
    with open(logfile,"r", encoding='UTF-8') as f:
        while True:
            socketio.sleep(3)
            for line in f.readlines():
                # 注意：这里不需要客户端连接的上下文，默认 broadcast = True ！！！！！！！
                socketio.emit('my_response',{'line': line},namespace='/runtime_logging')