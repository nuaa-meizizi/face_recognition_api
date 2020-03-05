"""
This is an example of using the k-nearest-neighbors (KNN) algorithm for face recognition.

When should I use this example?
This example is useful when you wish to recognize a large set of known people,
and make a prediction for an unknown person in a feasible computation time.

Algorithm Description:
The knn classifier is first trained on a set of labeled (known) faces and can then predict the person
in an unknown image by finding the k most similar faces (images with closet face-features under eucledian distance)
in its training set, and performing a majority vote (possibly weighted) on their label.

For example, if k=3, and the three closest face images to the given image in the training set are one image of Biden
and two images of Obama, The result would be 'Obama'.

* This implementation uses a weighted vote, such that the votes of closer-neighbors are weighted more heavily.

Usage:

1. Prepare a set of images of the known people you want to recognize. Organize the images in a single directory
   with a sub-directory for each known person.

2. Then, call the 'train' function with the appropriate parameters. Make sure to pass in the 'model_save_path' if you
   want to save the model to disk so you can re-use the model without having to re-train it.

3. Call 'predict' and pass in your trained model to recognize the people in an unknown image.

NOTE: This example requires scikit-learn to be installed! You can install it with pip:
$ pip3 install scikit-learn

"""
# -*- coding: utf-8 -*-
import math
from sklearn import neighbors
import os
import os.path
import pickle
from PIL import Image, ImageDraw
import face_recognition
from face_recognition.face_recognition_cli import image_files_in_folder

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def saveEncodings(Encodings,Image_name,output1 = 'data.pkl',output2 = 'data1.pkl'):
    output = open(output1, 'wb')
    output_names = open(output2, 'wb')
    pickle.dump(Encodings, output,-1)
    pickle.dump(Image_name, output_names,-1)
def train(train_dir, model_save_path=None, n_neighbors=None, knn_algo='ball_tree', verbose=False):

    X = []
    y = []
    print(train_dir)
    # Loop through each person in the training set
    for class_dir in os.listdir(train_dir):
        if not os.path.isdir(os.path.join(train_dir, class_dir)):
            continue
        pkl_file1 = open(os.path.join(train_dir, class_dir,class_dir), 'rb')
        Encoding = pickle.load(pkl_file1)
        pkl_file1.close()
        X.append(Encoding)
        y.append(class_dir)

    # Determine how many neighbors to use for weighting in the KNN classifier
    if n_neighbors is None:
        n_neighbors = int(round(math.sqrt(len(X))))
        if verbose:
            print("Chose n_neighbors automatically:", n_neighbors)
   # saveEncodings(X,y,'encodings/1233/known_data_1.pkl','encodings/1233/known_data1_1.pkl')

    # Create and train the KNN classifier
    knn_clf = neighbors.KNeighborsClassifier(n_neighbors=n_neighbors, algorithm=knn_algo, weights='distance')
    knn_clf.fit(X, y)

    # Save the trained KNN classifier
    if model_save_path is not None:
        with open(model_save_path, 'wb') as f:
            pickle.dump(knn_clf, f)

    return knn_clf



def predict(X_img_path, knn_clf=None, model_path=None, distance_threshold=0.39):
    """
    Recognizes faces in given image using a trained KNN classifier

    :param X_img_path: path to image to be recognized
    :param knn_clf: (optional) a knn classifier object. if not specified, model_save_path must be specified.
    :param model_path: (optional) path to a pickled knn classifier. if not specified, model_save_path must be knn_clf.
    :param distance_threshold: (optional) distance threshold for face classification. the larger it is, the more chance
           of mis-classifying an unknown person as a known one.
    :return: a list of names and face locations for the recognized faces in the image: [(name, bounding box), ...].
        For faces of unrecognized persons, the name 'unknown' will be returned.
    """
    if not os.path.isfile(X_img_path) or os.path.splitext(X_img_path)[1][1:] not in ALLOWED_EXTENSIONS:
        raise Exception("Invalid image path: {}".format(X_img_path))

    if knn_clf is None and model_path is None:
        raise Exception("Must supply knn classifier either thourgh knn_clf or model_path")

    # Load a trained KNN model (if one was passed in)
    if knn_clf is None:
        with open(model_path, 'rb') as f:
            knn_clf = pickle.load(f)

    # Load image file and find face locations
    X_img = face_recognition.load_image_file(X_img_path)
    X_face_locations = face_recognition.face_locations(X_img)

    # If no faces are found in the image, return an empty result.
    if len(X_face_locations) == 0:
        return []

    # Find encodings for faces in the test iamge
    faces_encodings = face_recognition.face_encodings(X_img, known_face_locations=X_face_locations)

    # Use the KNN model to find the best matches for the test face
    closest_distances = knn_clf.kneighbors(faces_encodings, n_neighbors=1)
    are_matches = [closest_distances[0][i][0] <= distance_threshold for i in range(len(X_face_locations))]

    # Predict classes and remove classifications that aren't within the threshold
    return [(faces_encodings[0],X_img_path[21:30],pred, loc) if rec else (faces_encodings,X_img_path[20:30],"unknown", loc) for pred, loc, rec in zip(knn_clf.predict(faces_encodings), X_face_locations, are_matches)]

def test_model():
    # STEP 1: Train the KNN classifier and save it to disk
    # Once the model is trained and saved, you can skip this step next time.
    print("Training KNN classifier...")
    classifier = train("upload_test/xh_10_done", model_save_path="models/1233/trained_knn_model_10.clf", n_neighbors=3)
    #classifier = train("knn_examples/xh3_done", model_save_path="trained_knn_model_10.clf", n_neighbors=3)
    print("Training complete!")

    # STEP 2: Using the trained classifier, make predictions for unknown images
    j = 0
    q = []
    faces_encodings = []
    X_img_path = []
    for image_file in os.listdir("upload_test/sfzh_10"):
        full_file_path = os.path.join("upload_test/sfzh_10", image_file)

     #   print("Looking for faces in {}".format(image_file))

        # Find all people in the image using a trained classifier model
        # Note: You can pass in either a classifier file name or a classifier model instance
        predictions = predict(full_file_path, model_path="models/1233/trained_knn_model_10.clf",distance_threshold = 0.6)

        # Print results on the console
        for unen,unname,name, (top, right, bottom, left) in predictions:
            if image_file[0:9] == name:
              j = j + 1
              print("- Found {} at ({}, {})".format(name, left, top))
            else :
              q.append(name)
              print(name,image_file[0:9])

            faces_encodings.append(unen)
            X_img_path.append(unname)
    saveEncodings(faces_encodings,X_img_path,'encodings/1233/unknown_data_1.pkl','encodings/1233/unknown_data1_1.pkl')
    print(j)

    print(q,len(q))
