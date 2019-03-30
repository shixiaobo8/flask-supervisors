#!/usr/bin/env python
# -*- coding:utf8 -*-
from flask import render_template,request, make_response, url_for,current_app,jsonify,g
from . import backend


@backend.route('/addFNav',methods=('POST',))
def addFNavs1():
    res = dict()
    res['code'] = 200
    res['data'] = 'ok'
    return jsonify(res)


@backend.route('/')
def index():
    return render_template("houtai/index.html")


