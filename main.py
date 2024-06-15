# By: Trevor Buchanan


from DataStructures.plot import Plot
from Helpers.utility import get_plot

from Helpers.visualizer import Visualizer
from Helpers.parser import Parser

from MachineLearningModule.data_handler import DataHandler
from MachineLearningModule.LSTM.Univariate.univariateLSTM import UnivariateLSTM
from MachineLearningModule.LSTM.Univariate.vanillaLSTM import VanillaLSTM


if __name__ == '__main__':
    print("AgAID Project\n")

    # cigreen0, cigreen, evi2, gndvi0, gndvi, ndvi, rdvi, savi, sr
    # Plots:
    winter_plots: list[Plot] = []
    spring_plots: list[Plot] = []

    # Parsing selections
    season = "spring"
    vi_formula = "ndvi"
    target_variety = "Seahawk"
    target_variate = "vi_mean"
    variety_block_pair = (1, 1)

    # Perform parsing based on selections
    parser = Parser()
    if season == "spring":
        parser.parse_spring_data(spring_plots, vi_formula)
        data_handler = DataHandler(spring_plots)
    else:
        parser.parse_winter_data(winter_plots, vi_formula)
        data_handler = DataHandler(winter_plots)

    # Data preparation for machine learning
    data_handler.make_uni_lstm_training_sets(target_variate)

    # Create model
    uni_lstm_learning_model = VanillaLSTM(num_epochs=100)
    uni_lstm_learning_model.load_trained_model()

    # Train model
    # data_handler.uni_lstm_training_on_test_sets(uni_lstm_learning_model)
    # uni_lstm_learning_model.save_trained_model()

    # Test the model
    untested_tup = data_handler.get_uni_lstm_untested_sets()[0]
    predictions = data_handler.get_uni_lstm_predictions_for_set(uni_lstm_learning_model, untested_tup[0])

    # Create visualizer
    visualizer = Visualizer()
    # Visual settings
    visualizer.line_mode = True
    visualizer.point_mode = True
    # Data selection
    # visualizer.show_missing_dates = True
    # visualizer.show_vi_mean = True
    # visualizer.show_air_temp = True
    # visualizer.show_dew_point = True
    # visualizer.show_relative_humidity = True
    # visualizer.show_soil_temp_2in = True
    # visualizer.show_soil_temp_8in = True
    # visualizer.show_precipitation = True
    # visualizer.show_solar_radiation = True
    # Result data selection
    # visualizer.show_heading_date = True
    # visualizer.show_plant_height = True
    # visualizer.show_test_pounds_per_bushel = True
    visualizer.show_yield = True
    visualizer.show_prediction = True

    # Individual plot visualization
    # Entry, Block (1-3)
    # entry_bloc_pairs = [(7, 1)]
    entry_bloc_pairs = [(untested_tup[1].variety_index, untested_tup[1].replication_variety)]
    if season == "spring":
        visualizer.visualize_plots(spring_plots, entry_bloc_pairs, predictions)
    elif season == "winter":
        visualizer.visualize_plots(winter_plots, entry_bloc_pairs, predictions)

    # Variety plot visualization
    # if season == "spring":
    #     visualizer.visualize_variety(spring_plots, target_variety)
    # elif season == "winter":
    #     visualizer.visualize_variety(winter_plots, target_variety)
