# By: Trevor Buchanan


from DataStructures.plot import Plot

from Helpers.visualizer import Visualizer
from Helpers.parser import Parser

from MachineLearningModule.data_handler import DataHandler
from MachineLearningModule.LSTM.Univariate.vanillaLSTM import VanillaLSTM
from MachineLearningModule.LSTM.Univariate.stackedLSTM import StackedLSTM

# Temp
# import matplotlib.pyplot as plt
#
#
# def f(x):
#     return (-1 / 100) * pow(x, 2) + (1 / 2) * x + 60
#
#
# def make_pattern():
#     vals = []
#     for x in range(80):
#         if x > 50:
#             vals.append(0)
#             continue
#         vals.append(f(x))
#
#     print(vals)
#     return vals
#
#
# func = make_pattern()
#
# plt.plot(func, label='Function')
# plt.title("Test")
# plt.xlabel('X')
# plt.ylabel('Y')
# plt.grid(True)
# plt.tight_layout()
# plt.show()

# exit(0)






# Tests _____________________________________________________________________________________________
# ex_seq1 = [30.0, 30.49, 30.96, 31.41, 31.84, 32.25, 32.64, 33.01, 33.36, 33.69, 34.0, 34.29, 34.56, 34.81, 35.04,
#            35.25, 35.44, 35.61, 35.76, 35.89, 36.0, 36.09, 36.16, 36.21, 36.24, 36.25, 36.24, 36.21, 36.16, 36.09,
#            36.0, 35.89, 35.76, 35.61, 35.44, 35.25, 35.04, 34.81, 34.56, 34.29, 34.0, 33.69, 33.36, 33.01, 32.64,
#            32.25, 31.84, 31.41, 30.96, 30.49, 30.0, 29.49, 28.96, 28.41, 27.84, 27.25, 26.64, 26.009999999999998,
#            25.36, 24.689999999999998, 24.0, 23.29, 22.560000000000002, 21.810000000000002, 21.04, 20.25,
#            19.439999999999998, 18.61, 17.759999999999998, 16.89, 16.0, 15.089999999999996, 14.159999999999997, 13.21,
#            12.240000000000002, 11.25, 10.240000000000002, 9.21, 8.159999999999997, 7.089999999999996]
# goal1 = 57.089999999999996
# ex_seq2 = [40.0, 40.49, 40.96, 41.41, 41.84, 42.25, 42.64, 43.01, 43.36, 43.69, 44.0, 44.29, 44.56, 44.81,
#            45.04, 45.25, 45.44, 45.61, 45.76, 45.89, 46.0, 46.09, 46.16, 46.21, 46.24, 46.25, 46.24, 46.21,
#            46.16, 46.09, 46.0, 45.89, 45.76, 45.61, 45.44, 45.25, 45.04, 44.81, 44.56, 44.29, 44.0, 43.69,
#            43.36, 43.01, 42.64, 42.25, 41.84, 41.41, 40.96, 40.489999999999995, 40.0, 39.489999999999995,
#            38.96, 38.41, 37.84, 37.25, 36.64, 36.01, 35.36, 34.69, 34.0, 33.29, 32.56, 31.810000000000002,
#            31.04, 30.25, 29.439999999999998, 28.61, 27.759999999999998, 26.89, 26.0, 25.089999999999996,
#            24.159999999999997, 23.21, 22.240000000000002, 21.25, 20.240000000000002, 19.21, 18.159999999999997,
#            17.089999999999996]
# goal2 = 67.089999999999996
# ex_seq3 = [50.0, 50.49, 50.96, 51.41, 51.84, 52.25, 52.64, 53.01, 53.36, 53.69, 54.0, 54.29, 54.56, 54.81,
#            55.04, 55.25, 55.44, 55.61, 55.76, 55.89, 56.0, 56.09, 56.16, 56.21, 56.24, 56.25, 56.24, 56.21,
#            56.16, 56.09, 56.0, 55.89, 55.76, 55.61, 55.44, 55.25, 55.04, 54.81, 54.56, 54.29, 54.0, 53.69,
#            53.36, 53.01, 52.64, 52.25, 51.84, 51.41, 50.96, 50.489999999999995, 50.0, 49.489999999999995,
#            48.96, 48.41, 47.84, 47.25, 46.64, 46.01, 45.36, 44.69, 44.0, 43.29, 42.56, 41.81, 41.04, 40.25,
#            39.44, 38.61, 37.76, 36.89, 36.0, 35.089999999999996, 34.16, 33.21, 32.24, 31.25, 30.240000000000002,
#            29.21, 28.159999999999997, 27.089999999999996]
# goal3 = 77.089999999999996
# ex_seq4 = [60.0, 60.49, 60.96, 61.41, 61.84, 62.25, 62.64, 63.01, 63.36, 63.69, 64.0, 64.29, 64.56, 64.81,
#            65.04, 65.25, 65.44, 65.61, 65.76, 65.89, 66.0, 66.09, 66.16, 66.21, 66.24, 66.25, 66.24, 66.21,
#            66.16, 66.09, 66.0, 65.89, 65.76, 65.61, 65.44, 65.25, 65.03999999999999, 64.81, 64.56,
#            64.28999999999999, 64.0, 63.69, 63.36, 63.01, 62.64, 62.25, 61.84, 61.41, 60.96, 60.489999999999995,
#            60.0, 59.489999999999995, 58.96, 58.41, 57.84, 57.25, 56.64, 56.01, 55.36, 54.69, 54.0, 53.29, 52.56,
#            51.81, 51.04, 50.25, 49.44, 48.61, 47.76, 46.89, 46.0, 45.089999999999996, 44.16, 43.21, 42.24,
#            41.25, 40.24, 39.21, 38.16, 37.089999999999996]
# goal4 = 87.089999999999996
# ex_seq5 = [60.0, 60.49, 60.96, 61.41, 61.84, 62.25, 62.64, 63.01, 63.36, 63.69, 64.0, 64.29, 64.56, 64.81, 65.04, 65.25,
#            65.44, 65.61, 65.76, 65.89, 66.0, 66.09, 66.16, 66.21, 66.24, 66.25, 66.24, 66.21, 66.16, 66.09, 66.0, 65.89,
#            65.76, 65.61, 65.44, 65.25, 65.03999999999999, 64.81, 64.56, 64.28999999999999, 64.0, 63.69, 63.36, 63.01,
#            62.64, 62.25, 61.84, 61.41, 60.96, 60.489999999999995, 60.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
#            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # Goal 87.089999999999996
#
# test_lstm = VanillaLSTM(num_epochs=1000)
#
# def normalize(lst):
#     max_elm = max(lst)
#     temp = list(map(lambda elm: elm / max_elm, lst))
#     # print(temp)
#     return temp
#
# sequences = [ex_seq1, ex_seq2, ex_seq3]
# goals = [goal1, goal2, goal3]
#
# test_lstm.load_trained_model(season="test")
# test_lstm.train(sequences, goals)
# test_lstm.save_trained_model(season="test")
# print(f'Goal1: {goal1}')
# print(f'Goal2: {goal2}')
# print(f'Goal3: {goal3}')
# print(f'Goal4: {goal4}')
# print(f'Prediction 1: {test_lstm.predict((ex_seq1))}')
# print(f'Prediction 2: {test_lstm.predict((ex_seq2))}')
# print(f'Prediction 3: {test_lstm.predict((ex_seq3))}')
# print(f'Prediction 4: {test_lstm.predict((ex_seq4))}')
# print(f'Prediction 5: {test_lstm.predict((ex_seq5))}')
# Tests _____________________________________________________________________________________________



if __name__ == '__main__':
    print("AgAID Project\n")

    # cigreen0, cigreen, evi2, gndvi0, gndvi, ndvi, rdvi, savi, sr
    # Plots:
    winter_plots: list[Plot] = []
    spring_plots: list[Plot] = []

    # Parsing selections
    season = "spring"
    vi_formula = "ndvi"
    # target_variety = "Seahawk"
    target_variate = "vi_mean"
    # target_variate = "air_temp"
    # Perform parsing based on selections
    parser = Parser()
    if season == "spring":
        parser.parse_spring_data(spring_plots, vi_formula)
        data_handler = DataHandler(spring_plots)
    else:
        parser.parse_winter_data(winter_plots, vi_formula)
        data_handler = DataHandler(winter_plots)

    # Data preparation for machine learning
    data_handler.make_uni_lstm_sets(target_variate)

    # Create model
    # uni_lstm_learning_model = StackedLSTM(num_epochs=200)
    uni_lstm_learning_model = VanillaLSTM(num_epochs=500)
    # uni_lstm_learning_model.load_trained_model(season)

    # Train model
    uni_lstm_learning_model.load_trained_model(season, vi_formula, target_variate)
    # data_handler.train_uni_lstm_on_test_sets(uni_lstm_learning_model)
    # uni_lstm_learning_model.save_trained_model(season, vi_formula, target_variate)

    # exit(0)

















    # Create visualizer
    visualizer = Visualizer()
    # Visual settings
    visualizer.line_mode = True
    visualizer.point_mode = True
    # Data selection
    # visualizer.show_missing_dates = True
    visualizer.show_vi_mean = True
    # visualizer.show_air_temp = True
    # visualizer.show_dew_point = True
    # visualizer.show_relative_humidity = True
    # visualizer.show_soil_temp_2in = True
    # visualizer.show_soil_temp_8in = True
    # visualizer.show_precipitation = True
    # visualizer.show_solar_radiation = True
    # Result data selection
    visualizer.show_heading_date = True
    # visualizer.show_plant_height = True
    # visualizer.show_test_pounds_per_bushel = True
    # visualizer.show_yield = True
    # visualizer.show_prediction = True

    # Individual plot visualization
    # Entry, Block (1-3)
    # entry_bloc_pairs = [(7, 1)]
    # Test the model
    for testing_set in data_handler.uni_lstm_testing_sets:
        predictions = data_handler.get_uni_lstm_predictions_for_set(uni_lstm_learning_model, testing_set[0])
        entry_bloc_pairs = [(testing_set[1].variety_index, testing_set[1].replication_variety)]
        if season == "spring":
            visualizer.visualize_plots(spring_plots, entry_bloc_pairs, predictions)
        elif season == "winter":
            visualizer.visualize_plots(winter_plots, entry_bloc_pairs, predictions)


    print("Already trained data: _____________________________________________________________________")
    # Test the model
    for testing_set in data_handler.uni_lstm_training_sets:
        predictions = data_handler.get_uni_lstm_predictions_for_set(uni_lstm_learning_model, testing_set[0])
        entry_bloc_pairs = [(testing_set[1].variety_index, testing_set[1].replication_variety)]
        if season == "spring":
            visualizer.visualize_plots(spring_plots, entry_bloc_pairs, predictions)
        elif season == "winter":
            visualizer.visualize_plots(winter_plots, entry_bloc_pairs, predictions)

    # Variety plot visualization
    # if season == "spring":
    #     visualizer.visualize_variety(spring_plots, target_variety)
    # elif season == "winter":
    #     visualizer.visualize_variety(winter_plots, target_variety)
