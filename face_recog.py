# -*- coding: utf-8 -*-
"""
Created on Thu Jun 21 00:33:06 2018

@author: Administrator
"""
# coding: utf8
import face_recognition
import cv2
import os
import pickle,pprint
import sys
reload(sys)
sys.setdefaultencoding('utf8')
Image_name = []
def judgeUnknown(path,filename):
    E_MORE_THAN_ONE = -1
    NO_FACE = -2
    # 读取图片并识别人脸
    try:
        img = face_recognition.load_image_file(path+"/"+filename)
    except:
		return NO_FACE
    face_locations = face_recognition.face_locations(img)
    print face_locations,'ll'

    # 调用opencv函数显示图片 
 #   img = cv2.imread("obama.jpg")
    # cv2.namedWindow("原图")
    # cv2.imshow("原图", img)

    # 遍历每个人脸，并标注
    faceNum = len(face_locations)
    print 'faceNum',faceNum
    if faceNum>1:
        return E_MORE_THAN_ONE
    elif faceNum==0:
        return NO_FACE
    return 1
def save(filename, contents): 
  fh = open(filename, 'w') 
  fh.write(contents) 
  fh.close()
def get(filename): 
  fh = open(filename, 'r') 
  a = fh.read()
  fh.close()
  return a.split("_")
def getAllImages(path,output1 = 'data.pkl',output2 = 'data1.pkl'):
    Images = []
    Encodings = []
    i = 0
    for filename in os.listdir(path):              #listdir的参数是文件夹的路径
        #print filename
        #if i > 470:
        Images = face_recognition.load_image_file(path+"/"+filename)
        Image_name.append(filename)
        face_bounding_boxes = face_recognition.face_locations(Images)
       # print i,filename
        Encodings.append(face_recognition.face_encodings(Images,known_face_locations=face_bounding_boxes))
        i = i + 1
        if i > 50 : break
   # print Encodings
 #   print type(Encodings)
    output = open(output1, 'wb')
    output_names = open(output2, 'wb')
    # Pickle dictionary using protocol 0.
    pickle.dump(Encodings, output,-1)
    pickle.dump(Image_name, output_names,-1)
    # Pickle the list using the highest protocol available.
    #pickle.dump(selfref_list, output, -1)

    output.close()
    return Encodings
def saveEncodings(path,Encodings,Image_name,output1 = 'data.pkl',output2 = 'data1.pkl'):
    output = open(output1, 'wb')
    output_names = open(output2, 'wb')
    # Pickle dictionary using protocol 0.
    pickle.dump(Encodings, output,-1)
    pickle.dump(Image_name, output_names,-1)
   
def getAllImagesFromFile(path,output1 = 'data.pkl',output2 = 'data1.pkl'):
    pkl_file1 = open(output1, 'rb')
    pkl_file2 = open(output2, 'rb')
    data1 = pickle.load(pkl_file1)
    data2 = pickle.load(pkl_file2)
    pkl_file1.close()
    pkl_file2.close()
    return data1,data2
    
def getUnknownImage(path,filename):
    unknown_image = face_recognition.load_image_file(path+"/"+filename);
    X_face_locations = face_recognition.face_locations(unknown_image)
    # If no faces are found in the image, return an empty result.
    if len(X_face_locations) == 0:
        return []
    # Find encodings for faces in the test iamge
    unknown_encoding = face_recognition.face_encodings(unknown_image, known_face_locations=X_face_locations)
 #   unknown_encoding = face_recognition.face_encodings(unknown_image)[0]
    return unknown_encoding

def getCompareResult(KnownEncodings,UnknownEncoding,tolerance1=0.39):
    a = face_recognition.face_distance(KnownEncodings, UnknownEncoding)
   # print 'a',a
    results = face_recognition.compare_faces(KnownEncodings, UnknownEncoding,tolerance=tolerance1)
    return results,a

def getResult(results,distances):
    #print results
    q = []
   # max_i = distances.tolist().index(max_distance)
    d1 = distances.tolist()
    d = distances.tolist()
    d.sort()
  #  d.reverse()
    j = 0
#    print distances[max_i],d[0]
    for i in range(0,10):
       # print i,d[i]
        if results[d1.index(d[i])] == True:
          q.append(d1.index(d[i]))
          #j = j + 1
         # if j == 5 : break
  #  return q
   # if results[max_i] == True:
   #     return max_i
   # for i in range(0, len(results)):
      #  if results[i] == True:
     #       q.append(i)
    return q
    return -1

def main(pathknow,pathunknown,unknownfilwname,model_path):
    distance_threshold = 0.6
    flag = judgeUnknown(pathunknown,unknownfilwname)
    if flag == 1:
        unknown_encoding = getUnknownImage(pathunknown,unknownfilwname)
        with open(model_path, 'rb') as f:
            knn_clf = pickle.load(f)
        closest_distances = knn_clf.kneighbors(unknown_encoding, n_neighbors=1)
        are_matches = [closest_distances[0][0][0] <= distance_threshold]

        # Predict classes and remove classifications that aren't within the threshold
        a =[pred if rec else ("unknown") for pred, rec in zip(knn_clf.predict(unknown_encoding), are_matches)]
        return a[0]
    else:
        return flag