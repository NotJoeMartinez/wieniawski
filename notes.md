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
- calculates histogram

### `cv2.cvtColor()`


### `cv2.HOGDescriptor()`
The cv2.HOGDescriptor() is a function in the OpenCV library in Python. 
HOG stands for Histogram of Oriented Gradients, which is a feature 
descriptor used in computer vision and image processing for the purpose 
of object detection.

- https://en.wikipedia.org/wiki/Histogram_of_oriented_gradients




## numpy

### `numpy.ndarray` 
- `ndarray` is short for N-dimensional array
- homogonus datatype `int32`, `float64` & `complex128`
- immutable, fixed size


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


### `svm.LinearSVC` 
- Linear Support Vector Classification.
- https://scikit-learn.org/stable/modules/generated/sklearn.svm.LinearSVC.html


### `model.fit()`
in `model.fit()` the `model` is a `sklearn.neural_network._multilayer_perceptron.MLPClassifier`
