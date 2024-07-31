from roboflow import Roboflow

from ImageHandling.image_loader import ImageLoader


class RoboFlowDetector:
    def __init__(self):
        self.version = 1
        self.image_loader = ImageLoader()

    def get_panel_rects(self, camera_name, image_name):
        """

        :param camera_name:
        :param image_name:
        :return:
        """
        # TODO: Function def
        image_path = self.image_loader.get_image_path(camera_name, image_name)
        rf = Roboflow(api_key="ubYr4GBtztqwxYsNZbqJ")

        try:
            workspace = rf.workspace()
            # print("Workspace loaded:", workspace)

            # Use the correct project ID
            project_id = "agaid-object-detection"  # Update this to the correct project ID
            project = workspace.project(project_id)
            # print("Project loaded:", project)

            model = project.version(self.version).model
            # print("Model loaded:", model)

            # Infer on a local image
            prediction = model.predict(image_path, confidence=40, overlap=30).json()

            # Extract rectangle coordinates
            rects = []
            for pred in prediction['predictions']:
                x = pred['x']
                y = pred['y']
                width = pred['width']
                height = pred['height']
                rects.append((x, y, width, height))

            # Visualize your prediction
            model.predict(image_path, confidence=40, overlap=30).save("ImageObjectDetectionResults/detected.jpg")

            return rects

        except Exception as e:
            print("Error occurred:", e)
            return None
