# By: Trevor Buchanan


from DataStructures.plot import Plot
from Helpers.utility import get_plot, normalize_all_of_attr, calculate_rmse

from Helpers.visualizer import Visualizer
from Helpers.parser import Parser

from MachineLearningModule.LSTM.Univariate.uni_lstm_data_handler import UniLSTMDataHandler
from MachineLearningModule.LSTM.Univariate.vanillaLSTM import VanillaLSTM
from MachineLearningModule.LSTM.Univariate.stackedLSTM import StackedLSTM


if __name__ == '__main__':
    print("AgAID Project\n")

    # cigreen0, cigreen, evi2, gndvi0, gndvi, ndvi, rdvi, savi, sr

    # Plots:
    plots: list[Plot] = []

    # Parsing selections
    season = "spring"

    # ML model selections
    model_num = 1
    saved_data_set_num = 1
    target_variate = "ndvi"

    # Perform parsing based on selections
    parser = Parser()
    parser.parse_data(season, plots)
    data_handler = UniLSTMDataHandler(plots)

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
    # data_handler.make_sets(target_variate, 80)
    # data_handler.save_sets(model_num)
    data_handler.load_saved_sets(30, model_num)
    # exit(0)

    # Create model
    # learning_model = StackedLSTM(model_num, num_epochs=300)
    learning_model = VanillaLSTM(model_num, num_epochs=300)

    # Train model
    learning_model.load_trained_model(model_num)
    # data_handler.train_on_training_sets(learning_model)
    # learning_model.save_trained_model(model_num)
    # exit(0)

    # Create visualizer
    visualizer = Visualizer()
    visualizer.line_mode = True
    visualizer.show_cigreen0 = True
    visualizer.show_cigreen = True
    visualizer.show_evi2 = True
    visualizer.show_gndvi0 = True
    visualizer.show_gndvi = True
    visualizer.show_ndvi = True
    visualizer.show_rdvi = True
    visualizer.show_savi = True
    visualizer.show_sr = True
    visualizer.show_heading_date = True
    # visualizer.show_yield = True
    # visualizer.show_prediction = True

    # Test the model and show results
    data_handler.make_predictions_and_accuracies_for_test_sets(learning_model)
    total_percent_errors = []
    total_rmse_errors = []
    for prediction_tup, accuracies_tup in zip(data_handler.predictions, data_handler.accuracies):
        entry_bloc_pairs = [(prediction_tup[1], prediction_tup[2])]
        percent_e_acc = sum(accuracies_tup[0]) / len(accuracies_tup[0])
        total_percent_errors.append(percent_e_acc)
        print(f'Average percent error (testing data): {percent_e_acc}')
        goal_val = get_plot(prediction_tup[1], prediction_tup[2], plots).crop_yield
        rmse_error = calculate_rmse(goal_val, prediction_tup[0])
        total_rmse_errors.append(rmse_error)
        print(f'RMSE error (testing data): {rmse_error}')
        # visualizer.visualize_plots(plots, entry_bloc_pairs, prediction_tup[0])
        print()
    print(f'Model average percent error (testing data): {sum(total_percent_errors) / len(total_percent_errors)}')
    print(f'Model average RMSE (testing data): {sum(total_rmse_errors) / len(total_rmse_errors)}')

    # data_handler.continue_training_on_weak_sets(learning_model, 2)

    # # Check model's performance on training data and show results
    # data_handler.make_predictions_and_accuracies_for_training_sets(learning_model)
    # total_percent_errors = []
    # total_r_squared_errors = []
    # total_rmse_errors = []
    # for prediction_tup, accuracies_tup in zip(data_handler.predictions, data_handler.accuracies):
    #     entry_bloc_pairs = [(prediction_tup[1], prediction_tup[2])]
    #     percent_e_acc = sum(accuracies_tup[0]) / len(accuracies_tup[0])
    #     total_percent_errors.append(percent_e_acc)
    #     print(f'Average percent error (training data): {percent_e_acc}')
    #     visualizer.visualize_plots(plots, entry_bloc_pairs, prediction_tup[0])
    #     print()
    # print(f'Model average percent error (training data): {sum(total_percent_errors) / len(total_percent_errors)}')

    # Visualize plot
    # visualizer.visualize_plots(plots, [(1, 1)])

    # Variety plot visualization
    # visualizer.visualize_variety(plots, "Glee")

    # Visualize all plots
    # visualizer.visualize_num_plots(plots, 35)

    # Visualize correspondence with averaged VI's
    # visualizer.visualize_avg_vi_correspondence(plots)

    # Visualize correspondence with VI at heading date
    # visualizer.visualize_heading_date_correlation(plots)
