#!/usr/bin/env python
# -*- coding:utf8 -*-
from flask import render_template
from . import server
from flask_login import login_required



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