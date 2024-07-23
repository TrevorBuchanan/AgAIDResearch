from math import sqrt

import cv2
import numpy as np
from matplotlib import pyplot as plt
from scipy.ndimage import convolve
from Helpers.utility import find_max_rectangle


class ImageProcessor:
    def __init__(self):
        pass

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

    def get_rects(self, image):
        image_cpy = image.copy()
        w = image_cpy.shape[1]
        h = image_cpy.shape[0]
        image_cpy = image_cpy[0:int(h / 2), 0:w]
        red_channel, green_channel, blue_channel = self.separate_colors(image_cpy)
        gray_channel = self.convert_to_gray(image_cpy)
        image_channels = [red_channel, green_channel, blue_channel, gray_channel]
        rects_list = []
        for image_channel in image_channels:
            rectangles = self.detect_rects(image_channel, show_mask=False, show_contours=False)
            rects_list.append(rectangles)

        # TEMP
        # colors = ['Reds', 'Greens', 'Blues', 'gray']
        # for ch, r, c in zip(image_channels, rects_list, colors):
        #     cpy = ch.copy()
        #     self.draw_rects_to_image(cpy, r)
        #     plt.figure(figsize=(16, 8))
        #     plt.imshow(cpy, cmap=c)
        #     plt.axis('off')
        #     plt.tight_layout()
        #     plt.show()
        # TEMP
        rects = self.get_best_rects(image_channels, rects_list)
        rects = self.filter_near_duplicates(rects)
        # rects = self.filter_rects_using_vertical_lines(image_channels, rects)
        # TEMP
        # cpy = image.copy()
        # self.draw_rects_to_image(cpy, rects)
        # plt.figure(figsize=(16, 8))
        # plt.imshow(cpy)
        # plt.title('Total rects')
        # plt.axis('off')
        # plt.tight_layout()
        # plt.show()
        # TEMP
        return rects

    def get_best_rects(self, image_channels, rects_list):
        best_rects = []
        tolerance = 10
        for image_channel1, rects1 in zip(image_channels, rects_list):
            for image_channel2, rects2 in zip(image_channels, rects_list):
                if image_channel1 is not image_channel2:
                    for rect1 in rects1:
                        for rect2 in rects2:
                            if self.is_near(rect1, rect2, tolerance):
                                pixel_ranges1 = []
                                pixel_ranges2 = []
                                for image_channel in image_channels:
                                    pixel_ranges1.append(self.get_pixel_range_for_rect(image_channel, rect1))
                                    pixel_ranges2.append(self.get_pixel_range_for_rect(image_channel, rect2))
                                pixel_range1 = sum(pixel_ranges1) / len(pixel_ranges1)
                                pixel_range2 = sum(pixel_ranges2) / len(pixel_ranges2)
                                if pixel_range1 < pixel_range2:
                                    best_rects.append(rect1)
                                else:
                                    best_rects.append(rect2)
        return best_rects

    @staticmethod
    def is_near(rect1, rect2, tolerance):
        center1_x = rect1[0] + rect1[2] / 2
        center1_y = rect1[1] + rect1[3] / 2
        center2_x = rect2[0] + rect2[2] / 2
        center2_y = rect2[1] + rect2[3] / 2
        distance = sqrt((center2_x - center1_x)**2 + (center2_y - center1_y)**2)
        return distance < tolerance

    def detect_rects(self, image_channel, tolerance=3, show_mask=False, show_rects_masks=False, show_contours=False):
        # Create an empty mask
        mask = np.zeros_like(image_channel, dtype=np.uint8)

        # Iterate over each pixel and compare with neighbors
        rows, cols = image_channel.shape
        for i in range(1, rows - 1):
            for j in range(1, cols - 1):
                # Check if neighboring pixels are within the tolerance
                if (abs(int(image_channel[i, j]) - int(image_channel[i - 1, j])) < tolerance and
                        abs(int(image_channel[i, j]) - int(image_channel[i + 1, j])) < tolerance and
                        abs(int(image_channel[i, j]) - int(image_channel[i, j - 1])) < tolerance and
                        abs(int(image_channel[i, j]) - int(image_channel[i, j + 1])) < tolerance):
                    mask[i, j] = 255

        # Show mask
        if show_mask:
            plt.figure(figsize=(16, 8))
            plt.imshow(mask, cmap='gray')
            plt.title('Mask')
            plt.axis('off')
            plt.tight_layout()
            plt.show()

        # Find contours in the mask
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Draw contours on a copy of the original image
        img_with_contours = image_channel.copy()
        cv2.drawContours(img_with_contours, contours, -1, (255,), thickness=cv2.FILLED)

        binary_contours = img_with_contours.copy()
        binary_contours[binary_contours != 255] = 0
        binary_contours[binary_contours == 255] = 1
        self.filter_lonelies(binary_contours, 5)

        if binary_contours.dtype != np.uint8:
            binary_contours = cv2.convertScaleAbs(binary_contours)
        contours2, _ = cv2.findContours(binary_contours, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Show the image with contours
        if show_contours:
            plt.figure(figsize=(16, 8))
            plt.imshow(img_with_contours, cmap='gray')
            plt.title('Contours')
            plt.axis('off')
            plt.tight_layout()
            plt.show()

            plt.figure(figsize=(16, 8))
            plt.imshow(binary_contours, cmap='gray')
            plt.title('Binary contours')
            plt.axis('off')
            plt.tight_layout()
            plt.show()

        rects = []
        # Check if valid
        min_required_area = 300
        max_width = 40
        max_height = 40
        # Loop through contours and approximate to polygon
        for contour in contours:
            # Get bounding rect and draw it
            x, y, w, h = cv2.boundingRect(contour)
            max_height = 50
            # Check width and height
            if w > max_width or h > max_height:
                pass
                continue
            # Check if area is greater than the minimum required
            if w * h < min_required_area:
                pass
                continue
            rects.append((x, y, w, h))
        for contour in contours:
            epsilon = 0.01 * cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, epsilon, True)

            # Get bounding rect and draw it
            x, y, w, h = cv2.boundingRect(approx)
            # Check width and height
            if w > max_width or h > max_height:
                continue
            # Check if area is greater than the minimum required
            if w * h < min_required_area:
                continue
            rects.append((x, y, w, h))
        for contour in contours2:
            # Get bounding rect and draw it
            x, y, w, h = cv2.boundingRect(contour)
            # Check width and height
            if w > max_width or h > max_height:
                continue
            # Check if area is greater than the minimum required
            if w * h < min_required_area:
                continue
            rects.append((x, y, w, h))
        for contour in contours2:
            epsilon = 0.01 * cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, epsilon, True)

            # Get bounding rect and draw it
            x, y, w, h = cv2.boundingRect(approx)
            # Check width and height
            if w > max_width or h > max_height:
                continue
            # Check if area is greater than the minimum required
            if w * h < min_required_area:
                continue
            rects.append((x, y, w, h))
        for r in rects:
            self.get_pixel_range_for_rect(image_channel, r)
        rects = self.filter_rects_by_uniform_value(image_channel, rects, 8, show_mask=show_rects_masks)
        for r in rects:
            self.get_pixel_range_for_rect(image_channel, r)
        return rects

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
        # If the image is multi-channel, convert it to grayscale
        if len(rect.shape) == 3:
            rect = np.mean(rect, axis=2)

        # Find the minimum and maximum pixel values
        min_pixel_value = np.min(rect)
        max_pixel_value = np.max(rect)

        return max_pixel_value - min_pixel_value

    def filter_rects_by_uniform_value(self, image_channel, rectangles, tolerance, show_mask=False):
        """

        :param image_channel:
        :param rectangles:
        :param tolerance:
        :param show_mask:
        :return:
        """
        # TODO: Add def
        valid_rects = []
        for rect in rectangles:
            scaled_image = image_channel[rect[1]:rect[1] + rect[3], rect[0]:rect[0] + rect[2]]

            # Create an empty mask
            mask = np.zeros_like(scaled_image, dtype=np.uint8)

            # Iterate over each pixel and compare with neighbors
            rows, cols = scaled_image.shape
            for i in range(1, rows - 1):
                for j in range(1, cols - 1):
                    # Check if neighboring pixels are within the tolerance
                    if (abs(int(scaled_image[i, j]) - int(scaled_image[i - 1, j])) < tolerance and
                            abs(int(scaled_image[i, j]) - int(scaled_image[i + 1, j])) < tolerance and
                            abs(int(scaled_image[i, j]) - int(scaled_image[i, j - 1])) < tolerance and
                            abs(int(scaled_image[i, j]) - int(scaled_image[i, j + 1])) < tolerance):
                        mask[i, j] = 255

            # Show mask
            if show_mask:
                plt.figure(figsize=(16, 8))
                plt.subplot(1, 2, 1)
                plt.imshow(mask, cmap='gray')
                plt.axis('off')
                plt.subplot(1, 2, 2)
                temp = image_channel.copy()
                self.draw_rects_to_image(temp, [rect])
                plt.imshow(temp, cmap='gray')
                plt.axis('off')
                plt.tight_layout()
                plt.show()

            # Cropping
            binary_array = mask / 255
            x, y, w, h = find_max_rectangle(binary_array)
            total_x = x + rect[0]
            total_y = y + rect[1]

            # Check if valid
            min_required_area = 275
            min_width = 8
            min_height = 8
            # Check if area is greater than the minimum required
            if w * h < min_required_area:
                continue
            # Check if length and width are greater than min
            if w < min_width or h < min_height:
                continue
            valid_rects.append((total_x, total_y, w, h))

        return valid_rects

    @staticmethod
    def filter_rects_to_similar_location(rects1, rects2, tolerance=50):
        """

        :param rects1:
        :param rects2:
        :param tolerance:
        :return:
        """
        # TODO: Func def
        filtered_rects1, filtered_rects2 = [], []

        for r1 in rects1:
            for r2 in rects2:
                if (r1[0] + (int(r1[2])/2)) - (r2[0] + (int(r2[2])/2)) < tolerance and \
                        (r1[1] + (int(r1[3])/2)) - (r2[1] + (int(r2[3])/2)) < tolerance:
                    filtered_rects1.append(r1)
                    filtered_rects2.append(r2)
        return filtered_rects1, filtered_rects2

    @staticmethod
    def filter_lonelies(image, max_length):
        """

        :param image:
        :param max_length:
        :return:
        """
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
        for col in range(image.shape[1]):  # arr.shape[1] gives the number of columns
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

    def filter_near_duplicates(self, rects, tolerance=10):
        """
        Filters out near duplicate rectangles based on the given tolerance.
        :param rects: List of rectangles, where each rectangle is represented as a tuple (x1, y1, x2, y2).
        :param tolerance: Tolerance for considering rectangles as near duplicates.
        :return: List of filtered rectangles with duplicates removed.
        """
        filtered_rects = []

        for rect1 in rects:
            is_duplicate = False
            for rect2 in filtered_rects:
                if self.is_near(rect1, rect2, tolerance):
                    is_duplicate = True
                    break

            if not is_duplicate:
                filtered_rects.append(rect1)

        return filtered_rects

    @staticmethod
    def find_vertical_lines(image_channel):
        """

        :param image_channel:
        :return:
        """
        # TODO: Function def
        same_length = 3
        diff_length = 2
        same_tolerance = 8
        diff_tolerance = 7

        def safe_access(arr, i, j):
            if 0 <= i < arr.shape[0] and 0 <= j < arr.shape[1]:
                return arr[i, j]
            return None

        def filter_vertical_lonelies(arr, max_length):
            for col in range(arr.shape[1]):  # arr.shape[1] gives the number of columns
                indices = []
                for k, r_val in enumerate(arr[:, col]):
                    if r_val == 1:
                        indices.append(k)
                    else:
                        if len(indices) <= max_length:
                            for index in indices:
                                arr[index][col] = 0
                        indices = []
            return arr

        mask = np.zeros_like(image_channel)
        bin_mask = np.zeros_like(image_channel)

        for j in range(image_channel.shape[1]):
            for i in range(image_channel.shape[0]):
                row_val = image_channel[i, j]
                left_good, right_good = False, False
                for offset in range(1, diff_length + 1):
                    right = safe_access(image_channel, i, j + offset)
                    left = safe_access(image_channel, i, j - offset)
                    if right is not None and left is not None:
                        if abs(np.subtract(right, row_val, dtype=np.float64)) >= diff_tolerance:
                            right_good = True
                        if abs(np.subtract(left, row_val, dtype=np.float64)) >= diff_tolerance:
                            left_good = True

                is_within_tolerance = True
                for offset in range(1, same_length + 1):
                    above = safe_access(image_channel, i + offset, j)
                    below = safe_access(image_channel, i - offset, j)
                    if above is not None and below is not None:
                        if abs(np.subtract(above, row_val, dtype=np.float64)) >= same_tolerance or \
                                abs(np.subtract(below, row_val, dtype=np.float64)) >= same_tolerance:
                            is_within_tolerance = False
                            break
                    else:
                        is_within_tolerance = False
                        break

                if is_within_tolerance and left_good and right_good:
                    mask[i, j] = 0
                    bin_mask[i, j] = 1
                else:
                    mask[i, j] = image_channel[i, j]

        bin_mask = filter_vertical_lonelies(bin_mask, 10)
        # plt.figure(figsize=(16, 8))
        # plt.title('Bin Mask')
        # plt.imshow(bin_mask, cmap='gray')
        # plt.axis('off')
        # plt.tight_layout()
        # plt.show()
        #
        # plt.figure(figsize=(16, 8))
        # plt.title('Mask')
        # plt.imshow(mask, cmap='gray')
        # plt.axis('off')
        # plt.tight_layout()
        # plt.show()
        return bin_mask

    def filter_rects_using_vertical_lines(self, image_channels, rects):
        """

        :param image_channels:
        :param rects:
        :return:
        """

        def get_segment(arr, rect, h):
            x = rect[0]
            y = rect[1]
            width = rect[2]
            height = rect[3]
            end_x = x + width
            end_y = y + h + height
            if end_x > arr.shape[1]:
                end_x = arr.shape[1]
            if end_y > arr.shape[0]:
                end_y = arr.shape[0]
            segment = arr[y:end_y, x:end_x]
            return segment

        def pad_ones(array, pad):
            kernel = np.ones((2 * pad + 1, 2 * pad + 1), dtype=np.uint8)
            padded_array = convolve(array, kernel, mode='constant', cval=0)
            padded_array = (padded_array > 0).astype(np.uint8)
            return padded_array

        # TODO: Function def
        valid_rects = []
        segment_height = 150
        total_bin_mask = np.zeros_like(image_channels[0])
        for k, image_channel in enumerate(image_channels):
            bin_mask = self.find_vertical_lines(image_channel)
            bin_mask = pad_ones(bin_mask, 1)
            total_bin_mask = bin_mask
            total_bin_mask = total_bin_mask & bin_mask

        # plt.figure(figsize=(16, 8))
        # plt.title('Full bin mask')
        # plt.imshow(total_bin_mask, cmap='gray')
        # plt.axis('off')
        # plt.tight_layout()
        # plt.show()
        for i, r in enumerate(rects):
            array_segment = get_segment(total_bin_mask, r, segment_height)
            if np.isin(1, array_segment):
                valid_rects.append(r)
        if len(valid_rects) == 0:
            return rects
        return valid_rects
