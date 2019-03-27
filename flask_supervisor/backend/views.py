#!/usr/bin/env python
# -*- coding:utf8 -*-
from flask import render_template,request, make_response, url_for,current_app,jsonify,g
from . import backend
import os,datetime,random


json_test={
        "code": 0
        ,"msg": ""
        ,"count": 3000000
        ,"data": [{
            "id": "10001"
            ,"username": "杜甫"
            ,"email": "xianxin@layui.com"
            ,"sex": "男"
            ,"city": "浙江杭州"
            ,"sign": "点击此处，显示更多。当内容超出时，点击单元格会自动显示更多内容。"
            ,"experience": "116"
            ,"ip": "192.168.0.8"
            ,"logins": "108"
            ,"joinTime": "2016-10-14"
            }, {
                "id": "10002"
                ,"username": "李白"
                ,"email": "xianxin@layui.com"
                ,"sex": "男"
                ,"city": "浙江杭州"
                ,"sign": "君不见，黄河之水天上来，奔流到海不复回。 君不见，高堂明镜悲白发，朝如青丝暮成雪。 人生得意须尽欢，莫使金樽空对月。 天生我材必有用，千金散尽还复来。 烹羊宰牛且为乐，会须一饮三百杯。 岑夫子，丹丘生，将进酒，杯莫停。 与君歌一曲，请君为我倾耳听。(倾耳听 一作：侧耳听) 钟鼓馔玉不足贵，但愿长醉不复醒。(不足贵 一作：何足贵；不复醒 一作：不愿醒/不用醒) 古来圣贤皆寂寞，惟有饮者留其名。(古来 一作：自古；惟 通：唯) 陈王昔时宴平乐，斗酒十千恣欢谑。 主人何为言少钱，径须沽取对君酌。 五花马，千金裘，呼儿将出换美酒，与尔同销万古愁。"
                ,"experience": "12"
                ,"ip": "192.168.0.8"
                ,"logins": "106"
                ,"joinTime": "2016-10-14"
                ,"LAY_CHECKED": True
                }, {
                    "id": "10003"
                    ,"username": "王勃"
                    ,"email": "xianxin@layui.com"
                    ,"sex": "男"
                    ,"city": "浙江杭州"
                    ,"sign": "人生恰似一场修行"
                    ,"experience": "65"
                    ,"ip": "192.168.0.8"
                    ,"logins": "106"
                    ,"joinTime": "2016-10-14"
                    }, {
                        "id": "10004"
                        ,"username": "李清照"
                        ,"email": "xianxin@layui.com"
                        ,"sex": "女"
                        ,"city": "浙江杭州"
                        ,"sign": "人生恰似一场修行"
                        ,"experience": "666"
                        ,"ip": "192.168.0.8"
                        ,"logins": "106"
                        ,"joinTime": "2016-10-14"
                        }, {
                            "id": "10005"
                            ,"username": "冰心"
                            ,"email": "xianxin@layui.com"
                            ,"sex": "女"
                            ,"city": "浙江杭州"
                            ,"sign": "人生恰似一场修行"
                            ,"experience": "86"
                            ,"ip": "192.168.0.8"
                            ,"logins": "106"
                            ,"joinTime": "2016-10-14"
                            }, {
                                    "id": "10006"
                                    ,"username": "贤心"
                                    ,"email": "xianxin@layui.com"
                                    ,"sex": "男"
                                    ,"city": "浙江杭州"
                                    ,"sign": "人生恰似一场修行"
                                    ,"experience": "12"
                                    ,"ip": "192.168.0.8"
                                    ,"logins": "106"
                                    ,"joinTime": "2016-10-14"
                                    }, {
                                            "id": "10007"
                                            ,"username": "贤心"
                                            ,"email": "xianxin@layui.com"
                                            ,"sex": "男"
                                            ,"city": "浙江杭州"
                                            ,"sign": "人生恰似一场修行"
                                            ,"experience": "16"
                                            ,"ip": "192.168.0.8"
                                            ,"logins": "106"
                                            ,"joinTime": "2016-10-14"
                                            }, {
                                                    "id": "10008"
                                                    ,"username": "贤心"
                                                    ,"email": "xianxin@layui.com"
                                                    ,"sex": "男"
                                                    ,"city": "浙江杭州"
                                                    ,"sign": "人生恰似一场修行"
                                                    ,"experience": "106"
                                                    ,"ip": "192.168.0.8"
                                                    ,"logins": "106"
                                                    ,"joinTime": "2016-10-14"
                                                                                                                                                                                                                                 }]
                                                                                                                                                                                                                    }  


@backend.route('/list_comment',methods=('GET','POST'))
def get_list_comments():
    return jsonify(json_test)


@backend.route('/addNavModal.html')
def test():
    return render_template('houtai/addNavModal.html')


@backend.route('/addFNav',methods=('POST',))
def addFNavs1():
    res = dict()
    res['code'] = 200
    res['data'] = 'ok'
    return jsonify(res)


@backend.route('/list_navs',methods=('GET','POST'))
def listNavs():
    print(g)
    return jsonify(g.get('navs'))


@backend.route('/system_settings')
def sys_settings():
    return render_template('houtai/system.html')


@backend.route('/')
def index():
    return render_template("houtai/index.html")


@backend.route('/comment')
def comment_list():
    return render_template("blog/comment_list.html")


def gen_rnd_filename():
    filename_prefix = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    return '%s%s' % (filename_prefix, str(random.randrange(1000, 10000)))


@backend.route('/edit',methods=('GET','POST'))
def edit():
    error = ''
    url = ''
    filename = ''
    """CKEditor file upload"""
    callback = request.args.get("CKEditorFuncNum")
    if request.method == 'GET': 
    	return render_template('blog/edit.html')
    elif request.method == 'POST' and 'upload' not in request.files:
        title = request.form.get('subject')
        data = request.form.get('content')
        post = Post(title=title,body=data)
        category = Category()
        post.save()
        response = make_response(data)
        response.headers["Content-Type"] = "text/html"
        return response
    elif request.method == 'POST' and 'upload' in request.files:
        fileobj = request.files['upload']
        fname, fext = os.path.splitext(fileobj.filename)
        rnd_name = '%s%s' % (gen_rnd_filename(), fext)
        filepath = os.path.join(current_app.static_folder, 'upload', rnd_name)
        # 检查路径是否存在，不存在则创建
        dirname = os.path.dirname(filepath)
        if not os.path.exists(dirname):
            try:
                os.makedirs(dirname)
            except:
                error = 'ERROR_CREATE_DIR'
        elif not os.access(dirname, os.W_OK):
            error = 'ERROR_DIR_NOT_WRITEABLE'
        if not error:
            fileobj.save(filepath)
            filename = '%s/%s' % ('upload', rnd_name)
            url = url_for('static', filename=filename)
    else:
        error = 'post error'
    res = """

<script type="text/javascript">
  window.parent.CKEDITOR.tools.callFunction(%s, '%s', '%s');
</script>

""" % (callback, url, error)
    response = make_response(res)
    response.headers["Content-Type"] = "text/html"
    return jsonify(uploaded=1, url=url, filename=filename)
    #return response
