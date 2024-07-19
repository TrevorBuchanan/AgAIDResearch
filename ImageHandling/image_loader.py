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

        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image {image_name}.png not found in {camera_dir}.")

        image = cv2.imread(image_path)
        # Convert BGR image to RGB
        img_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        return img_rgb
