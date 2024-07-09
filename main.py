# By: Trevor Buchanan


from DataStructures.plot import Plot

from Helpers.utility import get_plot, normalize_all_of_attr, calculate_rmse, convert_int_to_str_date
from Helpers.visualizer import Visualizer
from Helpers.parser import Parser

from MachineLearningModule.LSTM.vanillaLSTM import VanillaLSTM
from MachineLearningModule.LSTM.stackedLSTM import StackedLSTM
from MachineLearningModule.data_handler import DataHandler







# multivariate lstm example
from numpy import array
from numpy import hstack
from keras.models import Sequential
from keras.layers import LSTM, Dense, Input
from tensorflow.keras.optimizers import Adam


# split a multivariate sequence into samples
def split_sequences(sequences, n_steps):
    X, y = list(), list()
    for i in range(len(sequences)):
        # find the end of this pattern
        end_ix = i + n_steps
        # check if we are beyond the dataset
        if end_ix > len(sequences):
            break
        # gather input and output parts of the pattern
        seq_x, seq_y = sequences[i:end_ix, :-1], sequences[end_ix - 1, -1]
        X.append(seq_x)
        y.append(seq_y)
    return array(X), array(y)


# define input sequence
in_seq1 = array([10, 20, 30, 40, 50, 60, 70, 80, 90])
in_seq2 = array([15, 25, 35, 45, 55, 65, 75, 85, 95])
out_seq = array([in_seq1[i] + in_seq2[i] for i in range(len(in_seq1))])
# convert to [rows, columns] structure
in_seq1 = in_seq1.reshape((len(in_seq1), 1))
in_seq2 = in_seq2.reshape((len(in_seq2), 1))
out_seq = out_seq.reshape((len(out_seq), 1))
# horizontally stack columns
dataset = hstack((in_seq1, in_seq2, out_seq))
# choose a number of time steps
n_steps = 3
# convert into input/output
X, y = split_sequences(dataset, n_steps)
# the dataset knows the number of features, e.g. 2
n_features = X.shape[2]
# define model
model = Sequential()
model.add(Input(shape=(n_steps, n_features)))
model.add(LSTM(50, activation='relu'))
model.add(Dense(1))
optimizer = Adam()
model.compile(optimizer=optimizer, loss='mse')
# fit model
model.fit(X, y, epochs=200, verbose=1)
# demonstrate prediction
x_input = array([[80, 85], [90, 95], [100, 105]])
x_input = x_input.reshape((1, n_steps, n_features))
yhat = model.predict(x_input, verbose=0)
print(yhat)














































#
#
#
#
# def testing_performance(visualize=True):
#     temp = learning_model.verbose
#     learning_model.verbose = 3
#     # Test the model and show results
#     data_handler.make_predictions_and_accuracies_for_test_sets(learning_model)
#     total_percent_errors = []
#     total_rmse_errors = []
#     for prediction_tup, accuracies_tup in zip(data_handler.predictions, data_handler.accuracies):
#         entry_bloc_pairs = [(prediction_tup[1], prediction_tup[2])]
#         percent_e_acc = sum(accuracies_tup[0]) / len(accuracies_tup[0])
#         total_percent_errors.append(percent_e_acc)
#         # print(f'Average percent error (testing data): {percent_e_acc}')
#         goal_val = get_plot(prediction_tup[1], prediction_tup[2], plots).crop_yield
#         rmse_error = calculate_rmse(goal_val, prediction_tup[0])
#         total_rmse_errors.append(rmse_error)
#         # print(f'RMSE error (testing data): {rmse_error}')
#         if visualize:
#             visualizer.visualize_plots(plots, entry_bloc_pairs, prediction_tup[0])
#         # print()
#     print(f'Model average percent error (testing data): {sum(total_percent_errors) / len(total_percent_errors)}')
#     print(f'Model average RMSE (testing data): {sum(total_rmse_errors) / len(total_rmse_errors)}')
#     most_accurate_date = int(round(sum(data_handler.best_accuracies_dates) /
#                                    len(data_handler.best_accuracies_dates), 0))
#     print(f'Most accurate date (training data): {most_accurate_date} or {convert_int_to_str_date(most_accurate_date)}')
#     print(f'Average accuracy (percent error) at best date (testing data): '
#           f'{sum(data_handler.accuracies_at_bests) / len(data_handler.accuracies_at_bests)}')
#     print()
#     learning_model.verbose = temp
#
#
# def training_performance(visualize=True):
#     temp = learning_model.verbose
#     learning_model.verbose = 3
#     # Check model's performance on training data and show results
#     data_handler.make_predictions_and_accuracies_for_training_sets(learning_model)
#     total_percent_errors = []
#     total_rmse_errors = []
#     for prediction_tup, accuracies_tup in zip(data_handler.predictions, data_handler.accuracies):
#         entry_bloc_pairs = [(prediction_tup[1], prediction_tup[2])]
#         percent_e_acc = sum(accuracies_tup[0]) / len(accuracies_tup[0])
#         total_percent_errors.append(percent_e_acc)
#         # print(f'Average percent error (training data): {percent_e_acc}')
#         goal_val = get_plot(prediction_tup[1], prediction_tup[2], plots).crop_yield
#         rmse_error = calculate_rmse(goal_val, prediction_tup[0])
#         total_rmse_errors.append(rmse_error)
#         # print(f'RMSE error (training data): {rmse_error}')
#         if visualize:
#             visualizer.visualize_plots(plots, entry_bloc_pairs, prediction_tup[0])
#         # print()
#     print(f'Model average percent error (training data): {sum(total_percent_errors) / len(total_percent_errors)}')
#     print(f'Model average RMSE (training data): {sum(total_rmse_errors) / len(total_rmse_errors)}')
#     most_accurate_date = int(round(sum(data_handler.best_accuracies_dates) /
#                                    len(data_handler.best_accuracies_dates), 0))
#     print(f'Most accurate date (training data): {most_accurate_date} or {convert_int_to_str_date(most_accurate_date)}')
#     print(f'Average accuracy (percent error) at best date (training data): '
#           f'{sum(data_handler.accuracies_at_bests) / len(data_handler.accuracies_at_bests)}')
#     print()
#     learning_model.verbose = temp
#
#
# if __name__ == '__main__':
#     print("AgAID Project\n")
#
#     # cigreen0, cigreen, evi2, gndvi0, gndvi, ndvi, rdvi, savi, sr
#
#     # Plots:
#     plots: list[Plot] = []
#
#     # Parsing selections
#     season = "spring"
#
#     # ML model selections
#     model_num = 13
#     saved_data_set_num = 7
#
#     # Perform parsing based on selections
#     parser = Parser()
#     parser.parse_data(season, plots)
#     data_handler = DataHandler(plots)
#
#     # Perform normalizations
#     normalize_all_of_attr(plots, "cigreen0")
#     normalize_all_of_attr(plots, "cigreen")
#     normalize_all_of_attr(plots, "evi2")
#     normalize_all_of_attr(plots, "gndvi0")
#     normalize_all_of_attr(plots, "gndvi")
#     normalize_all_of_attr(plots, "ndvi")
#     normalize_all_of_attr(plots, "rdvi")
#     normalize_all_of_attr(plots, "savi")
#     normalize_all_of_attr(plots, "sr")
#
#     # Data preparation for machine learning
#     # data_handler.make_sets(target_variates=["cigreen0", "cigreen", "evi2", "gndvi0", "gndvi", "ndvi", "rdvi",
#     #                                         "savi", "sr"], training_percentage_amt=80)
#     data_handler.make_sets(target_variates=["ndvi"], training_percentage_amt=80)
#     data_handler.save_sets(saved_data_set_num)
#     # data_handler.load_saved_sets(100, saved_data_set_num)
#
#     # Create model
#     # learning_model = StackedLSTM()
#     learning_model = VanillaLSTM()
#
#     # Train model
#     # learning_model.load_trained_model(model_num)
#     data_handler.train_on_training_sets(learning_model)
#     learning_model.save_trained_model(model_num)
#
#     # Create visualizer
#     visualizer = Visualizer()
#     visualizer.line_mode = True
#     visualizer.show_heading_date = True
#     visualizer.show_yield = True
#     visualizer.show_prediction = True
#     visualizer.show_ndvi = True
#
#     training_performance(visualize=False)
#     testing_performance(visualize=False)
#
#     # Visualize plot
#     # visualizer.visualize_plots(plots, [(1, 1)])
#
#     # Variety plot visualization
#     # visualizer.visualize_variety(plots, "Jameson")
#
#     # Visualize all plots
#     # visualizer.visualize_num_plots(plots, 35)
#
#     # Visualize correspondence with averaged values
#     # visualizer.visualize_avg_correspondence(plots, "ndvi")
#
#     # Visualize correspondence with value at heading date
#     # visualizer.visualize_heading_date_correlation(plots, "ndvi")
