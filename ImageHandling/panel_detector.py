from ImageHandling.image_loader import ImageLoader
from ImageHandling.image_processor import ImageProcessor
from math import sqrt

import cv2
import numpy as np
from Helpers.utility import find_max_rectangle, calculate_subsection_areas, get_bounding_rects


class PanelDetector:
    def __init__(self):
        self.image_loader = ImageLoader()
        self.image_processor = ImageProcessor()
        # Initial mask tolerance
        self.same_value_tolerance = 3
        # Edge pixel filter
        self.edge_diff_tol = 8
        self.edge_check_dist = 7
        self.min_good_edge_pixels = 70
        # Pixel range filter
        self.max_pixel_range = 8
        # Uniform filter
        self.uniform_tolerance = 8
        self.area_min = 175
        self.area_max = 500
        self.min_width = 10
        self.min_height = 10
        # Similarities tolerances
        self.near_tolerance = 12
        self.shape_tolerance = 20
        # Vertical line detection
        self.same_length = 3
        self.diff_length = 2
        self.same_tolerance = 8
        self.diff_tolerance = 7

    def get_panel_rects(self, camera_name, image_name):
        """

        :param camera_name:
        :param image_name:
        :return:
        """
        # TODO: Function def
        image = self.image_loader.load_image(camera_name, image_name)
        working_image = self.get_working_image(image)
        red_channel, green_channel, blue_channel = self.image_processor.separate_colors(working_image)
        gray_channel = self.image_processor.convert_to_gray(working_image)
        color_channels = [red_channel, green_channel, blue_channel, gray_channel]
        working_rects = set()
        for c in color_channels:
            for rec in self.get_possible_rects(c):
                working_rects.add(rec)
        working_rects = self.remove_duplicates(image, working_rects)
        good_rects = set()
        for c in color_channels:
            filtered_rects = self.filter_rects(c, list(working_rects))
            for r in filtered_rects:
                good_rects.add(r)
        good_rects = self.remove_duplicates(image, list(good_rects))
        self.image_processor.draw_rects_to_image(image, good_rects)
        image_bgr = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        cv2.imwrite('ImageObjectDetectionResults/detected.jpg', image_bgr)
        return good_rects

    def filter_rects(self, color_channel, rects):
        """

        :param color_channel:
        :param rects:
        :return:
        """
        # TODO: Function def
        filtered_rects = rects
        filtered_rects = self.filter_by_uniform_values(color_channel, filtered_rects)
        filtered_rects = self.filter_by_pixel_range(color_channel, filtered_rects)
        filtered_rects = self.filter_by_edges(color_channel, filtered_rects)
        return filtered_rects

    def filter_by_pixel_range(self, color_channel, rects):
        """

        :param color_channel:
        :param rects:
        :return:
        """
        filtered_rects = []
        for r in rects:
            pixel_range = self.get_pixel_range_for_rect(color_channel, r)
            if pixel_range <= self.max_pixel_range:
                filtered_rects.append(r)
        if not filtered_rects:
            return rects
        return filtered_rects

    def filter_by_uniform_values(self, color_channel, rects):
        """

        :param color_channel:
        :param rects:
        :return:
        """
        # TODO: Function def
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

        if not filtered_rects:
            return rects
        return filtered_rects

    def filter_by_edges(self, color_channel, rects):
        """

        :param color_channel:
        :param rects:
        :return:
        """
        # TODO: Function def
        filtered_rects = []
        for rect in rects:
            if self.check_edges(color_channel, rect):
                filtered_rects.append(rect)
        if not filtered_rects:
            return rects
        return filtered_rects

    def get_possible_rects(self, color_channel):
        """

        :param color_channel:
        :return:
        """
        # TODO: Function def
        areas_img = self.get_possible_areas(color_channel)
        bounding_rects = get_bounding_rects(areas_img)
        return bounding_rects

    def get_possible_areas(self, color_channel):
        """

        :param color_channel:
        :return:
        """
        # TODO: Function def
        bin_contours_img = self.get_binary_contours_img(color_channel)
        areas_img = calculate_subsection_areas(bin_contours_img)
        areas_img[areas_img < self.area_min] = 0
        areas_img[areas_img > self.area_max] = 0
        areas_img[(areas_img >= self.area_min) & (areas_img <= self.area_max)] = 1
        return areas_img

    def get_binary_contours_img(self, color_channel):
        """

        :param color_channel:
        :return:
        """
        # TODO: Function def
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
        return binary_contours_img

    def check_edges(self, color_channel, rect):
        """

        :param color_channel:
        :param rect:
        :return:
        """
        # TODO: Function def
        w = color_channel.shape[1]
        h = color_channel.shape[0]
        top_y = rect[1]
        left_x = rect[0]
        right_x = rect[0] + rect[2] - 1
        bottom_y = rect[1] + rect[3] - 1
        checks = [False] * ((rect[2] * 2) + (rect[3] * 2) + 4)
        check_index = 0
        # Top edge
        for x in range(left_x, right_x + 1):
            pixel_val = color_channel[top_y, x]
            for offset in range(1, self.edge_check_dist + 1):
                if top_y - offset >= 0:
                    if abs(np.subtract(pixel_val, color_channel[top_y - offset, x],
                                       dtype=np.float64)) > self.edge_diff_tol:
                        checks[check_index] = True
            check_index += 1
        # Left edge
        for y in range(top_y, bottom_y + 1):
            pixel_val = color_channel[y, left_x]
            for offset in range(1, self.edge_check_dist + 1):
                if left_x - offset >= 0:
                    if abs(np.subtract(pixel_val, color_channel[y, left_x - offset],
                                       dtype=np.float64)) > self.edge_diff_tol:
                        checks[check_index] = True
            check_index += 1
        # Right edge
        for y in range(top_y, bottom_y + 1):
            pixel_val = color_channel[y, right_x]
            for offset in range(1, self.edge_check_dist + 1):
                if right_x + offset < w:
                    if abs(np.subtract(pixel_val, color_channel[y, right_x + offset],
                                       dtype=np.float64)) > self.edge_diff_tol:
                        checks[check_index] = True
            check_index += 1
        # Bottom edge
        for x in range(left_x, right_x + 1):
            pixel_val = color_channel[bottom_y, x]
            for offset in range(1, self.edge_check_dist + 1):
                if bottom_y + offset < h:
                    if abs(np.subtract(pixel_val, color_channel[bottom_y + offset, x],
                                       dtype=np.float64)) > self.edge_diff_tol:
                        checks[check_index] = True
            check_index += 1
        num_good_pixels = len(list(filter(lambda check: check is True, checks)))
        return num_good_pixels >= self.min_good_edge_pixels

    def remove_duplicates(self, image, rects):  # Removes if within similar tolerances
        """

        :param image:
        :param rects:
        :return:
        """
        # TODO: Function def
        filtered_rects = []
        similar_rects = -1
        remaining_rects = []
        for rect1 in rects:
            if similar_rects == -1:
                remaining_rects = rects
            similar_rects = set()
            for rect2 in remaining_rects:
                if rect1 != rect2:
                    if self.is_near(rect1, rect2, self.near_tolerance) and \
                            self.is_shape_similar(rect1, rect2, self.shape_tolerance):
                        similar_rects.add(rect1)
                        similar_rects.add(rect2)
            similar_rects_list = list(similar_rects)
            if not similar_rects_list:
                is_similar = False
                for r in filtered_rects:
                    if self.is_near(rect1, r, self.near_tolerance) and \
                            self.is_shape_similar(rect1, r, self.shape_tolerance):
                        is_similar = True
                if not is_similar:
                    similar_rects_list.append(rect1)
                else:
                    continue
            pixel_ranges = []
            for r in similar_rects_list:
                pixel_ranges.append(self.get_pixel_range_for_rect(image, r))
            lowest_range_index = pixel_ranges.index(min(pixel_ranges))
            filtered_rects.append(similar_rects_list[lowest_range_index])

            temp_remaining = []
            for rect in remaining_rects:
                if rect not in similar_rects_list:
                    temp_remaining.append(rect)
            remaining_rects = temp_remaining
        return filtered_rects

    @staticmethod
    def filter_lonelies(image, max_length):
        """

        :param image:
        :param max_length:
        :return:
        """
        # TODO: Function def
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
        """

        :param image:
        :return:
        """
        # TODO: Function def
        image_cpy = image.copy()
        w = image_cpy.shape[1]
        h = image_cpy.shape[0]
        image_cpy = image_cpy[0:int(h / 2.5), 0:w]
        return image_cpy

    @staticmethod
    def is_shape_similar(rect1, rect2, tolerance):
        """

        :param rect1:
        :param rect2:
        :param tolerance:
        :return:
        """
        # TODO: Func def
        w1 = rect1[2]
        h1 = rect1[3]
        w2 = rect2[2]
        h2 = rect2[3]
        width_diff = abs(w2 - w1)
        height_diff = abs(h2 - h1)
        return width_diff < tolerance and height_diff < tolerance

    @staticmethod
    def is_near(rect1, rect2, tolerance):
        """

        :param rect1:
        :param rect2:
        :param tolerance:
        :return:
        """
        # TODO: Func def
        x1 = rect1[0]
        y1 = rect1[1]
        x2 = rect2[0]
        y2 = rect2[1]
        distance = sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        return distance < tolerance

    @staticmethod
    def get_pixel_range_for_rect(image, rect):
        """
        Finds the range from the darkest to the lightest pixel in a given rectangle portion of an image
        :param image: The image to find pixel range from (in given rectangle)
        :param rect:
        :return: Range from the highest value pixel to the lowest value pixel in the given rectangle region
        """
        # TODO: Add function def
        x, y, width, height = rect
        # Ensure the provided rectangle coordinates are within the image bounds
        h, w = image.shape[:2]
        if x < 0 or y < 0 or x + width > w or y + height > h:
            raise ValueError("Rectangle coordinates are out of image bounds.")

        # Extract the rectangle portion of the image
        rect = image[y:y + height, x:x + width]

        # Compute the pixel values in the rectangle
        # If the image is multichannel, convert it to grayscale
        if len(rect.shape) == 3:
            rect = np.mean(rect, axis=2)

        # Find the minimum and maximum pixel values
        min_pixel_value = np.min(rect)
        max_pixel_value = np.max(rect)

        return max_pixel_value - min_pixel_value
