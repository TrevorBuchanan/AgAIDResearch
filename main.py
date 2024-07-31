# By: Trevor Buchanan

from task_controller import TaskController


if __name__ == '__main__':
    print("AgAID Project\n")

    task_controller = TaskController()
    # IMAGE PROCESSING
    # task_controller.run_image_processing_panel_detection_code('cam1', image_name='date_1-5-2024_12.19.46_1')
    task_controller.run_machine_learning_panel_detection_code('cam1', image_name='date_1-6-2024_13.0.11_1.png')

    # YIELD PREDICTION
    # See project notes for documentation of saved models
    # task_controller.run_yield_prediction_code(model_num=14, saved_data_set_num=8,
    #                                           season="winter", visualize_training=True)
    # task_controller.run_yield_prediction_code(model_num=1, saved_data_set_num=1, season="spring", visualize_test=True)
