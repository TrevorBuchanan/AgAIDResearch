# By: Trevor Buchanan


from DataStructures.plot import Plot
from Helpers.utility import get_plot, normalize_all_of_attr, calculate_rmse, convert_int_to_str_date

from Helpers.visualizer import Visualizer
from Helpers.parser import Parser

from MachineLearningModule.LSTM.Univariate.uni_lstm_data_handler import UniLSTMDataHandler
from MachineLearningModule.LSTM.Univariate.vanillaLSTM import VanillaLSTM
from MachineLearningModule.LSTM.Univariate.stackedLSTM import StackedLSTM


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
        # print(f'Average percent error (testing data): {percent_e_acc}')
        goal_val = get_plot(prediction_tup[1], prediction_tup[2], plots).crop_yield
        rmse_error = calculate_rmse(goal_val, prediction_tup[0])
        total_rmse_errors.append(rmse_error)
        # print(f'RMSE error (testing data): {rmse_error}')
        if visualize:
            visualizer.visualize_plots(plots, entry_bloc_pairs, prediction_tup[0])
        # print()
    print(f'Model average percent error (testing data): {sum(total_percent_errors) / len(total_percent_errors)}')
    print(f'Model average RMSE (testing data): {sum(total_rmse_errors) / len(total_rmse_errors)}')
    most_accurate_date = int(round(sum(data_handler.best_accuracies_dates) /
                                   len(data_handler.best_accuracies_dates), 0))
    print(f'Most accurate date (training data): {most_accurate_date} or {convert_int_to_str_date(most_accurate_date)}')
    print(f'Average accuracy (percent error) at best date (testing data): '
          f'{sum(data_handler.accuracies_at_bests) / len(data_handler.accuracies_at_bests)}')
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
        # print(f'Average percent error (training data): {percent_e_acc}')
        goal_val = get_plot(prediction_tup[1], prediction_tup[2], plots).crop_yield
        rmse_error = calculate_rmse(goal_val, prediction_tup[0])
        total_rmse_errors.append(rmse_error)
        # print(f'RMSE error (training data): {rmse_error}')
        if visualize:
            visualizer.visualize_plots(plots, entry_bloc_pairs, prediction_tup[0])
        # print()
    print(f'Model average percent error (training data): {sum(total_percent_errors) / len(total_percent_errors)}')
    print(f'Model average RMSE (training data): {sum(total_rmse_errors) / len(total_rmse_errors)}')
    most_accurate_date = int(round(sum(data_handler.best_accuracies_dates) /
                                   len(data_handler.best_accuracies_dates), 0))
    print(f'Most accurate date (training data): {most_accurate_date} or {convert_int_to_str_date(most_accurate_date)}')
    print(f'Average accuracy (percent error) at best date (training data): '
          f'{sum(data_handler.accuracies_at_bests) / len(data_handler.accuracies_at_bests)}')
    print()
    learning_model.verbose = temp


if __name__ == '__main__':
    print("AgAID Project\n")

    # cigreen0, cigreen, evi2, gndvi0, gndvi, ndvi, rdvi, savi, sr

    # Plots:
    plots: list[Plot] = []

    # Parsing selections
    season = "winter"

    # ML model selections
    model_num = 6
    saved_data_set_num = 6

    # Perform parsing based on selections
    parser = Parser()
    parser.parse_data(season, plots)
    data_handler = UniLSTMDataHandler(plots)

    # Perform normalizations
    normalize_all_of_attr(plots, "ndvi")

    # Data preparation for machine learning
    # data_handler.make_sets(target_variate="ndvi", training_percentage_amt=80, bulk_sets=True)
    # data_handler.save_sets(saved_data_set_num)
    data_handler.load_saved_sets(100, saved_data_set_num)

    # Create model
    # learning_model = StackedLSTM(model_num, num_epochs=300)
    learning_model = VanillaLSTM(model_num, num_epochs=300)

    # Train model
    learning_model.load_trained_model(model_num)
    # data_handler.train_on_training_sets(learning_model)
    # learning_model.save_trained_model(model_num)

    # Create visualizer
    visualizer = Visualizer()
    visualizer.line_mode = True
    visualizer.show_heading_date = True
    visualizer.show_yield = True
    visualizer.show_prediction = True
    visualizer.show_ndvi = True

    training_performance(visualize=True)
    testing_performance(visualize=True)



    # Glee
    # Kelse
    # Alum
    # Chet
    # Louise
    # Ryan
    # Seahawk
    # Whit
    # Dayn
    # Tekoa
    # Net CL+
    # Jedd

    # Rosalyn
    # Otto
    # Puma
    # Purl
    # Jasper
    # Inspire
    # Piranha CL+
    # Jameson


    # Visualize plot
    # visualizer.visualize_plots(plots, [(1, 1)])

    # Variety plot visualization
    # visualizer.visualize_variety(plots, "Jameson")

    # Visualize all plots
    # visualizer.visualize_num_plots(plots, 35)

    # Visualize correspondence with averaged values
    # visualizer.visualize_avg_correspondence(plots, "ndvi")

    # Visualize correspondence with value at heading date
    # visualizer.visualize_heading_date_correlation(plots, "ndvi")
