import random

from DataStructures.plot import Plot
from numpy import array, zeros

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
    return array(X), array(y)


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
    return array(sets), array(target_outputs)


def prep_sequence_target_yield(sequence: list, result_yield: float) -> tuple[array, array]:
    # TODO: Add return description
    """
    Split the data into sets of length n_steps and have their target always be yield
    :param sequence: list - Univariate list of numbers
    :param result_yield: float - The target yield amount that the model is meant to predict towards
    :return: (tuple[np.ndarray, np.ndarray]) -
    """

    def pad_list(lst, pad_left, pad_right):
        total_length = len(lst) + pad_left + pad_right
        padded_array = zeros(total_length, dtype=float)
        padded_array[pad_left:pad_left + len(lst)] = lst
        return padded_array

    sets = []
    target_outputs = []
    end_i_set = len(sequence)
    for i, _ in enumerate(sequence):
        seq_set, seq_target_output = sequence[0:end_i_set - i], result_yield
        seq_set = pad_list(seq_set, 0, i)
        sets.append(seq_set)
        target_outputs.append(seq_target_output)
    return array(sets), array(target_outputs)


class DataHandler:
    def __init__(self, plots: list[Plot]) -> None:
        self.plots = plots
        self.uni_lstm_training_sets: list[(bool, list, Plot)] = []

    def make_uni_lstm_training_sets(self, target_variate: str):
        """
        Makes a set of univariate training sets with given target variate and saves
        it to classes univariate_training_sets
        :param target_variate: str - The variate to target when creating the training sets
        """

        # TODO: Predict indices fix
        percentage = 80
        total_amt = len(self.plots)
        unique_count = int(total_amt * (percentage / 100))
        predict_plot_indices = set()

        while len(predict_plot_indices) < unique_count:
            index = random.randint(0, total_amt - 1)
            predict_plot_indices.add(index)

        predict_plot_indices = list(predict_plot_indices)

        # Make training sets
        for i, plot in enumerate(self.plots):
            uni_var_set = self.get_uni_lstm_set(plot, target_variate)
            if len(uni_var_set) > 0:
                if i in predict_plot_indices:
                    self.uni_lstm_training_sets.append((False, uni_var_set, plot))
                else:
                    self.uni_lstm_training_sets.append((True, uni_var_set, plot))
        pass

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

    def uni_lstm_training_on_test_sets(self, model: UnivariateLSTM):
        # TODO: Function description
        """

        :param model:
        :return:
        """
        for test_set in self.uni_lstm_training_sets:
            if test_set[0]:
                model.train(test_set[1], test_set[2].crop_yield)

    def get_uni_lstm_untested_sets(self) -> list[tuple]:
        # TODO: Function description
        """

        :return:
        """
        untested = list(map(lambda trio: (trio[1], trio[2]),
                        list(filter(lambda trio: not trio[0], self.uni_lstm_training_sets))))
        return untested

    def get_uni_lstm_predictions_for_set(self, model: UnivariateLSTM, test_set: list) -> list:
        # TODO: Function description
        """

        :param model:
        :param test_set:
        :return:
        """
        predictions = []
        tests_for_each_day = prep_sequence_target_yield(test_set, 0)[0]
        for test_set in tests_for_each_day:
            predictions.append(model.predict(test_set)[0][0])
        return predictions
