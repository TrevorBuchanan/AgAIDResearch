
from DataStructures.plot import Plot

from Helpers.utility import get_plot, normalize_all_of_attr, calculate_rmse, convert_int_to_str_date
from Helpers.visualizer import Visualizer
from Helpers.parser import Parser

from MachineLearningModule.LSTM.vanillaLSTM import VanillaLSTM
from MachineLearningModule.LSTM.stackedLSTM import StackedLSTM
from MachineLearningModule.data_handler import DataHandler

from Helpers.utility import sort_list_by_datetime
from ImageHandling.image_loader import ImageLoader
from ImageHandling.image_processor import ImageProcessor
from ImageHandling.image_displayer import ImageDisplayer
from tqdm import tqdm

from ImageHandling.panel_detector import PanelDetector


class TaskController:
    @staticmethod
    def run_image_panel_detection_code(self):
        image_loader = ImageLoader()
        image_processor = ImageProcessor()
        image_displayer = ImageDisplayer()

        # Image loading
        camera_name = 'cam4'
        # Get image
        # image_name = 'date_29-4-2024_10.0.10_1'
        # image = image_loader.load_image(camera_name, image_name)
        # images = [image]
        # image_names = [image_name]

        # Get images
        images, image_names = image_loader.load_all_images(camera_name)

        # Sort images
        nir_images, rgb_images, full_images = {}, {}, {}
        for name, image in zip(image_names, images):
            nir_image, rgb_image = image_processor.vertical_image_split(image)
            nir_images[name] = nir_image
            rgb_images[name] = rgb_image
            full_images[name] = image
        sorted_names = sort_list_by_datetime(nir_images)

        # Find reference panel
        temp_max_amt = 20
        temp_using_img_names = sorted_names[15:temp_max_amt]
        panel_detector = PanelDetector()
        for i, image_name in enumerate(tqdm(temp_using_img_names, desc="Detecting Panel in Images")):
            nir_rects = panel_detector.get_panel_rect(nir_images[image_name])
            rgb_rects = panel_detector.get_panel_rect(rgb_images[image_name])
            image_processor.draw_rects_to_image(nir_images[image_name], nir_rects)
            image_processor.draw_rects_to_image(rgb_images[image_name], rgb_rects)

        # Display image
        for image_name in temp_using_img_names:
            image_displayer.plot_images([full_images[image_name]], labels=[image_name])

    @staticmethod
    def run_yield_prediction_code(self):
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
        # Yield prediction using time series VI (Vegetation indices)
        # cigreen0, cigreen, evi2, gndvi0, gndvi, ndvi, rdvi, savi, sr

        # Plots:
        plots: list[Plot] = []

        # Parsing selections
        season = "winter"

        # Best winter: 14 on data 8 with honorable mention 6 on data 6, best spring: 1 on data 1
        # ML model selections
        model_num = 14
        saved_data_set_num = 8

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
        visualizer.show_ndvi = True

        # training_performance(visualize=True)
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

