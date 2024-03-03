## 2024-01-28T05-25-59Z
rotation seems to be the biggest problem

- https://www.youtube.com/@OpticalMusicRecognition
- https://drive.google.com/file/d/10E6YZPazVhFrROcea63f1j6ZtLQnyBk-/view

## 2024-03-03T10-24-03Z

The reson `run_experiment` is named `run_experiment` is because
it looks like the original developer was testing out multiple 
different models and "feature sets". 

These models are fetched from `load_classifiers()` as a dictionary 
of different sklean models. 

```python
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
```

The only one actually used in the final product was 'NN' which is a Multi Layer
Perseptron Classifier, which is an old term for Nural Network.

the second paramater taken by `run_experiment` is `feature_set='hog'`.  `HOG`
stands for Histogram of Oriented Gradients.

Before feeding the images to the model for training the dataset is loaded with
this feature_set flag set as `hog`

```python 
features, labels = load_dataset(feature_set, dir_names) 
```

`features` is actually an array of `ndarrays`, these arrays corispond to images
from the dataset. `labels` are just the name of directories corisopding to the 
images.


`load_dataset()` itterates through the dataset, converts each image to an
ndarray and passes it to `extract_features()` with the argument of the image and
a string specifiying the feature set. which is allways `hog`


`extract_hog_features` then calls `extract_hog_features` which does the
`Histogram of Oriented Gradients` thing which I don't understand.

We can simplify all this removing the dynamic parts. 
- return only a `sklearn` modle and random seadfrom `load_classifiers`
- refactor `load_dataset` to always use `hog` feature extraction

but something tells me I should at least try to use the other feature
extractors and models to see how they do.
