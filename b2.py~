#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from bottle import *
from face_recog import main
import sys
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
 
upload_path_know = os.path.join(base_path, 'upload/','know')   # 上传文件目录
if not os.path.exists(upload_path_know):
    os.makedirs(upload_path_know)
 
upload_path_unknown = os.path.join(base_path, 'upload/','unknown')   # 上传文件目录
if not os.path.exists(upload_path_unknown):
    os.makedirs(upload_path_unknown)
 
 
@route('/', method='GET')
@route('/upload_know', method='GET')
@route('/index.html', method='GET')
@route('/upload.html', method='GET')
def index():
    """显示上传页"""
    return HTML
 
 
@route('/upload_know', method='POST')
def do_upload_know():
    """处理上传文件"""
    filedata = request.files.get('fileField')
    print filedata.file
    if filedata.file:
        file_name = os.path.join(upload_path_know, filedata.filename)
        try:
            filedata.save(file_name)  # 上传文件写入
            getAllImages(upload_path_know)
        except IOError:
            return '2'
        return '1'
    else:
        return '-1'
@route('/upload_unknown', method='POST')
def do_upload_unknown():
    """处理上传文件"""
    filedata = request.files.get('fileField')
     
    if filedata.file:
        file_name = os.path.join(upload_path_unknown, filedata.filename)
        try:
            filedata.save(file_name)  # 上传文件写入
            return '{}'.format(main(upload_path_know,upload_path_unknown,filedata.filename))
        except IOError:
			return '{}'.format(main(upload_path_know,upload_path_unknown,filedata.filename))

    else:
        return '-1'
 
@route('/favicon.ico', method='GET')
def server_static():
    """处理网站图标文件, 找个图标文件放在脚本目录里"""
    return static_file('favicon.ico', root=base_path)
 
 
@error(404)
def error404(error):
    """处理错误信息"""
    return '404 发生页面错误, 未找到内容'
 
run(host='192.168.152.129', port=8080, reloader=True)  # reloader设置为True可以在更新代码时自动重载
