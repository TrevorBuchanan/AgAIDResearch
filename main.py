# By: Trevor Buchanan

# univariate lstm example
from numpy import array, zeros
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Input

# split a univariate sequence into samples
def split_sequence(sequence, n_steps):
    X, y = list(), list()
    for i in range(len(sequence)):
        # find the end of this pattern
        end_ix = i + n_steps
        # check if we are beyond the sequence
        if end_ix > len(sequence) - 1:
            break
        # gather input and output parts of the pattern
        seq_x, seq_y = sequence[i:end_ix], sequence[end_ix]
        X.append(seq_x)
        y.append(seq_y)
    return array(X), array(y)

def test_split_sequence(sequence, n_steps):
    def pad_list(lst, pad_left, pad_right):
        total_length = len(lst) + pad_left + pad_right
        padded_array = zeros(total_length, dtype=int)
        padded_array[pad_left:pad_left+len(lst)] = lst
        return padded_array

    X, y = list(), list()
    for i in range(len(sequence)):
        # find the end of this pattern
        end_ix = i + n_steps
        # check if we are beyond the sequence
        if end_ix > len(sequence):
            break
        # gather input and output parts of the pattern
        seq_x, seq_y = sequence[i:end_ix], 250
        seq_x = pad_list(seq_x, i, len(sequence) - n_steps - i)
        X.append(seq_x)
        y.append(seq_y)
    return array(X), array(y)

def test2_split_sequence(sequence):
    def pad_list(lst, pad_left, pad_right):
        total_length = len(lst) + pad_left + pad_right
        padded_array = zeros(total_length, dtype=int)
        padded_array[pad_left:pad_left+len(lst)] = lst
        return padded_array

    X, y = list(), list()
    end_ix = len(sequence)
    for i in range(len(sequence)):
        # check if we are beyond the sequence
        if end_ix > len(sequence):
            break
        # gather input and output parts of the pattern
        seq_x, seq_y = sequence[0:end_ix - i], 555
        seq_x = pad_list(seq_x, 0, i)
        X.append(seq_x)
        y.append(seq_y)
    return array(X), array(y)

# define input sequence
raw_seq = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 120, 130]
# raw_seq = [10, 20, 30, 40, 50, 60, 70, 80, 90]
# choose a number of time steps
n_steps = 3
# split into samples
# X, y = test_split_sequence(raw_seq, n_steps)
X, y = test2_split_sequence(raw_seq)
# reshape from [samples, timesteps] into [samples, timesteps, features]
n_features = 1
X = X.reshape((X.shape[0], X.shape[1], n_features))

# define model
model = Sequential()
model.add(Input(shape=((len(raw_seq)), n_features)))
model.add(LSTM(50, activation='relu')) # 50 Units (neurons)
model.add(Dense(1))
model.compile(optimizer='adam', loss='mse')
# fit model
model.fit(X, y, epochs=500, verbose=1)
# demonstrate prediction
x_input = array([10, 20, 30, 40, 50, 60, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
x_input = x_input.reshape((1, (len(x_input)), n_features))
yhat = model.predict(x_input, verbose=1)
print(yhat)


# from DataStructures.plot import Plot

# from Helpers.visualizer import Visualizer
# from Helpers.parser import Parser

# from MachineLearningModule.data_prepper import DataPrepper
# from MachineLearningModule.LSTM.Univariate.univariateLSTM import UnivariateLSTM
# from MachineLearningModule.LSTM.Univariate.vanillaLSTM import VanillaLSTM

# # cigreen0, cigreen, evi2, gndvi0, gndvi, ndvi, rdvi, savi, sr
# winter_plots: list[Plot] = []
# spring_plots: list[Plot] = []

# # Create visualizer
# visualizer = Visualizer()

# if __name__ == '__main__':
#     print("AgAID Project\n")

#     # Parsing selections
#     season = "spring"
#     vi_formula = "ndvi"
#     target_variety = "Seahawk"
#     target_variate = "vi_mean"
#     variety_block_pair = (1, 1)

#     # Perform parsing based on selections
#     parser = Parser()
#     data_prepper: DataPrepper
#     if season == "spring":
#         parser.parse_spring_data(spring_plots, vi_formula)
#         data_prepper = DataPrepper(spring_plots)
#     elif season == "winter":
#         parser.parse_winter_data(winter_plots, vi_formula)
#         data_prepper = DataPrepper(spring_plots)

#     # Machine learning model training
#     sequence = data_prepper.get_univariate_set(variety_block_pair[0], variety_block_pair[1], target_variate)
#     print(sequence)
#     print(min(sequence))
#     print(max(sequence))
#     print(len(sequence))
#     sets, target_outs = data_prepper.split_sequence_target_yield(sequence, 3, 50)
#     univariate_learning_model: UnivariateLSTM = VanillaLSTM()
#     print(type(univariate_learning_model))
#     univariate_learning_model.train(sets, target_outs)
#     series = []
#     univariate_learning_model.predict(series)


























    ## Visual settings
    # visualizer.line_mode = True
    # visualizer.point_mode = True
    ## Data selection
    # visualizer.show_missing_dates = True
    # visualizer.show_vi_mean = True
    # visualizer.show_air_temp = True
    # visualizer.show_dew_point = True
    # visualizer.show_relative_humidity = True
    # visualizer.show_soil_temp_2in = True
    # visualizer.show_soil_temp_8in = True
    # visualizer.show_precipitation = True
    # visualizer.show_solar_radiation = True
    ## Result data selection
    # visualizer.show_heading_date = True
    # visualizer.show_plant_height = True
    # visualizer.show_test_pounds_per_bushel = True
    # visualizer.show_yield = True

    # Individual plot visualization
    # Entry, Block (1-3)
    # entry_bloc_pairs = [(7, 1)]
    # if season == "spring":
    #     visualizer.visualize_plots(spring_plots, entry_bloc_pairs)
    # elif season == "winter":
    #     visualizer.visualize_plots(winter_plots, entry_bloc_pairs)

    # Variety plot visualization
    # if season == "spring":
    #     visualizer.visualize_variety(spring_plots, target_variety)
    # elif season == "winter":
    #     visualizer.visualize_variety(winter_plots, target_variety)
