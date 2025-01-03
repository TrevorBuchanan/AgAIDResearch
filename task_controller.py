import csv

from DataStructures.plot import Plot

from Helpers.utility import get_plot, normalize_all_of_attr, calculate_rmse, convert_int_to_str_date
from Helpers.visualizer import Visualizer
from Helpers.parser import Parser

from MachineLearningModule.LSTM.vanillaLSTM import VanillaLSTM
from MachineLearningModule.ObjectDetectors.custom_YOLO_detector import CustomYOLODetector
from MachineLearningModule.ObjectDetectors.robo_flow_detector import RoboFlowDetector
from MachineLearningModule.data_handler import DataHandler

from ImageHandling.panel_detector import PanelDetector


class TaskController:
    @staticmethod
    def panel_detection(method, camera_name, image_name=""):
        """
        Detects panels in an image using the specified method and saves the result to an image and the detected
        rectangles to a CSV file in ImageObjectDetectionResults.

        :param method: The method to use for panel detection ('image_process', 'roboflow', or 'yolo').
        :param camera_name: The name of the camera used to capture the image.
        :param image_name: The name of the image file to process (default is an empty string).
        """

        def save_rects(rectangles, filename='ImageObjectDetectionResults/detected_rects.csv'):
            # Define the header for the CSV file
            header = ['x', 'y', 'width', 'height']
            # Open the CSV file in write mode
            with open(filename, mode='w', newline='') as file:
                writer = csv.writer(file)
                # Write the header
                writer.writerow(header)
                # Write each rectangle to the CSV file
                for rect in rectangles:
                    writer.writerow(rect)

        valid_methods = ['image_process', 'roboflow', 'yolo']
        if method not in valid_methods:
            raise Exception(f"Please select a valid method: {valid_methods}")

        rects = []
        if method == 'image_process':
            panel_detector = PanelDetector()
            rects = panel_detector.get_panel_rects(camera_name, image_name)
        if method == 'roboflow':
            robo_flow_detector = RoboFlowDetector()
            rects = robo_flow_detector.get_panel_rects(camera_name, image_name)
        if method == 'yolo':
            custom_yolo_detector = CustomYOLODetector()
            rects = custom_yolo_detector.get_panel_rects(camera_name, image_name)
        save_rects(rects)

    @staticmethod
    def yield_prediction(model_num, saved_data_set_num, season="", visualize_test=False, visualize_training=False):
        """
        Calculates and shows yield prediction models' performance.

        :param model_num: The model number to use for predictions.
        :param saved_data_set_num: The saved dataset number to load.
        :param season: The season for which to perform predictions ('winter' or 'spring').
        :param visualize_test: Whether to visualize testing performance.
        :param visualize_training: Whether to visualize training performance.
        """
        # Functions for calculating and showing yield prediction models
        def testing_performance(visualize=True):
            temp = learning_model.verbose
            learning_model.verbose = 3
            # Test the model and show results
            data_handler.make_predictions_and_accuracies_for_test_sets(learning_model)
            total_percent_errors = []
            total_rmse_errors = []
            for prediction_tup, accuracies_tup in zip(data_handler.predictions, data_handler.accuracies):
                entry_bloc_pairs = [(prediction_tup[1], prediction_tup[2])]
                percent_e_acc = sum(accuracies_tup[0]) / len(accuracies_tup[0])
                total_percent_errors.append(percent_e_acc)
                print(f'Average percent error (testing data): {round(percent_e_acc, 2)}')
                goal_val = get_plot(prediction_tup[1], prediction_tup[2], plots).crop_yield
                rmse_error = calculate_rmse(goal_val, prediction_tup[0])
                total_rmse_errors.append(rmse_error)
                print(f'RMSE error (testing data): {round(rmse_error, 2)}')
                if visualize:
                    visualizer.visualize_plots(plots, entry_bloc_pairs, prediction_tup[0])
                print()
            print(f'Model average percent error (testing data): '
                  f'{round(sum(total_percent_errors) / len(total_percent_errors), 2)}')
            print(f'Model average RMSE (testing data): {round(sum(total_rmse_errors) / len(total_rmse_errors), 2)}')
            most_accurate_date = int(round(sum(data_handler.best_accuracies_dates) /
                                           len(data_handler.best_accuracies_dates), 0))
            print(
                f'Most accurate date (training data): {most_accurate_date} or {convert_int_to_str_date(most_accurate_date)}')
            print(f'Average accuracy (percent error) at best date (testing data): '
                  f'{round(sum(data_handler.accuracies_at_bests) / len(data_handler.accuracies_at_bests), 2)}')
            print()
            learning_model.verbose = temp

        def training_performance(visualize=True):
            temp = learning_model.verbose
            learning_model.verbose = 3
            # Check model's performance on training data and show results
            data_handler.make_predictions_and_accuracies_for_training_sets(learning_model)
            total_percent_errors = []
            total_rmse_errors = []
            for prediction_tup, accuracies_tup in zip(data_handler.predictions, data_handler.accuracies):
                entry_bloc_pairs = [(prediction_tup[1], prediction_tup[2])]
                percent_e_acc = sum(accuracies_tup[0]) / len(accuracies_tup[0])
                total_percent_errors.append(percent_e_acc)
                print(f'Average percent error (training data): {round(percent_e_acc, 2)}')
                goal_val = get_plot(prediction_tup[1], prediction_tup[2], plots).crop_yield
                rmse_error = calculate_rmse(goal_val, prediction_tup[0])
                total_rmse_errors.append(rmse_error)
                print(f'RMSE error (training data): {round(rmse_error, 2)}')
                if visualize:
                    visualizer.visualize_plots(plots, entry_bloc_pairs, prediction_tup[0])
                print()
            print(f'Model average percent error (training data): '
                  f'{round(sum(total_percent_errors) / len(total_percent_errors), 2)}')
            print(f'Model average RMSE (training data): {round(sum(total_rmse_errors) / len(total_rmse_errors), 2)}')
            most_accurate_date = int(round(sum(data_handler.best_accuracies_dates) /
                                           len(data_handler.best_accuracies_dates), 0))
            print(
                f'Most accurate date (training data): {most_accurate_date} or {convert_int_to_str_date(most_accurate_date)}')
            print(f'Average accuracy (percent error) at best date (training data): '
                  f'{round(sum(data_handler.accuracies_at_bests) / len(data_handler.accuracies_at_bests), 2)}')
            print()
            learning_model.verbose = temp

        # Plots:
        plots: list[Plot] = []

        # Parsing selections
        if season != 'winter' and season != 'spring':
            raise Exception("Please select a season: winter or spring")

        # Best winter: 14 on data 8 with honorable mention 6 on data 6, best spring: 1 on data 1
        # ML model selections
        # model_num = 14
        # saved_data_set_num = 8

        # Perform parsing based on selections
        parser = Parser()
        parser.parse_data(season, plots)
        data_handler = DataHandler(plots)

        # Perform normalizations
        normalize_all_of_attr(plots, "cigreen0")
        normalize_all_of_attr(plots, "cigreen")
        normalize_all_of_attr(plots, "evi2")
        normalize_all_of_attr(plots, "gndvi0")
        normalize_all_of_attr(plots, "gndvi")
        normalize_all_of_attr(plots, "ndvi")
        normalize_all_of_attr(plots, "rdvi")
        normalize_all_of_attr(plots, "savi")
        normalize_all_of_attr(plots, "sr")

        # Data preparation for machine learning
        # data_handler.make_sets(target_variates=["cigreen0", "cigreen", "evi2", "gndvi0", "gndvi", "ndvi", "rdvi",
        #                                         "savi", "sr"], training_percentage_amt=80, bulk_sets=True)
        # data_handler.make_sets(target_variates=["ndvi"], training_percentage_amt=80)
        # data_handler.save_sets(saved_data_set_num)
        data_handler.load_saved_sets(100, saved_data_set_num)

        # Create model
        # learning_model = StackedLSTM()
        learning_model = VanillaLSTM(num_epochs=100)

        # Train model
        learning_model.load_trained_model(model_num)
        # data_handler.train_on_training_sets(learning_model)
        # learning_model.save_trained_model(model_num)

        # Create visualizer
        visualizer = Visualizer()
        visualizer.show_heading_date = True
        visualizer.show_yield = True
        visualizer.show_prediction = True

        if visualize_training:
            training_performance(visualize=True)
        if visualize_test:
            testing_performance(visualize=True)

        # Visualize plot
        # visualizer.visualize_plots(plots, [(1, 1)])
        #
        # Variety plot visualization
        # visualizer.visualize_variety(plots, "Piranha CL+")
        #
        # Visualize all plots
        # visualizer.visualize_num_plots(plots, 35)
        #
        # Visualize correspondence with averaged values
        # visualizer.visualize_avg_correspondence(plots, "ndvi")
        #
        # Visualize correspondence with value at heading date
        # visualizer.visualize_heading_date_correlation(plots, "ndvi")

