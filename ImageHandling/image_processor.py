import cv2
import numpy as np
from matplotlib import pyplot as plt

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

    def detect_rects(self, gray_scale_image, tolerance=4, show_mask=False, show_rects_masks=False, show_contours=False):
        # Create an empty mask
        mask = np.zeros_like(gray_scale_image, dtype=np.uint8)

        # Iterate over each pixel and compare with neighbors
        rows, cols = gray_scale_image.shape
        # x_center = int(cols / 2)
        for i in range(1, rows - 1):
            for j in range(1, cols - 1):
                # Check if neighboring pixels are within the tolerance
                if (abs(int(gray_scale_image[i, j]) - int(gray_scale_image[i - 1, j])) < tolerance and
                        abs(int(gray_scale_image[i, j]) - int(gray_scale_image[i + 1, j])) < tolerance and
                        abs(int(gray_scale_image[i, j]) - int(gray_scale_image[i, j - 1])) < tolerance and
                        abs(int(gray_scale_image[i, j]) - int(gray_scale_image[i, j + 1])) < tolerance):
                    mask[i, j] = 255

        # Show mask
        if show_mask:
            plt.figure(figsize=(16, 8))
            plt.imshow(mask, cmap='gray')
            plt.axis('off')
            plt.tight_layout()
            plt.show()

        edges = cv2.Canny(mask, 50, 150)
        plt.figure(figsize=(16, 8))
        plt.imshow(edges, cmap='gray')
        plt.axis('off')
        plt.tight_layout()
        plt.show()

        # Find contours in the mask
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Draw contours on a copy of the original image
        img_with_contours = gray_scale_image.copy()
        cv2.drawContours(img_with_contours, contours, -1, (0, 255, 0), 2)

        # Show the image with contours
        if show_contours:
            plt.figure(figsize=(16, 8))
            plt.imshow(img_with_contours, cmap='gray')
            plt.axis('off')
            plt.tight_layout()
            plt.show()

        # Create a blank image to draw filled contours
        outlines_image = np.zeros_like(img_with_contours)

        for contour in contours:
            # Draw filled contour on the blank image
            cv2.drawContours(outlines_image, [contour], -1, (255,), thickness=cv2.FILLED)

        rects = []

        # Loop through contours and approximate to polygon
        for contour in contours:
            epsilon = 0.01 * cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, epsilon, True)

            # Get bounding rect and draw it
            x, y, w, h = cv2.boundingRect(approx)
            # Check if valid
            min_required_area = 250
            max_width = 50
            max_height = 50
            # Check width and height
            if w > max_width or h > max_height:
                pass
                # continue
            # Check if area is greater than the minimum required
            if w * h < min_required_area:
                pass
                # continue
            rects.append((x, y, w, h))
        rects = self.filter_rects(gray_scale_image, rects, 7, show_mask=show_rects_masks)
        return rects

    @staticmethod
    def draw_rects_to_left_image(image, rectangles: list) -> None:
        """
        Draws given rectangle list on to image
        :param image: The image to draw to
        :param rectangles: list - List of tuple rectangles in the form (x pos, y pos, width, height)
        :return: None
        """
        # Draw rectangles on the original image
        for rect in rectangles:
            cv2.rectangle(image, (rect[0], rect[1]), (rect[0] + rect[2], rect[1] + rect[3]), (0, 255, 0), 2)

    @staticmethod
    def draw_rects_to_right_image(image, rectangles: list) -> None:
        """
        Draws given rectangle list on to image
        :param image: The image to draw to
        :param rectangles: list - List of tuple rectangles in the form (x pos, y pos, width, height)
        :return: None
        """
        width_offset = int(image.shape[1] / 2)
        # Draw rectangles on the original image
        for rect in rectangles:
            cv2.rectangle(image, (rect[0] + width_offset, rect[1]), (rect[0] + width_offset + rect[2],
                                                                     rect[1] + rect[3]), (0, 255, 0), 2)

    @staticmethod
    def get_pixel_range_for_rect(image, x: int, y: int, width: int, height: int):
        """
        Finds the range from the darkest to the lightest pixel in a given rectangle portion of an image
        :param image: The image to find pixel range from (in given rectangle)
        :param x: int - The x position of the desired rectangle
        :param y: int - The y position of the desired rectangle
        :param width: int - The width position of the desired rectangle
        :param height: int - The height position of the desired rectangle
        :return: Range from the highest value pixel to the lowest value pixel in the given rectangle region
        """
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

    def filter_rects(self, gray_scale_image, rectangles, tolerance, show_mask=False):  # Temp Name
        valid_rects = []
        for rect in rectangles:
            scaled_image = gray_scale_image[rect[1]:rect[1] + rect[3], rect[0]:rect[0] + rect[2]]
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
                temp = gray_scale_image
                self.draw_rects_to_left_image(temp, [rect])
                plt.imshow(gray_scale_image, cmap='gray')
                plt.axis('off')
                plt.tight_layout()
                plt.show()

            # Cropping
            binary_array = mask / 255
            x, y, w, h = find_max_rectangle(binary_array)
            total_x = x + rect[0]
            total_y = y + rect[1]

            # Check if valid
            min_required_area = 250
            max_width = 50
            max_height = 50
            # Check width and height
            if w > max_width or h > max_height:
                pass
                # continue
            # Check if area is greater than the minimum required
            if w * h < min_required_area:
                pass
                # continue

            valid_rects.append((total_x, total_y, w, h))

        return valid_rects

    @staticmethod
    def filter_rects_to_similar_location(rects1, rects2):
        """

        :param rects1:
        :param rects2:
        :return:
        """
        pass