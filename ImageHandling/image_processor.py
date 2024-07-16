import cv2
import numpy as np


class ImageProcessor:
    def __init__(self):
        self.min_length = 3
        self.shape_edge_tolerance = 2  # Max num pixels to skip when checking for edge

    @staticmethod
    def vertical_image_split(image) -> tuple:
        """
        Cuts an image in half vertically and returns both halves
        :param image: Image to perform split on
        :return: tuple[,] - The two halves of the vertical split in the form (left, right)
        """
        width = int(image.shape[1] / 2)
        height = int(image.shape[0] / 2)
        x, y, w, h = 0, 0, width, height
        left_half_img = image[y:y + h, x:x + w]
        width = int(image.shape[1] / 2)
        height = int(image.shape[0] / 2)
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
    def detect_rects(gray_scale_image, tolerance=5):
        # Create an empty mask
        mask = np.zeros_like(gray_scale_image, dtype=np.uint8)

        # Iterate over each pixel and compare with neighbors
        rows, cols = gray_scale_image.shape
        x_center = int(cols / 2)
        for i in range(1, rows - 1):
            for j in range(1, cols - 1):
                # Check if neighboring pixels are within the tolerance
                if (abs(int(gray_scale_image[i, j]) - int(gray_scale_image[i - 1, j])) < tolerance and
                        abs(int(gray_scale_image[i, j]) - int(gray_scale_image[i + 1, j])) < tolerance and
                        abs(int(gray_scale_image[i, j]) - int(gray_scale_image[i, j - 1])) < tolerance and
                        abs(int(gray_scale_image[i, j]) - int(gray_scale_image[i, j + 1])) < tolerance):
                    mask[i, j] = 255

        cv2.imshow("Mask", mask)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        # Find contours in the mask
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Draw contours on a copy of the original image
        img_with_contours = gray_scale_image.copy()
        cv2.drawContours(img_with_contours, contours, -1, (0, 255, 0), 2)

        # Show the image with contours
        cv2.imshow("Contours", img_with_contours)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        rects = []
        for contour in contours:
            # Approximate contour to polygon
            epsilon = 0.02 * cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, epsilon, True)

            x, y, w, h = cv2.boundingRect(approx)
            checks = []
            # Check if valid

            min_required_area = 400
            max_center_deviation = 70
            max_width = 60
            max_height = 60
            max_pixel_range = 10
            # Check width and height
            if w < max_width and h < max_height:
                checks.append(True)
            else:
                # pass
                checks.append(False)
            # Check if area is greater than the minimum required
            if w * h > min_required_area:
                checks.append(True)
            else:
                # pass
                checks.append(False)
            # Check if near x center
            if abs(x + int(w / 2) - x_center) < max_center_deviation:
                checks.append(True)
            else:
                pass
                checks.append(False)
            # Check pixel range

            # Validate all checks
            final_check = True
            for check in checks:
                if not check:
                    final_check = False
                    break
            if final_check:
                rects.append((x, y, w, h))

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
            cv2.rectangle(image, (rect[0], rect[1]), (rect[0] + rect[2], rect[1] + rect[3]), (0, 255, 0), 2)

