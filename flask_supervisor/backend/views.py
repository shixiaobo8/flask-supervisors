#!/usr/bin/env python
# -*- coding:utf8 -*-
from flask import render_template,request, make_response, url_for,current_app,jsonify,g
from . import backend
from flask_login import login_required,logout_user,current_user
from flask import redirect
from flask_supervisor.supervisor.models import  User

# 注册页面
@backend.route('/register')
def register():
    return render_template("houtai/reg.html")


# 登陆首页
@login_required
@backend.route('/')
def index():
    return render_template("houtai/index.html")

# 退出登陆
@backend.route('/Logout',methods=('GET','POST'))
@login_required
def logout():
    logout_user()
    return redirect("/houtai")


# 修改用户信息
@backend.route('/userinfo',methods=('GET','POST'))
@login_required
def userInfo():
    return  render_template("index/user/userInfo.html")