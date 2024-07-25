# By: Trevor Buchanan

from MachineLearningModule.ObjectDetecters.RoboFlowDetector import RoboFlowDetector
from task_controller import TaskController


if __name__ == '__main__':
    print("AgAID Project\n")

    # task_controller = TaskController()

    # _______________________________________________________________________________
    image_name = 'date_29-4-2024_10.0.10_1.png'
    robo_flow_detector = RoboFlowDetector()
    robo_flow_detector.get_rects(image_name)
    exit(0)


    # ________________________________________________________________________________________________________
