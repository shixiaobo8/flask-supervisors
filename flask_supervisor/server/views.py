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