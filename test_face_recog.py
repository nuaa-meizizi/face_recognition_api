# -*- coding: utf-8 -*-
from face_recog import *

def test(pathknow,pathunknown):
    Encodings_1,Image_name_1 = getAllImagesFromFile(pathknow,output1 = 'data_test_konw_1.pkl',output2 = 'data_test_know_2.pkl')
    Encodings_2,Image_name_2 = getAllImagesFromFile(pathunknown,output1 = 'data_test_unknown_1.pkl',output2 = 'data_test_unknown_2.pkl')

    # unknown_encoding = getUnknownImage(pathunknown,unknownfilwname)
    t_rate_10 = 0
    f_q = []
    i = 0
    for unknown_encoding in Encodings_2:
        results,distances = getCompareResult(Encodings_1,unknown_encoding,0.6)
        
        result = getResult(results,distances)
        for r in result:
          if Image_name_1[r] == Image_name_2[i]:
             t_rate_10 = t_rate_10 + 1
        i = i + 1
#        if i == 30 : break
    print t_rate_10
    print f_q

base_path = os.path.dirname(os.path.realpath(__file__))  # 获取脚本路径
 
upload_path_know = os.path.join(base_path, 'upload_test/','know_test')   # 上传文件目录
if not os.path.exists(upload_path_know):
    os.makedirs(upload_path_know)
 
upload_path_unknown = os.path.join(base_path, 'upload_test/','unknown_test')   # 上传文件目录
if not os.path.exists(upload_path_unknown):
    os.makedirs(upload_path_unknown)

test(upload_path_know,upload_path_unknown)
