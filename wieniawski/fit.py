import os
import pickle
import cv2
import numpy as np
from .box import Box
from .train_model import *

import matplotlib.pyplot as plt

def predict(img, model_path=None):

    if model_path != None:
        model_file = model_path
    else:
        model_file = os.getenv("DEFAULT_MODEL")

    if not os.path.exists(model_file):
        print('Please wait while training the NN-HOG model....')
        train('NN', 'hog', 'nn_trained_model_hog')

    model = pickle.load(open(model_file, 'rb'))

    features = extract_features(img, 'hog')
    labels = model.predict([features])

    return labels

