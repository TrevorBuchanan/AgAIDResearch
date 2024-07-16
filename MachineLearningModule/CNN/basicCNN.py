import cv2
import numpy as np
from matplotlib import pyplot as plt

min_length = 3

def is_vertical_line(image_arr, i, j):
    line_len = 0
    initial_val = image_arr[i, j]
    for k, _ in enumerate(image_arr):
        for l, _ in enumerate(image_arr[k]):
            if image_arr[l, k] == 255:
                line_len += 1
            else:
                if
    if line_len > 0:
        return 0


def is_horizontal_line(image_arr, i, j):
    for k, _ in enumerate(image_arr):
        for l, _ in enumerate(image_arr[k]):
            image_arr[k]


def find_shapes(image):
    range_tolerance = 9
    shape_edge_tolerance = 2  # Max num pixels to skip when checking for edge

    # Initialize a 2D array (grayscale) based on image dimensions
    processed_img = np.zeros((height, width), dtype=np.uint8)

    # Filter for sign
    for i, _ in enumerate(image):
        for j, _ in enumerate(image[i]):
            neighbors = get_neighbors(image, i, j)
            if max(neighbors) - min(neighbors) < range_tolerance:
                processed_img[i, j] = 255

    # Convert to grayscale if the image is in RGB
    if len(processed_img.shape) == 3:
        gray = cv2.cvtColor([processed_img], cv2.COLOR_BGR2GRAY)
    else:
        gray = processed_img

    # Find lines
    for i, _ in enumerate(image):
        for j, _ in enumerate(image[i]):
            if is_horizontal_line(image, i, j) and is_vertical_line(image, i, j):


    rectangles = [(50, 80, 12, 64)]

    return rectangles

def find_vertical_lines(image):
    pass

# Function to get neighbors
def get_neighbors(arr, row, col):
    surrounding_neighbors = []
    rows, cols = arr.shape

    # Define relative positions of 8 neighboring cells
    directions = [(-1, -1), (-1, 0), (-1, 1),
                  (0, -1), (0, 1),
                  (1, -1), (1, 0), (1, 1)]

    for dr, dc in directions:
        r, c = row + dr, col + dc
        if 0 <= r < rows and 0 <= c < cols:
            surrounding_neighbors.append(arr[r, c])

    return surrounding_neighbors


# Opening image
img = cv2.imread("image.png")

# Convert BGR image to RGB
img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# Get image dimensions
height, width, channels = img.shape

# Split channels
red_channel = img_rgb[:, :, 0]
green_channel = img_rgb[:, :, 1]
blue_channel = img_rgb[:, :, 2]

# Convert to grayscale
img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2GRAY)

# Display the original image and channels
plt.figure(figsize=(16, 8))

plt.subplot(2, 3, 1)
plt.imshow(img_rgb)
plt.title('Original RGB Image')
plt.axis('off')

plt.subplot(2, 3, 2)
plt.imshow(red_channel, cmap='Reds')
plt.title('Red Channel')
plt.axis('off')

plt.subplot(2, 3, 3)
plt.imshow(green_channel, cmap='Greens')
plt.title('Green Channel')
plt.axis('off')

plt.subplot(2, 3, 4)
plt.imshow(blue_channel, cmap='Blues')
plt.title('Blue Channel')
plt.axis('off')

plt.subplot(2, 3, 5)
plt.imshow(img_gray, cmap='gray')
plt.title('Grayscale Image')
plt.axis('off')

# Edge detection
# edges_img = np.zeros(processed_img.shape)
# for i, _ in enumerate(filtered_img):
#     for j, _ in enumerate(filtered_img[i]):
#         line = filtered_img[i][j:-1]
#         # Try right
#         print(line)
#         for k, _ in enumerate(line):
#             if abs(line[k] - line[k + 1]) < range_tolerance:


# Find rectangles
rectangles = find_shapes(img_gray)

# Draw rectangles on the original image
for rect in rectangles:
    cv2.rectangle(img_rgb, (rect[0], rect[1]), (rect[0] + rect[2], rect[1] + rect[3]), (0, 255, 0), 2)

x = 800
y = 300
width = 50
height = 70

# Specify subplot
plt.subplot(2, 3, 6)
# Draw the rectangle
# cv2.rectangle(img_rgb, (x, y), (x + width, y + height), (0, 255, 0), 2)
# Display the result
plt.imshow(img_rgb)
# plt.imshow(filtered_img, cmap='gray', vmin=0, vmax=255)
plt.axis('off')
plt.tight_layout()
plt.show()
