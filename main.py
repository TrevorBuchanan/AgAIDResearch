# By: Trevor Buchanan

from task_controller import TaskController


if __name__ == '__main__':
    print("AgAID Project\n")

    # See project notes for documentation of saved models and all other project details
    task_controller = TaskController()

    # IMAGE PROCESSING - (Results saved in ImageObjectDetectionResults)
    # task_controller.panel_detection('image_process', 'cam1', image_name='date_1-6-2024_13.0.11_1')
    # task_controller.panel_detection('roboflow', 'cam1', image_name='date_1-6-2024_13.0.11_1')
    # task_controller.panel_detection('yolo', 'cam1', image_name='date_1-6-2024_13.0.11_1')

    # YIELD PREDICTION
    # task_controller.yield_prediction(model_num=14, saved_data_set_num=8, season="winter", visualize_training=True)
    # task_controller.yield_prediction(model_num=1, saved_data_set_num=1, season="spring", visualize_test=True)
