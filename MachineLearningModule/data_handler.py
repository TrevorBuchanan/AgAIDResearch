import random
import numpy as np

from DataStructures.plot import Plot

from MachineLearningModule.LSTM.Univariate.univariateLSTM import UnivariateLSTM


# https://machinelearningmastery.com/how-to-develop-lstm-models-for-time-series-forecasting/
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
    return np.array(X), np.array(y)


def split_sequence_target_yield(sequence: list, n_steps: int, result_yield: float):
    # TODO: Fix description

    """
    Split the data into sets of length n_steps and have their target always be yield
    :param: sequence: list - Univariate list of numbers
    :param: n_steps: int - Length of sets that will be fed to the LSTM model
    result_yield (float): The target yield amount that the model is meant to predict towards
    :return
    """
    sets = []
    target_outputs = []
    for i, _ in enumerate(sequence):
        end_i_set = i + n_steps
        if end_i_set > len(sequence):
            break
        seq_set, seq_target_output = sequence[i:end_i_set], result_yield
        sets.append(seq_set)
        target_outputs.append(seq_target_output)
    return np.array(sets), np.array(target_outputs)


def prep_sequence_target_val(sequences: list[list], targets: list[float]) -> tuple[np.array, np.array]:
    # TODO: Add return description
    """
    Split the data into sets of length n_steps and have their target always be yield
    :param sequences: list[list] - List of univariate list of numbers
    :param targets: list[float] - List of target amounts that the model is meant to predict towards
    :return: (tuple[np.ndarray, np.ndarray]) -
    """

    def pad_list(lst, pad_left, pad_right, num):
        total_length = len(lst) + pad_left + pad_right
        padded_array = np.full(total_length, num, dtype=float)
        padded_array[pad_left:pad_left + len(lst)] = lst
        return padded_array.tolist()

    max_len = 0
    for seq in sequences:
        if len(seq) > max_len:
            max_len = len(seq)

    sets = []
    target_outputs = []
    for sequence, target in zip(sequences, targets):
        end_i_set = len(sequence)
        for i, _ in enumerate(sequence):
            seq_set, seq_target_output = sequence[0:end_i_set - i], target
            seq_set = pad_list(seq_set, 0, i, 0)
            if len(sequence) < max_len:
                ignore_padding_len = max_len - len(sequence)
                seq_set = pad_list(seq_set, 0, ignore_padding_len, -1)
            sets.append(seq_set)
            target_outputs.append(seq_target_output)
    return np.array(sets), np.array(target_outputs)


class DataHandler:
    def __init__(self, plots: list[Plot]) -> None:
        self.plots = plots
        self.uni_lstm_training_sets: list[(list, Plot)] = []
        self.uni_lstm_testing_sets: list[(list, Plot)] = []

    def make_uni_lstm_sets(self, target_variate: str):
        """
        Makes a set of univariate training and testing sets with given target variate and saves
        them to uni_lstm_training_sets and uni_lstm_testing_sets
        :param target_variate: str - The variate to target when creating the training sets
        """

        training_percentage_amt = 80
        total_amt = len(self.plots)
        unique_count = int(total_amt * (training_percentage_amt / 100))
        test_plot_indices = set()

        while len(test_plot_indices) < unique_count:
            index = random.randint(0, total_amt - 1)
            test_plot_indices.add(index)

        test_plot_indices = list(test_plot_indices)

        # Make training sets
        for i, plot in enumerate(self.plots):
            uni_var_set = self.get_uni_lstm_set(plot, target_variate)
            if len(uni_var_set) > 0:
                if i in test_plot_indices:  # Check if in 80 percent group of test plots
                    self.uni_lstm_training_sets.append((uni_var_set, plot))
                else:
                    self.uni_lstm_testing_sets.append((uni_var_set, plot))

    @staticmethod
    def get_uni_lstm_set(plot: Plot, target_variate: str) -> list:
        """
        Get a list of values of given plot, and target variate
        :param plot: Plot - Plot to get set from
        :param target_variate: str - The variate type to target in the plot
        :returns: list - list of target variate values
        """
        univariate_set = []
        for dp in plot.data_points:
            value = getattr(dp.vi_state, target_variate, None)
            if value is None:
                value = getattr(dp.conditions_state, target_variate, None)
            if value is not None:
                univariate_set.append(value)
        return univariate_set

    def train_uni_lstm_on_test_sets(self, model: UnivariateLSTM):
        # TODO: Function description
        """

        :param model:
        :return:
        """
        test_sets = []
        targets = []
        for test_set in self.uni_lstm_training_sets:
            test_sets.append(test_set[0])
            targets.append(test_set[1].crop_yield)

        model.train(test_sets, targets)

    def get_uni_lstm_predictions_for_set(self, model: UnivariateLSTM, test_set: list) -> list:
        # TODO: Function description
        """

        :param model:
        :param test_set:
        :return:
        """
        predictions = []
        tests_for_each_day = prep_sequence_target_val([test_set], [0 for _, _ in enumerate(test_set)])[0]
        for test_set in tests_for_each_day:
            predictions.append(model.predict(test_set)[0][0])
        return predictions
