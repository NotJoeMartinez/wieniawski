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


def plot_images(img1, img2):
    fig, axs = plt.subplots(1, 2, figsize=(10, 5))

    axs[0].imshow(img1, cmap='gray')
    axs[0].set_title('Original Image')

    axs[1].imshow(img2, cmap='gray')
    axs[1].set_title('after flip')

    # Hide x labels and tick labels for top plots and y ticks for right plots.
    for ax in axs.flat:
        ax.label_outer()

    plt.show()



def plot_single_image(img, title=""):
    plt.imshow(img, cmap='gray')
    plt.title(title)
    plt.show()