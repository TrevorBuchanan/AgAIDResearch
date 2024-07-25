from math import sqrt

import cv2
import numpy as np
from matplotlib import pyplot as plt
from scipy.ndimage import convolve
from Helpers.utility import find_max_rectangle


class ImageProcessor:
    @staticmethod
    def vertical_image_split(image) -> tuple:
        """
        Cuts an image in half vertically and returns both halves
        :param image: Image to perform split on
        :return: tuple[,] - The two halves of the vertical split in the form (left, right)
        """
        width = int(image.shape[1] / 2)
        height = int(image.shape[0])
        x, y, w, h = 0, 0, width, height
        left_half_img = image[y:y + h, x:x + w]
        width = int(image.shape[1] / 2)
        height = int(image.shape[0])
        x, y, w, h = width, 0, width, height
        right_half_img = image[y:y + h, x:x + w]
        return left_half_img, right_half_img

    @staticmethod
    def separate_colors(image) -> tuple:
        """
        Separates the color channels in an image and returns a tuple of all three
        :param image: Image to perform separation on
        :return: tuple[np.array, np.array, np.array] - Tuple of color channels in the form (r, g, b)
        """
        # Split channels
        red_channel = image[:, :, 0]
        green_channel = image[:, :, 1]
        blue_channel = image[:, :, 2]
        return red_channel, green_channel, blue_channel

    @staticmethod
    def convert_to_gray(image) -> cv2.cvtColor:
        """
        Converts a given image into a gray scale version
        :return: cv2.cvtColor - Gray scale version of original image
        """
        # Convert to grayscale
        return cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

    @staticmethod
    def draw_rects_to_image(image, rectangles: list) -> None:
        """
        Draws given rectangle list on to image
        :param image: The image to draw to
        :param rectangles: list - List of tuple rectangles in the form (x pos, y pos, width, height)
        :return: None
        """
        # Draw rectangles on the original image
        for rect in rectangles:
            cv2.rectangle(image, (rect[0], rect[1]), (rect[0] + rect[2], rect[1] + rect[3]), (0, 255, 0), 1)

