#!/usr/bin/env python
# -*- coding:utf8 -*-
"""
	flask-scripts 定制脚本文件
	
"""
from flask_script import Command

class Hello(Command):

    def run(self):
        print("hello,flask_scripts")

