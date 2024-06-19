import random

from DataStructures.plot import Plot
from MachineLearningModule.LSTM.Univariate.univariateLSTM import UnivariateLSTM
from MachineLearningModule.data_handler import DataHandler, prep_sequence_target_val


class UniLSTMDataHandler(DataHandler):
    def __init__(self, plots: list[Plot]) -> None:
        super().__init__(plots)
        self.plots = plots
        self.training_sets: list[(list, Plot)] = []
        self.testing_sets: list[(list, Plot)] = []
        self.use_saved_test_plots = False

    def make_sets(self, target_variate: str):
        """
        Makes a set of uni-variate training and testing sets with given target variate and saves
        them to uni_lstm_training_sets and uni_lstm_testing_sets
        :param target_variate: str - The variate to target when creating the training sets
        """

        training_percentage_amt = 90
        total_amt = len(self.plots)
        unique_count = int(total_amt * (training_percentage_amt / 100))
        test_plot_indices = set()

        while len(test_plot_indices) < unique_count:
            index = random.randint(0, total_amt - 1)
            test_plot_indices.add(index)

        test_plot_indices = list(test_plot_indices)
        if len(test_plot_indices) == 0:
            test_plot_indices.append(random.randint(0, total_amt - 1))
        # Make training sets
        for i, plot in enumerate(self.plots):
            uni_var_set = self.get_uni_lstm_set(plot, target_variate)
            if len(uni_var_set) > 0:
                if i in test_plot_indices:  # Check if in 80 percent group of test plots
                    self.uni_lstm_training_sets.append((uni_var_set, plot))
                else:
                    self.uni_lstm_testing_sets.append((uni_var_set, plot))

    @staticmethod
    def get_set(plot: Plot, target_variate: str) -> list:
        """
        Get a list of values of given plot, and target variate
        :param plot: Plot - Plot to get set from
        :param target_variate: str - The variate type to target in the plot
        :returns: list - list of target variate values
        """
        uni_variate_set = []
        for dp in plot.data_points:
            value = getattr(dp.vi_state, target_variate, None)
            if value is None:
                value = getattr(dp.conditions_state, target_variate, None)
            if value is not None:
                uni_variate_set.append(value)
        return uni_variate_set

    def train_on_test_sets(self, model: UnivariateLSTM):
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

    @staticmethod
    def get_predictions_for_set(model: UnivariateLSTM, test_set: list) -> list:
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

    def save_test_plots(self):
        pass

    def load_saved_test_plots(self):
        pass
