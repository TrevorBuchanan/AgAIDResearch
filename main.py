# By: Trevor Buchanan


from DataStructures.plot import Plot

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
    vi_formula = "ndvi"

    # ML model selections
    model_num = 2
    target_variate = "vi_mean"

    # Perform parsing based on selections
    parser = Parser()
    parser.parse_data(season, plots, vi_formula)
    # data_handler = UniLSTMDataHandler(plots)

    # Data preparation for machine learning
    # data_handler.make_sets(target_variate)
    # data_handler.save_sets()
    # data_handler.load_saved_sets()

    # Create model
    # learning_model = StackedLSTM(num_epochs=300)
    # learning_model = VanillaLSTM(num_epochs=300)

    # Train model
    # learning_model.load_trained_model(season, vi_formula, target_variate, model_num)
    # data_handler.train_on_training_sets(learning_model)
    # learning_model.save_trained_model(season, vi_formula, target_variate, model_num)
    # exit(0)

    # Create visualizer
    visualizer = Visualizer()
    # Visualize selections
    # target_variety = "Glee"
    # Visual settings
    visualizer.line_mode = True
    # visualizer.point_mode = True
    # Data selection
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
    visualizer.show_yield = True
    visualizer.show_prediction = True

    # Individual plot visualization
    # Test the model
    # for testing_set in data_handler.testing_sets:
    #     predictions = data_handler.get_predictions_for_set(learning_model, testing_set[0])
    #     entry_bloc_pairs = [(testing_set[1], testing_set[2])]
    #     visualizer.visualize_plots(plots, entry_bloc_pairs, predictions)
    #
    # print("Already trained data: _____________________________________________________________________")
    # Test the model
    # for testing_set in data_handler.training_sets:
    #     predictions = data_handler.get_predictions_for_set(learning_model, testing_set[0])
    #     entry_bloc_pairs = [(testing_set[1], testing_set[2])]
    #     visualizer.visualize_plots(plots, entry_bloc_pairs, predictions)
    #     print("_____________________________________________________________________")

    # Variety plot visualization
    # visualizer.visualize_variety(plots, target_variety)

    # Visualize all plots
    # visualizer.visualize_num_plots(plots, 1)

    # Visualize correspondence
    visualizer.visualize_correspondence(plots)
