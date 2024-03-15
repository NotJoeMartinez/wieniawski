everyone starts somewhere

## opencv

### `cv2.imread()`
- returns an `numpy.ndarray`

### `cv2.resize()`
- resizes image

### `cv2.normalize()`

### `cv2.flatten()`
- converts 3d array into 1d array

### `cv2.calcHist()`
calculates histograms of images. 

colored histograms and greyscale histograms have different uses cases.
this project uses grey scale histograms for the purpose of image 
segmentation.

- https://docs.opencv.org/4.x/d1/db7/tutorial_py_histogram_begins.html

### `cv2.cvtColor()`
used to convert an image from one color space to another.



### `cv2.HOGDescriptor()`
The cv2.HOGDescriptor() is a function in the OpenCV library in Python. 
HOG stands for Histogram of Oriented Gradients, which is a feature 
descriptor used in computer vision and image processing for the purpose 
of object detection.

default args
```python
cv2.HOGDescriptor(win_size=(64, 128),
                  block_size=(16, 16),
                  block_stride=(8, 8),
                  cell_size=(8, 8),
                  nbins=9,
                  win_sigma=DEFAULT_WIN_SIGMA,
                  threshold_L2hys=0.2,
                  gamma_correction=true,
                  nlevels=DEFAULT_NLEVELS)
```

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

- https://docs.opencv.org/3.4/d5/d33/structcv_1_1HOGDescriptor.html
- https://en.wikipedia.org/wiki/Histogram_of_oriented_gradients
- https://learnopencv.com/histogram-of-oriented-gradients/
- https://github.com/solerjuan/astroHOG
- https://ui.adsabs.harvard.edu/abs/2019A%26A...622A.166S/abstract 




## numpy

### `numpy.ndarray` 
- `ndarray` is short for N-dimensional array
- homogonus datatype `int32`, `float64` & `complex128`
- immutable, fixed size


## matplotlib


## sklearn


### `KNeighborsClassifier`
- https://en.wikipedia.org/wiki/K-nearest_neighbors_algorithm 
- https://scikit-learn.org/stable/modules/generated/sklearn.neighbors.KNeighborsClassifier.html

### `MLPClassifier`
- `sklearn.neural_network.MLPClassifier`
- Multi-layer Perceptron classifier. optimizes the log-loss function using 
LBFGS or stochastic gradient descent. 

- https://scikit-learn.org/stable/modules/generated/sklearn.neural_network.MLPClassifier.html
- https://dasha.ai/en-us/blog/log-loss-function
- https://machinelearningmastery.com/adam-optimization-algorithm-for-deep-learning

### `svm.LinearSVC` 
- Linear Support Vector Classification.
- https://scikit-learn.org/stable/modules/generated/sklearn.svm.LinearSVC.html
https://www.csie.ntu.edu.tw/~cjlin/papers/libsvm.pdf


### `model.fit()`
in `model.fit()` the `model` is a `sklearn.neural_network._multilayer_perceptron.MLPClassifier`
