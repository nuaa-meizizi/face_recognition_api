# -*- coding: utf-8 -*-
"""
Created on Thu Jun 21 00:33:06 2018

@author: Administrator
"""

# -*- coding: utf-8 -*-

# 检测人脸
import face_recognition
import cv2
import os


# for i in range(0, faceNum):
#     top =  face_locations[i][0]
#     right =  face_locations[i][1]
#     bottom = face_locations[i][2]
#     left = face_locations[i][3]

#     start = (left, top)
#     end = (right, bottom)

#     color = (55,255,155)
#     thickness = 3
#     cv2.rectangle(img, start, end, color, thickness)

# # 显示识别结果
# cv2.namedWindow("识别")
# cv2.imshow("识别", img)

# cv2.waitKey(0)
# cv2.destroyAllWindows()
Image_name = []
def judgeUnknown(path,filename):
    E_MORE_THAN_ONE = -1
    NO_FACE = -2
    # 读取图片并识别人脸
    img = face_recognition.load_image_file(path+"/"+filename)
    face_locations = face_recognition.face_locations(img)
    print face_locations

    # 调用opencv函数显示图片
 #   img = cv2.imread("obama.jpg")
    # cv2.namedWindow("原图")
    # cv2.imshow("原图", img)

    # 遍历每个人脸，并标注
    faceNum = len(face_locations)
    if faceNum>1:
        return E_MORE_THAN_ONE
    elif faceNum==0:
        return NO_FACE
    return 1
def getAllImages(path):
    Images = []
    Encodings = []
    i = 0
    for filename in os.listdir(path):              #listdir的参数是文件夹的路径
        print filename
        Images.append(face_recognition.load_image_file(path+"/"+filename))
        Image_name.append(filename)
        Encodings.append(face_recognition.face_encodings(Images[i])[0])
        i = i + 1
    return Images,Encodings

def getUnknownImage(path,filename):
    unknown_image = face_recognition.load_image_file(path+"/"+filename);
    unknown_encoding = face_recognition.face_encodings(unknown_image)[0]
    return unknown_encoding

def getCompareResult(KnownEncodings,UnknownEncoding):
    results = face_recognition.compare_faces(KnownEncodings, UnknownEncoding,tolerance=0.39)
    return results

def getResult(results):
    print results
    for i in range(0, len(results)):
        if results[i] == True:
            return i
    return -1

def main(pathknow,pathunknown,unknownfilwname):
    flag = judgeUnknown(pathunknown,unknownfilwname)
    if flag!=1:
        print "-1"
        return -1
    Images,Encodings = getAllImages(pathknow)
    unknown_encoding = getUnknownImage(pathunknown,unknownfilwname)
    results = getCompareResult(Encodings,unknown_encoding)
    result = getResult(results)
    print "result",result
    print result,Image_name[result]
    return Image_name[result]
