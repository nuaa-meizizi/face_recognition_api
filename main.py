#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from bottle import *
from face_recog import main,judgeUnknown,saveEncoding
from ml_model import *
import sys
from include.result import *
reload(sys)
sys.setdefaultencoding('utf8')
HTML = """
<!DOCTYPE html>
<html>
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
        <title>定义input type="file" 的样式</title>
        <style type="text/css">
            body{
                font-size:14px;
                align-text:center;
            }
            input{
                vertical-align:middle;
                margin:0;
                padding:0
            }
            .file-box{
                position:relative;
                width:340px;
                margin:0px auto;
            }
            .txt{
                height:22px;
                border:1px solid #cdcdcd;
                width:180px;
            }
            .btn{
                background-color:#FFF;
                border:1px solid #CDCDCD;
                height:24px;
                width:70px;
            }
            .file{
                position:absolute;
                top:0;
                right:80px;
                height:24px;
                filter:alpha(opacity:0);
                opacity: 0;
                width:260px
            }
        </style>
    </head>
    <body>
        <div class="file-box">
            <form action="/upload_know" method="post" enctype="multipart/form-data">
                <input type='text' name='textfield' id='textfield' class='txt' />
                <input type='button' class='btn' value='浏览...' />
                <input type="file" name="fileField" class="file" id="fileField" size="28" onchange="document.getElementById('textfield').value=this.value" />
                <input type="submit" name="submit" class="btn" value="上传" onclick=""/>
            </form>
        </div>
    </body>
</html>
"""


base_path = os.path.dirname(os.path.realpath(__file__))  # 获取脚本路径

""""创建目录"""

upload_path_know = os.path.join(base_path, 'upload/','know')   # 上传文件目录
if not os.path.exists(upload_path_know):
    os.makedirs(upknowload_path_know)

upload_path_tmp = os.path.join(base_path, 'upload/','tmp')   # 上传文件目录
if not os.path.exists(upload_path_tmp):
    os.makedirs(upload_path_tmp)

upload_path_unknown = os.path.join(base_path, 'upload/','unknown')   # 上传文件目录
if not os.path.exists(upload_path_unknown):
    os.makedirs(upload_path_unknown)

upload_path_encoding = os.path.join(base_path, 'upload/','encoding')   # 上传文件目录
if not os.path.exists(upload_path_encoding):
    os.makedirs(upload_path_encoding)

E_MORE_THAN_ONE = -1
NO_FACE = -2

@route('/', method='GET')
@route('/upload_know', method='GET')
@route('/index.html', method='GET')
@route('/upload.html', method='GET')

def index():
    """显示上传页"""
    return HTML

@route('/upload_know', method='POST')
def do_upload_know():
    result=Result()
    result.set_null()
    """处理上传文件"""
    filedata = request.files.get('fileField')
    print filedata
    print filedata.filename
    if filedata.file:

        file_name = os.path.join(upload_path_tmp, filedata.filename)
        if not os.path.exists(file_name):

            print('not exits')
            filedata.save(file_name)  # 上传文件写入
            """判断图片中人脸个数"""
            flag = judgeUnknown(upload_path_tmp, filedata.filename)
            if flag == 1:
                file_name = os.path.join(upload_path_know, filedata.filename.split('.jpg')[0])
                os.makedirs(file_name)
                file_name = os.path.join(file_name, filedata.filename)
                filedata.save(file_name)
                saveEncoding(file_name,upload_path_encoding,output1 = filedata.filename.split('.jpg')[0])
                """训练分类器，有点耗时，可做优化，不如上传n个人脸之后再一起训练"""
                classifier = train("upload/encoding", model_save_path="models/upload/upload.clf", n_neighbors=3)
                return result.success('upload success')
            else:
                os.remove(file_name)
            if flag == E_MORE_THAN_ONE:
                return result.error('E_MORE_THAN_ONE',flag)
            elif flag == NO_FACE:
                return result.error('NO_FACE',flag)
            return result.error('NO_FACE',flag)
        else:
            return result.error('already_upload',2)
    else:
        return result.error('got no pics',-1)

@route('/upload_unknown', method='POST')
def do_upload_unknown():
    result=Result()
    result.set_null()
    """处理上传文件"""
    filedata = request.files.get('fileField')
    if filedata.file:
        file_name = os.path.join(upload_path_unknown, filedata.filename)
        if os.path.exists(file_name)==False:
            filedata.save(file_name)  # 上传文件写入
        flag = judgeUnknown(upload_path_unknown,filedata.filename)
        if flag == E_MORE_THAN_ONE:
            return result.error('E_MORE_THAN_ONE',flag)
        elif flag == NO_FACE:
            return result.error('NO_FACE',flag)
        return result.success('{}'.format(main(upload_path_know,upload_path_unknown,filedata.filename,'models/upload/upload.clf')))
    else:
        return result.error('got no pic',-1)

@route('/train_model',method='GET')
def train_model():
    """可不定期训练KNN模型"""
    result=Result()
    result.set_null()
    classifier = train("upload/know", model_save_path="models/upload/upload.clf", n_neighbors=3)
    return 1

@route('/favicon.ico', method='GET')
def server_static():
    result.set_null()
    result=Result()
    """处理网站图标文件, 找个图标文件放在脚本目录里"""
    return static_file('favicon.ico', root=base_path)

@error(404)
def error404(error):
    result=Result()
    result.set_null()
    """处理错误信息"""
    return '404 发生页面错误, 未找到内容'

 """端口可修改为任意端口，若是部署在云服务器，需要开放相端口(阿里云)"""
run(host='127.0.0.1', port=8080, reloader=True)  # reloader设置为True可以在更新代码时自动重载
