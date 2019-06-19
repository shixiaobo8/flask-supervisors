#!/usr/bin/env python
# -*- coding:utf8 -*-
"""
	restful api route 类和类注册文件
"""
from flask_restful import abort,Resource,reqparse,fields,marshal_with,marshal
# from flask_supervisor.supervisor.models import Nav,subNav
from flask_supervisor import mysql_db
from sqlalchemy import and_,or_
from sqlalchemy.orm import joinedload,contains_eager,subqueryload
from flask_supervisor.supervisor.models import Host,Group,Node,User,Nav,subNav
from flask_login import login_user,logout_user,LoginManager
from ..utils import generate_response,CustomFlaskErr
from flask import request,current_app,logging
from flask import jsonify,flash,redirect,session
from datetime import timedelta
from flask_supervisor import login_manager
from werkzeug.utils import secure_filename
import werkzeug
import time,os

def getUserTouxiang(username):
    user_touxiang = mysql_db.session.query(User.avatar).filter_by(username=username).first()[0]
    return "/static/" + user_touxiang

def getUserNavList(username):
    subnavs = mysql_db.session.query(Nav).filter(Nav.is_del==0).join(subNav,Nav.id==subNav.nav_Id,isouter=True).filter(subNav.is_del==0).all()
    return marshal(subnavs,Nav_fields)

class TouXiangUrl(fields.Raw):
    def format(self, value):
        return "/static/" + value;

class NavType(fields.Raw):
    def format(self, value):
        if value:
            return '前台'
        else:
            return '后台'

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
            session["navs"] = getUserNavList(username)
            session["touxiang"] = getUserTouxiang(username)
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


# 导航栏 单个处理类
class NavApi(Resource):
    # 请求参数处理
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.args = self.reqparse.parse_args()
        # 获取request json 参数
        self.json_args = request.json
        super(NavApi, self).__init__()

    # 查询单个
    def get(self):
        return self.args

    # 新增一个
    def post(self):
        # 获取request json 参数
        json_args = self.json_args
        # 获取二级导航栏参数
        nav_name = json_args['nav_name']
        nav_type = json_args['nav_type']
        if nav_type == '前台':
            nav_type = 1
        elif nav_type == '后台':
            nav_type = 0
        subnav_url = json_args['subnav_url']
        subnav_name = json_args['subnav_name']
        # 查询是否含有相同的一级导航栏
        exists_fName = Nav.query.filter_by(navTitle=nav_name).first()
        firstNav = Nav(nav_name, '', nav_type, 1)
        sub_nav = subNav(subnav_name, subnav_url)
        # 检查是否含有存在的二级菜单
        exists_sNav = subNav.query.filter(or_(subNav.title == subnav_name, subNav.nav_url == subnav_url)).first()
        if exists_sNav:
            current_app.logger.error("查询出错: 已存在相同的二级导航栏信息")
            raise CustomFlaskErr("NavAlreadyExistsError2")
        # 先添加一级菜单,然后关联二级菜单
        if not exists_fName:
            mysql_db.session.add(sub_nav)
            # 关联二级菜单
            firstNav.subnavs.append(sub_nav)
            mysql_db.session.add(firstNav)
            mysql_db.session.commit()
        else:
            sub_nav.nav_Id=exists_fName.id
            mysql_db.session.add(sub_nav)
            mysql_db.session.commit()
        return generate_response(data=json_args)

    # 修改一个
    def put(self):
        # 获取request json 参数
        json_args = self.json_args
        # 获取二级导航栏参数
        nav_name = json_args['nav_name']
        nav_type = json_args['nav_type']
        subnav_id = json_args['id']
        nav_id = json_args['nav_id']
        if nav_type == '前台':
            nav_type = 1
        elif nav_type == '后台':
            nav_type = 0
        subnav_url = json_args['subnav_url']
        subnav_name = json_args['subnav_name']
        # 查询是否含有相同的一级导航栏
        exists_fName = Nav.query.filter_by(id=nav_id).first()
        # 检查是否含有存在的二级菜单
        exists_sNav = subNav.query.filter_by(id=subnav_id).first()
        try:
            # 修改数据库信息
            exists_sNav.title = subnav_name
            exists_sNav.nav_url = subnav_url
            exists_fName.nav_name = nav_name
            exists_fName.nav_type = nav_type
            mysql_db.session.commit()
            return {'code': 20000, 'message': "更新成功!"}
        except Exception as e:
            message = "更新失败:" + str(e)
            return {'code': 20002, 'message': message}



    # 删除一个
    def delete(self):
        # 获取request json 参数
        json_args = self.json_args
        # 获取二级导航栏参数
        subnav_id = json_args['subnav_id']
        # 检查是否含有存在的二级菜单
        exists_sNav = subNav.query.filter_by(id=subnav_id).first()
        try:
            # 修改数据库信息
            exists_sNav.is_del = 1
            mysql_db.session.commit()
            return {'code': 20000, 'message': "删除成功!"}
        except Exception as e:
            message = "删除失败:" + str(e)
            return {'code': 20002, 'message': message}


# 输出字段
subNav_fields = {
    'subnav_name':fields.String(attribute='title'),
    'subnav_url': fields.String(attribute='nav_url'),
}

Nav_fields = {
    'id':fields.Integer,
    'nav_name':fields.String(attribute='navTitle'),
    'nav_type':NavType(attribute='navType'),
    'url': fields.String(attribute='navUrl'),
    'subnavs': fields.List(fields.Nested(subNav_fields,allow_null=True,default=''),default='')
}

# 导航栏nav 处理列表类
class NavListApi(Resource):

    # 请求参数处理
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('currentPage', type = int, default=1, location='args',help='第几个分页')
        self.reqparse.add_argument('page_size', type = int, default=10 , location='args',help='每页显示多少')
        # 获取request json 参数
        self.json_args = request.json
        super(NavListApi,self).__init__()

    # 获取(查询)nav 列表
    #@marshal_with(Nav_fields,envelope='Nav')
    def get(self):
        args = self.reqparse.parse_args()
        print(args)
        page_index = args['currentPage']
        page_size = args['page_size']
        # # 先获取所有满足条件的nav isouter=True 表示left join all 方法得到一个列表,这里不使用paginate,会报错
        # navall = mysql_db.session.query(Nav).filter(Nav.is_del==0).join(subNav,Nav.id==subNav.nav_Id,isouter=True).all()
        # navall = mysql_db.session.query(subNav).join(subNav.nav_Id).filter(Nav.is_del==0).options(contains_eager(Nav.subnavs)).all()
        # navall = mysql_db.session.query(Nav).options(joinedload(Nav.subnavs)).filter(Nav.is_del==0).all()
        # navall = mysql_db.session.query(subNav).options(subqueryload(subNav.nav_Id)).filter(Nav.is_del==0).all()
        navall = mysql_db.session.query(subNav.id,Nav.id,subNav.title,subNav.nav_url,Nav.navTitle,Nav.navType,Nav.navUrl).filter(Nav.is_del==0).join(subNav,Nav.id==subNav.nav_Id,isouter=True).filter(subNav.is_del==0).all()
        # sql = '''select `sv_subnavs`.*,`sv_navs`.navTitle,`sv_navs`.navType from sv_subnavs  LEFT JOIN `sv_navs` on `sv_subnavs`.nav_Id = `sv_navs`.id where sv_subnavs.`is_del` = 0;'''
        # navall = mysql_db.session.query(sql)
        # 分页
        page_navs = navall[(page_index-1)*page_size:page_size*page_index]
        res_obj=[]
        for nav in page_navs:
            new_nav_obj = {}
            new_nav_obj['id'] = nav[0]
            new_nav_obj['nav_id'] = nav[1]
            new_nav_obj['subnav_name'] = nav[2]
            new_nav_obj['subnav_url'] = nav[3]
            new_nav_obj['nav_name'] = nav[4]
            if nav[5]:
                new_nav_obj['nav_type'] = 1
            else:
                new_nav_obj['nav_type'] = 0
            new_nav_obj['nav_url'] = nav[6]
            res_obj.append(new_nav_obj)
        return {'code':0,'count':len(navall),'cureent_page':page_index,"page_size":page_size,'data':res_obj}
        # return {"count": 1, "current_page": 1, "page_sizes": 10,
            # "data": [{"nav_name": "test", "nav_type": "qian", "subnav_name": "sfdasf", "subnav_url": "/test/test"},{"nav_name": "test", "nav_type": "qian", "subnav_name": "sfdasf", "subnav_url": "/test/test"}]}

    # 修改多个nav列表
    def post(self):
        return 'post test'

    # 增加多个列表
    def put(self):
        args = self.reqparse.parse_args()
        return {"data":args}

    # 删除多个列表
    def delete(self):
        # 获取request json 参数
        json_args = self.json_args
        # 获取二级导航栏参数
        delete_data = json_args['delete_data']
        ids = [ data['id'] for data in delete_data ]
        try:
            # 修改数据库信息
            for id in ids:
                subNav.query.filter(subNav.id==id).update({"is_del":1})
            mysql_db.session.commit()
            return {'code': 20000, 'message': "删除成功!"}
        except Exception as e:
            message = "删除失败:" + str(e)
            return {'code': 20002, 'message': message}
