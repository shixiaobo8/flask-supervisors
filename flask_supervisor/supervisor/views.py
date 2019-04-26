#!/usr/bin/env python
# -*- coding:utf8 -*-
from flask import render_template,current_app
from . import supervisor
from flask_login import login_required


# 创建一个视图应用,博客首页
@supervisor.route('/',methods=('GET','POST'))
@login_required
def index():
    return render_template('base/frame_boot_base.html')


@supervisor.route('/test')
def test():
    return render_template("houtai/index.html")
