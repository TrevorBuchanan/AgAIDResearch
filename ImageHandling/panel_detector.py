from ImageHandling.image_processor import ImageProcessor
from math import sqrt

import cv2
import numpy as np
from matplotlib import pyplot as plt
from Helpers.utility import find_max_rectangle, calculate_subsection_areas, get_bounding_rects


class PanelDetector:
    def __init__(self):
        self.image_processor = ImageProcessor()
        self.same_value_tolerance = 3
        self.uniform_tolerance = 255
        self.corner_diff_tol = 10
        self.corner_check_dist = 5
        self.min_num_corner_good = 2
        self.area_min = 200
        self.area_max = 500
        self.min_width = 10
        self.min_height = 10

        # Temporary maybe
        self.show_mask = False
        self.show_areas = False
        self.temp_color_channels_names = ['Reds', 'Greens', 'Blues', 'gray']
        self.temp_color_channel_index = 0

    def get_panel_rect(self, image):
        working_image = self.get_working_image(image)
        red_channel, green_channel, blue_channel = self.image_processor.separate_colors(working_image)
        gray_channel = self.image_processor.convert_to_gray(working_image)
        color_channels = [red_channel, green_channel, blue_channel, gray_channel]
        working_rects = []
        for i, c in enumerate(color_channels):  # TODO: Change back to normal
            self.temp_color_channel_index = i
            for rec in self.get_possible_rects(c):
                working_rects.append(rec)
        good_rects = {}
        print(len(working_rects))
        for i, c in enumerate(color_channels):  # TODO: Change back to normal
            self.temp_color_channel_index = i
            good_rects = self.filter_rects(c, working_rects)
        print(len(good_rects))
        return list(good_rects)

    def filter_rects(self, color_channel, rects):
        filtered_rects = self.filter_by_corners(color_channel, rects)

        return filtered_rects

    def filter_by_corners(self, color_channel, rects):
        filtered_rects = []
        for rect in rects:
            scaled_image = color_channel[rect[1]:rect[1] + rect[3], rect[0]:rect[0] + rect[2]]
            similar_value_mask = np.zeros_like(scaled_image, dtype=np.uint8)
            num_rows, num_cols = scaled_image.shape
            for i in range(1, num_rows - 1):
                for j in range(1, num_cols - 1):
                    if (abs(int(scaled_image[i, j]) - int(scaled_image[i - 1, j])) < self.uniform_tolerance and
                            abs(int(scaled_image[i, j]) - int(scaled_image[i + 1, j])) < self.uniform_tolerance and
                            abs(int(scaled_image[i, j]) - int(scaled_image[i, j - 1])) < self.uniform_tolerance and
                            abs(int(scaled_image[i, j]) - int(scaled_image[i, j + 1])) < self.uniform_tolerance):
                        similar_value_mask[i, j] = 1
            x, y, w, h = find_max_rectangle(similar_value_mask)
            total_x = x + rect[0] - 1
            total_y = y + rect[1] - 1
            w = w + 1
            h = h + 1
            if w * h < self.area_min or w < self.min_width or h < self.min_height:
                continue
            filtered_rects.append((total_x, total_y, w, h))
        return filtered_rects

    def get_possible_rects(self, color_channel):
        areas_img = self.get_possible_areas(color_channel)
        bounding_rects = get_bounding_rects(areas_img)
        return bounding_rects

    def get_possible_areas(self, color_channel):
        bin_contours_img = self.get_binary_contours_img(color_channel)
        areas_img = calculate_subsection_areas(bin_contours_img)
        areas_img[areas_img < self.area_min] = 0
        areas_img[areas_img > self.area_max] = 0
        areas_img[(areas_img >= self.area_min) & (areas_img <= self.area_max)] = 1
        return areas_img

    def get_binary_contours_img(self, color_channel):
        similar_values_mask = np.zeros_like(color_channel, dtype=np.uint8)
        num_rows, num_cols = color_channel.shape
        for i in range(1, num_rows - 1):
            for j in range(1, num_cols - 1):
                if (abs(int(color_channel[i, j]) - int(color_channel[i - 1, j])) < self.same_value_tolerance and
                        abs(int(color_channel[i, j]) - int(color_channel[i + 1, j])) < self.same_value_tolerance and
                        abs(int(color_channel[i, j]) - int(color_channel[i, j - 1])) < self.same_value_tolerance and
                        abs(int(color_channel[i, j]) - int(color_channel[i, j + 1])) < self.same_value_tolerance):
                    similar_values_mask[i, j] = 1
        sim_vals_contours, _ = cv2.findContours(similar_values_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        img_with_contours = color_channel.copy()
        cv2.drawContours(img_with_contours, sim_vals_contours, -1, (255,), thickness=cv2.FILLED)
        binary_contours_img = img_with_contours.copy()
        binary_contours_img[binary_contours_img != 255] = 0
        binary_contours_img[binary_contours_img == 255] = 1
        self.filter_lonelies(binary_contours_img, 5)
        if binary_contours_img.dtype != np.uint8:
            binary_contours_img = cv2.convertScaleAbs(binary_contours_img)
        binary_contours, _ = cv2.findContours(binary_contours_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        return binary_contours_img

    def check_corners(self, color_channel, rect):
        num_good_corners = 0
        w = color_channel.shape[1]
        h = color_channel.shape[0]
        top_left_pos = (rect[0], rect[1])
        top_right_pos = (rect[0] + rect[2], rect[1])
        bottom_left_pos = (rect[0], rect[1] + rect[3])
        bottom_right_pos = (rect[0] + rect[2], rect[1] + rect[3])
        top_left_val = color_channel[top_left_pos]
        top_right_val = color_channel[top_right_pos]
        bottom_left_val = color_channel[bottom_left_pos]
        bottom_right_val = color_channel[bottom_right_pos]

        # Check top left (move up) (move left)
        # Move up
        for offset in range(1, self.corner_check_dist + 1):
            if top_left_pos[1] - offset > 0:
                if abs(top_left_val - color_channel[top_left_pos[0], top_left_val[1] - offset]) < self.corner_diff_tol:
                    pass
        # Check top right (move up) (move right)

        # Check bottom left (move down) (move left)

        # Check bottom right (move down) (move right)

    @staticmethod
    def filter_lonelies(image, max_length):
        """

        :param image:
        :param max_length:
        :return:
        """
        # TODO: Func def
        for row in image:
            indices = []
            for i, col_val in enumerate(row):
                if col_val == 1:
                    indices.append(i)
                else:
                    if len(indices) <= max_length:
                        for index in indices:
                            row[index] = 0
                    indices = []
        for col in range(image.shape[1]):
            indices = []
            for i, row_val in enumerate(image[:, col]):
                if row_val == 1:
                    indices.append(i)
                else:
                    if len(indices) <= max_length:
                        for index in indices:
                            image[index][col] = 0
                    indices = []
        return image

    @staticmethod
    def get_working_image(image):
        image_cpy = image.copy()
        w = image_cpy.shape[1]
        h = image_cpy.shape[0]
        image_cpy = image_cpy[0:int(h / 2.5), 0:w]
        return image_cpy

# plt.figure(figsize=(16, 8))
# plt.imshow(areas_img, cmap=self.temp_color_channels_names[self.temp_color_channel_index])
# plt.title('Areas img')
# plt.axis('off')
# plt.tight_layout()
# plt.show()
