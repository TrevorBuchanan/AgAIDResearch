from roboflow import Roboflow

from ImageHandling.image_loader import ImageLoader


class RoboFlowDetector:
    def __init__(self):
        self.version = 1
        self.image_loader = ImageLoader()

    def get_rects(self, image_name):
        image_path = self.image_loader.get_image_path(image_name)
        rf = Roboflow(api_key="ubYr4GBtztqwxYsNZbqJ")
        project = rf.workspace().project("MODEL_ENDPOINT")
        model = project.version(self.version).model

        # infer on a local image
        # print(model.predict(image_path, confidence=40, overlap=30).json())

        # visualize your prediction
        model.predict(image_path, confidence=40, overlap=30).save("prediction.jpg")
