import math

import cv2
import numpy as np
from matplotlib import pyplot as plt


class ImageDisplayer:
    def __init__(self):
        pass

    @staticmethod
    def plot_images(image_list: list, cmaps=None) -> None:
        """
        Displays given list of images
        :param cmaps: list - cmap str names of how each image should be plotted
        :param image_list: list - list of images to be shown
        :return: None
        """
        if cmaps is None:
            cmaps = []
        num_images = len(image_list)

        plt.figure(figsize=(16, 8))
        num_rows = math.floor(math.sqrt(num_images))
        num_columns = math.ceil(math.sqrt(num_images))
        for i, image in enumerate(image_list):
            plt.subplot(num_rows, num_columns, i + 1)
            if len(cmaps) - 1 >= i:
                plt.imshow(image, cmap=cmaps[i])
            else:
                plt.imshow(image)
            # plt.title('Image')
            plt.axis('off')
        plt.tight_layout()
        plt.show()

