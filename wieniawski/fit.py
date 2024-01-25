import cv2
import numpy as np
from .box import Box
from .train_model import *
import os
import pickle

def predict(img):
    model_file = os.getenv("DEFAULT_MODEL")
    if not os.path.exists(model_file):
        print('Please wait while training the NN-HOG model....')
        train('NN', 'hog', 'nn_trained_model_hog')

    model = pickle.load(open(model_file, 'rb'))
    features = extract_features(img, 'hog')
    labels = model.predict([features])

    return labels


# if __name__ == "__main__":
#     img = cv2.imread('testresult/0_6.png')
#     labels = predict(img)
#     print(labels)
