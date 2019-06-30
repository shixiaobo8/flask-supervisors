#!/usr/bin/env python
# -*- coding:utf8 -*-
from flask import render_template
from . import server
from flask_login import login_required
from flask_supervisor import socketio
from flask_socketio import emit,send,Namespace
from flask import request,current_app



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


# ansible分组管理
@login_required
@server.route('/ansible/manage')
def anisble():
    return render_template("server/ansible_manage.html")


# ansible分组管理
@login_required
@server.route('/ci-cd')
def cicd():
    return render_template("server/cicd.html")

#
# class MyCustomNamespace(Namespace):
#     def on_connect(self):
#         print("有客户端连接了...")
#         send_message = "你好client"
#         print("向客户端发送消息"+ send_message)
#         emit('my_response', send_message)
#
#     def on_disconnect(self):
#         print("有客户端退出连接了...")
#
#     def on_my_event(self, data):
#         print(data)
#         emit('my_response', data+"11111111166000011")
#
# socketio.on_namespace(MyCustomNamespace('/testwebsocket'))

# webscoket 连接
@socketio.on('connect', namespace='/testwebsocket')
def test_connect():
    print("客户端连接了..")
    emit('my_response', "client ，你好....")

@socketio.on('disconnect',namespace='/testwebsocket')
def test_disconnect():
    print('Client disconnected')

@socketio.on('my_response',namespace='/testwebsocket')
def handle_my_response_testwebsocket_event(data):
    print("my_event")
    emit("my_response",data)
    print(data)
    # import time
    # #进行一些对value的处理或者其他操作,在此期间可以随时会调用emit方法向前台发送消息
    # emit('my_response',{'code':'200','msg':'start to process...'})
    # time.sleep(5)
    # emit('my_response',{'code':'200','msg':'processed111'})

@login_required
@server.route("/testwebsocket")
def websockettest():
    return render_template("server/testwebsocket.html")
