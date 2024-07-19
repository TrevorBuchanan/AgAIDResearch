import cv2
import os


class ImageLoader:
    def __init__(self):
        pass

    @staticmethod
    def load_image(camera_name: str, image_name: str):
        """
        Gets image at given image name from files in ReferencePanelData/<camera_name>
        :param camera_name: str - Name of the camera directory to search in
        :param image_name: str - Name of image file to load
        :return: Image
        """
        root_dir = 'ReferencePanelData'
        camera_dir = os.path.join(root_dir, camera_name)
        image_path = os.path.join(camera_dir, f"{image_name}.png")

        # Ensure the directory exists
        if not os.path.isdir(camera_dir):
            raise FileNotFoundError(f"Directory {camera_dir} does not exist.")

        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image {image_name}.png not found in {camera_dir}.")

        image = cv2.imread(image_path)
        # Convert BGR image to RGB
        img_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        return img_rgb

    @staticmethod
    def load_all_images(camera_name: str):
        """
        Gets all images from the specified camera directory within ReferencePanelData.

        :param camera_name: str - Name of the camera directory to get images from.
        :return: List of images as NumPy arrays in RGB format.
        """
        root_dir = 'ReferencePanelData'
        camera_dir = os.path.join(root_dir, camera_name)

        # Ensure the directory exists
        if not os.path.isdir(camera_dir):
            raise FileNotFoundError(f"Directory {camera_dir} does not exist.")

        images = []
        image_names = []
        # Iterate over all files in the directory
        for filename in os.listdir(camera_dir):
            image_path = os.path.join(camera_dir, filename)

            # Read image if it's a file and has an image extension
            if os.path.isfile(image_path) and filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
                image = cv2.imread(image_path)

                if image is not None:
                    # Convert BGR image to RGB
                    img_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                    images.append(img_rgb)
                    image_names.append(filename)
                else:
                    print(f"Warning: Could not read image {filename}")

        return images, image_names
