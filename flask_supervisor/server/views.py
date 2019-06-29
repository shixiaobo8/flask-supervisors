#!/usr/bin/env python
# -*- coding:utf8 -*-
from flask import render_template
from . import server
from flask_login import login_required
from flask_supervisor import socketio
from flask_socketio import emit,send,Namespace



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


class MyCustomNamespace(Namespace):
    def on_connect(self):
        print("有客户端连接了")

    def on_disconnect(self):
        print("有客户端退出连接了...")

    def on_my_event(self, data):
        emit('my_response', data)

socketio.on_namespace(MyCustomNamespace('/websocket'))


# webscoket 连接
# @socketio.on("json")
# def handle_json(json):
#     print('received json: ' + str(json))
#
# @socketio.on('connect', namespace='/websocket')
# def test_connect():
#     emit('my response', {'data': 'Connected'})
#
# @socketio.on('disconnect')
# def test_disconnect():
#     print('Client disconnected')