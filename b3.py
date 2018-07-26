# -*- coding: utf-8 -*-
import math
from sklearn import neighbors
import os
import os.path
import pickle
import time
from PIL import Image, ImageDraw
#import face_recognition
from scipy.sparse import csr_matrix, coo_matrix
#from face_recognition.face_recognition_cli import image_files_in_folder
from sklearn.preprocessing import StandardScaler
from sklearn.datasets import make_moons, make_circles, make_classification
from sklearn.neighbors import KNeighborsClassifier
from sklearn import neighbors
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.naive_bayes import GaussianNB
#import sklearn.discriminant_analysis
#from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
#from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis as QDA
from scipy.sparse import csr_matrix, coo_matrix
from sklearn.metrics import confusion_matrix    #计算混淆矩阵
from sklearn.metrics import matthews_corrcoef #计算MCC
from sklearn.metrics import  roc_auc_score  #计算MCC 只对二分类可以计算
from sklearn.metrics import  accuracy_score  #计算ACC
from sklearn.ensemble import GradientBoostingClassifier
from sklearn import metrics
import pickle

#names = ["Nearest Neighbors", "Linear SVM", "RBF SVM", "Decision Tree",
#         "Random Forest", "AdaBoost","GradientBoosting", "Naive Bayes", "LDA", "QDA"]
#names = ["Nearest Neighbors", "Linear SVM", "RBF SVM", "Decision Tree",
#         "Random Forest", "AdaBoost","GradientBoosting", "Naive Bayes"]
names = ["Nearest Neighbors"]
classifiers = [
    KNeighborsClassifier(n_neighbors=2, algorithm='ball_tree', weights='distance'),
    SVC(kernel="linear", C=0.025),
    SVC(gamma=2, C=1),
    DecisionTreeClassifier(max_depth=5),
    RandomForestClassifier(max_depth=5, n_estimators=10, max_features=1),
    AdaBoostClassifier(n_estimators=100),
    GradientBoostingClassifier(n_estimators=100, learning_rate=1.0,max_depth=1, random_state=0),
    GaussianNB()]
 #   LDA(),
 #   QDA()]
def knn_train(X,y, model_save_path=None, n_neighbors=None, knn_algo='ball_tree', verbose=False):

  #  X = []
  #  y = []
    # Determine how many neighbors to use for weighting in the KNN classifier
    if n_neighbors is None:
        n_neighbors = int(round(math.sqrt(len(X))))
        if verbose:
            print("Chose n_neighbors automatically:", n_neighbors)

    # Create and train the KNN classifier
    knn_clf = neighbors.KNeighborsClassifier(n_neighbors=n_neighbors, algorithm=knn_algo, weights='distance',n_jobs =2)
    knn_clf.fit(X, y)

    # Save the trained KNN classifier
    if model_save_path is not None:
        with open(model_save_path, 'wb') as f:
            pickle.dump(knn_clf, f)

    return knn_clf
def other_train(X,y, model_save_path=None, n_neighbors=None, knn_algo='ball_tree', verbose=False):

  #  X = []
  #  y = []
    # Determine how many neighbors to use for weighting in the KNN classifier
    if n_neighbors is None:
        n_neighbors = int(round(math.sqrt(len(X))))
        if verbose:
            print("Chose n_neighbors automatically:", n_neighbors)

    # Create and train the KNN classifier
    knn_clf = neighbors.KNeighborsClassifier(n_neighbors=n_neighbors, algorithm=knn_algo, weights='distance')
    knn_clf.fit(X, y)

    # Save the trained KNN classifier
    if model_save_path is not None:
        with open(model_save_path, 'wb') as f:
            pickle.dump(knn_clf, f)

    return knn_clf
def getAllImagesFromFile(output1 = 'data.pkl',output2 = 'data1.pkl'):
    pkl_file1 = open(output1, 'rb')
    pkl_file2 = open(output2, 'rb')
    data1 = pickle.load(pkl_file1)
    data2 = pickle.load(pkl_file2)
    pkl_file1.close()
    pkl_file2.close()
    return data1,data2
def getDatas(d):
    X_train,y_train = getAllImagesFromFile(output1 = './upload/'+d+'/data_know.pkl',output2 = './upload/'+d+'/data1_know.pkl')
    X_test,y_test = getAllImagesFromFile(output1 = './upload/'+d+'/data_unknown.pkl',output2 = './upload/'+d+'/data1_unknown.pkl')
    return X_train, X_test, y_train, y_test
def test_models(X_train, X_test, y_train, y_test,d):
    for name, clf in zip(names, classifiers):
        print(name)
      #  clf.fit(X_train,y_train)
      #  s=pickle.dumps(clf)
        #f=open('./models/'+d+'_'+name+'.txt','wb+')
        f = open('./models/trained_knn_model_xh_10_done.clf','rb')
        clf = pickle.load(f)
        print(clf)
  #      f.write(s)
  #      f.close()
        distance_threshold = 0.6
      #  pkl_file1 = open('./models/'+d+'_'+name+'.txt', 'rb')
     #   pkl_file2 = open(output2, 'rb')
     #   clf = pickle.load(pkl_file1,encoding='bytes')
        #clf = pickle.load()
        # Use the KNN model to find the best matches for the test face
        y_pred = []
        j = 0
        i = 0
        for faces_encodings in X_test:
            
            closest_distances = clf.kneighbors(faces_encodings, n_neighbors=1)
            are_matches = [closest_distances[0][0][0] <= distance_threshold]
         #   print closest_distances,are_matches
    # Predict classes and remove classifications that aren't within the threshold
           # print(are_matches)
          #  print(clf.predict([faces_encodings]))
            for pred, rec in zip(clf.predict([faces_encodings]), are_matches):
                if rec:
                    y_pred.append(pred)
                else:
                    y_pred.append(pred)
            if y_pred[i][0:9] == y_test[i][0:9]
                j = j + 1
                print(i,j,pred)
            else : print(i,j,pred,y_test[i][0:9])
            i = i + 1
      #  y_pred.append([(pred) if rec else ("unknown") )

      #  y_pred =clf.predict(X_test)
        j = 0
        for i in range(0,len(y_pred)):
            if y_pred[i] == y_test[i]:
                j = j + 1
        if j!=0:
            print(j,len(y_pred),(float)(j/(len(y_pred))))
        else:
            print(j,len(y_pred),0)
        # 计算混淆 矩阵 Compute confusion matrix

#        cm = confusion_matrix(y_test, y_pred)

    #    print(cm)
    #    Precision = (float)(cm[0][0]/(cm[1][0]+cm[0][0]))
   #     Recall = (float)(cm[0][0]/(cm[0][0]+cm[0][1]))
   #     F1 = 2*Precision*Recall/(Precision+Recall)
   #     #计算准确率,MCC等
      #  print("Precision: %f "%Precision)
   #     print("Recall: %f"%Recall)
   #     print("F1 Score: %f"%F1)
 #       print("MCC: %f " %matthews_corrcoef(y_test,y_pred))

   #     print( "ACC:  %f "% accuracy_score(y_test,y_pred))
    #    print("AUC Score (Test): " , metrics.roc_auc_score(y_test,y_pred))

      #  import pickle

if __name__ == '__main__':
    X_train, X_test, y_train, y_test = getDatas('1174')
    test_models(X_train, X_test, y_train, y_test,'1174')