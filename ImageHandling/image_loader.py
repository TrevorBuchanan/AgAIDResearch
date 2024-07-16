import cv2
import os


class ImageLoader:
    def __init__(self):
        pass

    @staticmethod
    def load_image(image_name: str):
        """
        Gets image at given image name from files in ReferencePanelData
        :param image_name: str - Name of image file to load
        :return: Image
        """
        root_dir = 'ReferencePanelData'
        image_path = None

        # Walk through all directories and files under root_dir
        for root, dirs, files in os.walk(root_dir):
            for file in files:
                if file == f"{image_name}.png":
                    image_path = os.path.join(root, file)
                    break
            if image_path:
                break
        if not image_path:
            print(f"Image {image_name}.png not found in {root_dir} or its subdirectories.")
            return
        image = cv2.imread(image_path)
        # Convert BGR image to RGB
        img_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        return img_rgb
