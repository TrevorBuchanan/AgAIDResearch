# By: Trevor Buchanan

from task_controller import TaskController


if __name__ == '__main__':
    print("AgAID Project\n")

    task_controller = TaskController()
    task_controller.run_image_processing_panel_detection_code('cam1', image_name='date_1-5-2024_12.19.46_1')
