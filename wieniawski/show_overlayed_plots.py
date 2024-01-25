
from cv2 import imread
import matplotlib.pyplot as plt

def show_og_overlayed(og_fname, ov_fname, res):
    rows = 3
    columns = 1
    og = imread(og_fname)
    ov = imread(ov_fname)
    fig = plt.figure(figsize=(10, 7))

    fig.add_subplot(rows, columns, 1)

    # show og img 
    plt.imshow(ov)
    plt.title("With Overlay")
    fig.add_subplot(rows, columns, 2)

    # show overlayed img 
    plt.imshow(og)
    plt.title("Original Image")


    fig.add_subplot(rows, columns, 3)
    plt.axis("off")
    plt.title("Output array of notes")
    plt.text(0, 0.8, str(res))

    plt.show()

