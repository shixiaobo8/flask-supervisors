#!/usr/bin/env python
# -*- coding:utf8 -*-
from  flask import Blueprint

# 创建蓝图
supervisor = Blueprint('supervisor',__name__)

from . import views
