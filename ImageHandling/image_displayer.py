import math

import cv2
import numpy as np
from matplotlib import pyplot as plt


class ImageDisplayer:
    def __init__(self):
        pass

    @staticmethod
    def plot_images(image_list: list) -> None:
        """
        Displays given list of images
        :param image_list: list - list of images to be shown
        :return: None
        """
        num_images = len(image_list)

        plt.figure(figsize=(16, 8))
        num_rows = math.floor(math.sqrt(num_images))
        num_columns = math.ceil(math.sqrt(num_images))
        for i, image in enumerate(image_list):
            plt.subplot(num_rows, num_columns, i + 1)
            plt.imshow(image)
            # plt.title('Image')
            plt.axis('off')
        plt.tight_layout()
        plt.show()

