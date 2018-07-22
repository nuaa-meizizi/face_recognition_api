# -*- coding: utf-8 -*-
from bottle import route, run
import sys
reload(sys)
sys.setdefaultencoding('utf8')
@route('/hello')
def  hello ():
    return "Hello World！"


run (host = 'localhost' , port = 8082 , debug = True )