import os
import cv2
import random
import pickle
from pathlib import Path
from glob import glob
import imutils
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn import svm

dataset_path = os.getenv("TRAIN_DATA_PATH") 
target_img_size = (100, 100)
sample_count = 50


def extract_raw_pixels(img):
    resized = cv2.resize(img, target_img_size)
    return resized.flatten()


def extract_hsv_histogram(img):
    resized = cv2.resize(img, target_img_size)
    hsv = cv2.cvtColor(resized, cv2.COLOR_BGR2HSV)
    hist = cv2.calcHist([hsv], 
                        [0, 1, 2], 
                        None, 
                        [8, 8, 8],
                        [0, 180, 0, 256, 0, 256])
    if imutils.is_cv2():
        hist = cv2.normalize(hist)
    else:
        cv2.normalize(hist, hist)
    return hist.flatten()


def extract_hog_features(img):
    print(f"extract_hog_features: img.shape: {img.shape} ")
    img = cv2.resize(img, target_img_size)
    win_size = (100, 100)
    cell_size = (4, 4)
    block_size_in_cells = (2, 2)

    block_size = (block_size_in_cells[1] * cell_size[1],
                  block_size_in_cells[0] * cell_size[0])

    block_stride = (cell_size[1], cell_size[0])

    nbins = 9  # Number of orientation bins

    
    """
    win_size: Size of detection window in pixels (width, height). 
    Defines the region of interest. 

    block_size: Block size in pixels (width, height). Defines how 
    many cells are in each block.

    block_stride: Block stride in pixels (horizontal, vertical). 
    defines the distance between adjecent blocks.

    cell_size: Cell size in pixels (width, height). Determines the 
    size fo your cell

    nbins: Number of bins for the histograms. Determines the number 
    of angular bins used to make the histograms HOG uses unsigned 
    gradients, so the angular bins will have values between 0 and 180 degrees
    """

    hog = cv2.HOGDescriptor(win_size, 
                            block_size,
                            block_stride, 
                            cell_size, 
                            nbins)
    h = hog.compute(img)
    h = h.flatten()
    return h.flatten()


def extract_features(img, feature_set='raw'):
    if feature_set == 'hog':
        return extract_hog_features(img)
    elif feature_set == 'raw':
        return extract_raw_pixels(img)
    else:
        return extract_hsv_histogram(img)


def load_dataset(feature_set='raw', dir_names=[]):

    features = [] # array of ndarrays of images?
    labels = [] # directory names
    count = 0

    for dir_name in dir_names:

        imgs = glob(f'{dataset_path}/{dir_name}/*.png')
        count += len(imgs)

        # why do we need to shuffle the images?
        subset = random.sample(
            [i for i in range(len(imgs))], 
            min(len(imgs), sample_count)
            )

        for i in subset:
            img = cv2.imread(imgs[i])
            labels.append(dir_name)
            features.append(extract_features(img, feature_set))

    print(f'Total: {len(dir_names)} directories, and {count} images')

    return features, labels


def load_classifiers():
    random_seed = 42
    random.seed(random_seed)
    np.random.seed(random_seed)

    classifiers = {
        'SVM': svm.LinearSVC(random_state=random_seed),
        'KNN': KNeighborsClassifier(n_neighbors=7),
        'NN': MLPClassifier(activation='relu', 
                            hidden_layer_sizes=(200,),
                            max_iter=10000, alpha=1e-4,
                            solver='adam', verbose=20,
                            tol=1e-8, random_state=1,
                            learning_rate_init=.0001,
                            learning_rate='adaptive')
    }
    return classifiers, random_seed


def run_experiment(classifier='NN', feature_set='hog', dir_names=[]):
    print('Loading dataset. This will take time ...')
    features, labels = load_dataset(feature_set, dir_names)
    print('Finished loading dataset.')
    # classifiers is an array of sklearn models
    classifiers, random_seed = load_classifiers()

    train_features, test_features, train_labels, test_labels = train_test_split(
        features, 
        labels, 
        test_size=0.2, 
        random_state=random_seed)

    # sklearn.neural_network._multilayer_perceptron.MLPClassifier
    model = classifiers[classifier]

    print('############## Training', classifier, "##############")
    model.fit(train_features, train_labels)
    accuracy = model.score(test_features, test_labels)

    print(classifier, 'accuracy:', accuracy*100, '%')

    return model, accuracy


def train(model_name, feature_name, saved_model_name):
    

    # dir_names = [path.split('/')[2] for path in glob(f'{dataset_path}/*')]
    dir_names = [subdir.name for subdir in Path(dataset_path).iterdir() if subdir.is_dir()]
    model, accuracy = run_experiment(model_name, feature_name, dir_names)
    model_output_dir = os.getenv("MODEL_OUTPUT_DIR")

    filename = f'{model_output_dir}/{saved_model_name}.sav'
    pickle.dump(model, open(filename, 'wb'))


