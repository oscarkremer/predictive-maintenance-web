import cv2
import random
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from collections import namedtuple

GRID_SIZE = 100
ALEX_NET = 227
IMAGE_WIDTH = 150
IMAGE_HEIGHT = 300


def image_grid(data, labels, path, size=5):
    if size > np.sqrt(len(data)):
        size = int(np.floor(np.sqrt(len(data))))
    rand_index = random.sle(range(len(data)), k=size * size)
    filename = 'test.png'

    fig = plt.figure(figsize=(GRID_SIZE, GRID_SIZE))
    plt.legend(fontsize=10, loc='lower right').set_title(
        'Cerberus - Classification')
    plt.axis('off')
    for m in range(1, size * size + 1):
        img = data[rand_index[m - 1]].reshape([ALEX_NET, ALEX_NET, 3])
        img = cv2.resize(img, (IMAGE_WIDTH, IMAGE_HEIGHT), cv2.INTER_CUBIC)
        fig.add_subplot(size, size + 1, m)
        plt.imshow(img)
        plt.title(labels[rand_index[m - 1]], fontsize=5)
        plt.axis('off')

    plt.savefig('{0}/{1}'.format(path, filename), transparent=False)
    plt.show()
