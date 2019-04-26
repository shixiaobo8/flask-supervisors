#!/usr/bin/env python
# -*- coding:utf8 -*-
"""
	restful api route 类和类注册文件
"""
from flask_restful import abort,Resource,reqparse,fields,marshal_with,marshal
# from flask_supervisor.supervisor.models import Nav,subNav
# from .. import mysql_db
from sqlalchemy import and_
from flask_supervisor.supervisor.models import Host,Group,Node,User
from flask_login import login_user,logout_user,LoginManager
from ..utils import generate_response,CustomFlaskErr
from flask import request,current_app
from flask import jsonify
from datetime import timedelta
from flask_supervisor import login_manager

class TouXiangUrl(fields.Raw):
    def format(self, value):
        return "/static/" + value;

@login_manager.user_loader
def load_user(userid):
    return User.query.get(int(userid))

class LoginApi(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.json_args = request.json
        self.reqparse.add_argument('username', type=str, required=True,
                                   help='用户名或密码不正确', location='json')
        self.reqparse.add_argument('password', type=str, required=True,
                                   help='用户名或密码不正确', location='json')

    # 登录查询
    def post(self):
        username = self.json_args['username']
        password = self.json_args['password']
        res_data = "ok"
        code = '20000'
        user = User.query.filter(and_(User.username==username,User.password_hash==password)).first()
        if user:
            login_user(user,duration=timedelta(minutes=1))
        if not user:
            res_data  = "not ok"
            code = '20002'
        return({"data":res_data,"code":code})


user_fields = {
    'id':fields.Integer(attribute='id'),
    'username':fields.String(attribute='username'),
    'weixin':fields.String(attribute='weixin_name'),
    'email': fields.String(attribute='email'),
    'password': fields.String(attribute='password_hash'),
    'phone':fields.String(attribute='phone'),
    'ctime': fields.DateTime(dt_format='iso8601',attribute='join_date'),
    'mtime': fields.DateTime(dt_format='iso8601', attribute='last_modify'),
    'touxiang': TouXiangUrl(attribute="avatar")
}

# 导航栏 单个处理类
class UserApi(Resource):
    # 请求参数处理
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.args = self.reqparse.parse_args()
        # 获取request json 参数
        self.json_args = request.json
        self.reqparse.add_argument('username', type=str,location='args')

    # 查询单个
    def get(self):
        args = self.reqparse.parse_args()
        username = args['username']
        user=User.query.filter_by(username=username).first()
        return jsonify([marshal(user,user_fields)])


    # 增加一个
    def post(self):
        pass

    # 修改一个
    def put(self):
        # 获取request json 参数
        json_args = self.json_args
        # 获取二级导航栏参数
        sNavs = json_args['sNavs']
        # 查询是否含有相同的菜单名称和url
        # exists_fName = Nav.query.filter_by(navTitle=json_args['fNavName']).first()
        # exists_fUrl = ''
        # if json_args['fNavUrl'] != '':
        #     exists_fUrl = Nav.query.filter_by(navUrl=json_args['fNavUrl']).first()
        # if exists_fUrl or exists_fName:
        #     current_app.logger.error("查询出错: 已存在相同的一级导航栏信息")
        #     raise CustomFlaskErr("vAlreadyExistsError1")
        # else:
        #     # 先添加一级菜单,然后关联二级菜单
        #     firstNav = Nav(json_args['fNavName'],json_args['fNavUrl'],int(json_args['type']),int(json_args['navPris'][0]))
        #     for secondNav in sNavs:
        #         # 检查是否含有存在的二级菜单
        #         exists_sNav = subNav.query.filter_by(title=secondNav['sNavName'],nav_url=secondNav['sNavUrl']).first()
        #         if exists_sNav:
        #             current_app.logger.error("查询出错: 已存在相同的二级导航栏信息")
        #             raise CustomFlaskErr("NavAlreadyExistsError2")
        #         else:
        #             sub_nav = subNav(secondNav['sNavName'],secondNav['sNavUrl'])
        #             mysql_db.session.add(sub_nav)
        #             # 关联二级菜单
        #             firstNav.subnavs.append(sub_nav)
        #     mysql_db.session.add(firstNav)
        #     mysql_db.session.commit()
        # return generate_response(data=json_args)

    # 删除一个
    def delete(self):
        pass


# 输出字段
subNav_fields = {
    'subtitle':fields.String(attribute='title'),
    'suburl': fields.String(attribute='nav_url'),
}

Nav_fields = {
    'id':fields.Integer,
    'title':fields.String(attribute='navTitle'),
    'type':fields.Integer(attribute='navType'),
    'url': fields.String(attribute='navUrl'),
    'subnavs': fields.List(fields.Nested(subNav_fields,allow_null=True,default=''),default='')
}

# 导航栏nav 处理列表类
class NavListApi(Resource):

    # 请求参数处理
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('page', type = int, default=1, location='args',help='第几个分页')
        self.reqparse.add_argument('limit', type = int, default=10 , location='args',help='每页显示多少')
        super(NavListApi,self).__init__()

    # 获取(查询)nav 列表
    #@marshal_with(Nav_fields,envelope='Nav')
    def get(self):
        args = self.reqparse.parse_args()
        page_index = args['page']
        page_size = args['limit']
        # # 先获取所有满足条件的nav isouter=True 表示left join all 方法得到一个列表,这里不使用paginate,会报错
        # navall = mysql_db.session.query(Nav).filter(Nav.is_del==0).join(subNav,Nav.id==subNav.nav_Id,isouter=True).all()
        # 分页
        # page_navs = navall[(page_index-1)*page_size:page_size*page_index]
        return {'code':0,'count':len(navall),'cureent_page':page_index,"page_size":page_size,'data':marshal(page_navs,Nav_fields)}

    # 修改多个nav列表
    def post(self):
        return 'post test'

    # 增加多个列表
    def put(self):
        args = self.reqparse.parse_args()
        return {"data":args}

    # 删除多个列表
    def delete(self):
        pass
