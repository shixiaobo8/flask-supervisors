#!/usr/bin/env python
# -*- coding:utf8 -*-
"""
	restful api route 类和类注册文件
"""
from flask_restful import abort,Resource,reqparse,fields,marshal_with,marshal
# from flask_supervisor.supervisor.models import Nav,subNav
from flask_supervisor import mysql_db
from sqlalchemy import and_
from flask_supervisor.supervisor.models import Host,Group,Node,User
from flask_login import login_user,logout_user,LoginManager
from ..utils import generate_response,CustomFlaskErr
from flask import request,current_app,logging
from flask import jsonify,flash,redirect
from datetime import timedelta
from flask_supervisor import login_manager
from werkzeug.utils import secure_filename
import werkzeug
import time,os

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
            current_app.logger.info("用户"+username+"登录了...")
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

# 用户信息 单个处理类
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
        username = self.json_args['username']
        password = self.json_args['password']
        email = self.json_args['email']
        res_data = ""
        code = '20002'
        is_username = User.query.filter_by(username=username).first()
        is_email = User.query.filter_by(email=email).first()
        if is_username is not None:
            res_data = "用户名已被占用!"
        elif is_email is not None:
            res_data = "邮箱已被使用!"
        else:
            res_data  = "注册用户信息正确!"
            code = '20000'
            new_user = User(username,email,password)
            mysql_db.session.add(new_user)
            mysql_db.session.commit()
        return({"data":res_data,"code":code})

    # 修改一个
    def put(self):
        # 获取request json 参数
        json_args = self.json_args
        # 获取修改参数
        email = json_args['email']
        username = json_args['username']
        password = json_args['password']
        phone = json_args['phone']
        weixin_name = json_args['weixin_name']
        message = "更新成功!"
        code = '20000'
        try:
            user = User.query.filter_by(username=username).first()
            user.email=email
            user.username=username
            user.phone=phone
            user.weixin_name=weixin_name
            user.password_hash=password
            user.last_modify = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
            mysql_db.session.commit()
        except Exception as e:
            print(e)
            code = '20002'
            message = "更新失败!"
        return jsonify({"code":code,'message':message})

    # 删除一个
    def delete(self):
        pass


user_touxiang_fields = {
    'username':fields.String(attribute='username'),
    'touxiang': TouXiangUrl(attribute="avatar")
}

# 用户头像 单个处理类
class UserTouXiangApi(Resource):
    # 请求参数处理
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.args = self.reqparse.parse_args()
        # 获取request json 参数
        self.json_args = request.json
        self.reqparse.add_argument('username', type=str,location='args',required=True)

    # 查询头像信息
    def get(self):
        try:
            args = self.reqparse.parse_args()
            username = args['username']
            # user = User.query.with_entities(User.username,User.avatar).filter_by(username=username).first()
            user_touxiang = mysql_db.session.query(User.avatar).filter_by(username=username).first()
            mysql_db.session.commit()
            return jsonify([{"username":username,"touxiang":user_touxiang[0]}])
        except Exception as e:

            return

    # 上传头像
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('file', type=werkzeug.datastructures.FileStorage, location='files')
        username = request.form['username']
        message = "更新成功!"
        code = '20000'
        # 上传图片
        try:
            # check if the post request has the file part
            if 'file' not in request.files:
                flash('No file part')
                message='No file part'
                return redirect(request.url)
            file = request.files['file']
            # if user does not select file, browser also
            # submit an empty part without filename
            if file.filename == '':
                flash('No selected file')
                message='No selected file'
            if file:
                filename = secure_filename(file.filename)
                print(filename)
                if not os.path.exists(os.getcwd()+os.sep+os.path.join(current_app.config['UPLOAD_FOLDER']+os.sep,username)):
                    os.mkdir(os.getcwd()+os.sep+current_app.config['UPLOAD_FOLDER']+os.sep+username)
                file.save(os.path.join(os.getcwd()+os.sep+current_app.config['UPLOAD_FOLDER']+os.sep+username, filename))
            user = User.query.filter_by(username=username).first()
            user.username = username
            user.avatar=os.path.join(current_app.config['UPLOAD_FOLDER']+os.sep+username, filename).replace("flask_supervisor"+os.sep,'').replace('static'+os.sep,'')
            user.last_modify = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            mysql_db.session.commit()
        except Exception as e:
            print(e)
            code = '20002'
            message = "更新失败!"
        return jsonify({"code": code, 'message': message})

    # 修改头像
    def put(self):
        self.post()

    # 删除头像
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
