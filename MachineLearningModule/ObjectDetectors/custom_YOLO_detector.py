import cv2
import torch

from ImageHandling.image_loader import ImageLoader


class CustomYOLODetector:
    def __init__(self):
        self.image_loader = ImageLoader()

    def get_panel_rects(self, camera_name, image_name):
        """

        :param camera_name:
        :param image_name:
        :return:
        """
        image_path = self.image_loader.get_image_path(camera_name, image_name)
        img = cv2.imread(image_path)
        model = torch.hub.load('ultralytics/yolov5', 'custom', path='MachineLearningModule/ObjectDetectors/'
                                                                    'CustomYOLOModel/custom_yolo_v5.pt')
        results = model(img)
        desired_classes = ['Panel']
        filtered_results = results.pandas().xyxy[0]
        filtered_results = filtered_results[filtered_results['name'].isin(desired_classes)]
        # List to store rectangles
        rects = []
        for _, row in filtered_results.iterrows():
            x1, y1, x2, y2, conf, cls, name = row
            cv2.rectangle(img, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
            cv2.putText(img, f'{name} {conf:.2f}', (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9,
                        (36, 255, 12), 2)
            rects.append([int(x1), int(y1), int(x2 - x1), int(y2 - y1)])

        cv2.imwrite('ImageObjectDetectionResults/detected.jpg', img)
        return rects
