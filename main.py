from typing import Tuple

import numpy as np
from skimage.io import imread, imshow, show
from skimage.color import rgb2gray
import matplotlib.pyplot as plt

from dino import Dino


def load_dino() -> np.ndarray:
    return rgb2gray(imread('data/dino.png', as_gray=True))


def handle_shot(shot: np.ndarray, dino_position: Tuple[int, int], template_shape: Tuple):
    plt.figure(figsize=(16, 9))
    sb = plt.subplot()
    sb.imshow(shot, cmap=plt.cm.gray)
    # plt.plot(x + t_w, mid_y, 'ro')
    rect = plt.Rectangle((x, y), t_w, t_h, edgecolor='r', facecolor='none')
    sb.add_patch(rect)
    # plt.plot(x, y, 'ro')
    plt.show()


def main():
    dino_img = load_dino()
    # imshow(dino_img)
    # show()
    dino = Dino(dino_img)
    dino.init()
    dino.start()


if __name__ == '__main__':
    main()
