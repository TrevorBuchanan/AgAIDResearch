import random
import ast

from DataStructures.plot import Plot

from Helpers.utility import get_plot

from MachineLearningModule.LSTM.Univariate.univariateLSTM import UnivariateLSTM
from MachineLearningModule.data_handler import DataHandler, prep_sequence_target_val


class UniLSTMDataHandler(DataHandler):
    def __init__(self, plots: list[Plot]) -> None:
        super().__init__(plots)
        self.plots = plots
        self.training_sets: list[(list, int, int)] = []
        self.testing_sets: list[(list, int, int)] = []

    def make_sets(self, target_variate: str) -> None:
        """
        Makes a set of uni-variate training and testing sets with given target variate and saves
        them to training_sets and testing_sets
        :param target_variate: str - The variate to target when creating the training sets
        :return: None
        """

        training_percentage_amt = 80
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
            uni_var_set = self.get_set(plot, target_variate)
            if len(uni_var_set) > 0:
                if i in test_plot_indices:  # Check if in 80 percent group of test plots
                    self.training_sets.append((uni_var_set, plot.variety_index, plot.replication_variety))
                else:
                    self.testing_sets.append((uni_var_set, plot.variety_index, plot.replication_variety))
        self.cut_sets_to_level()
        # self.bulk_sets_to_level()

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

    def train_on_training_sets(self, model: UnivariateLSTM):
        """
        Train given model on class's training sets
        :param model: keras.models.Sequential - Model to be trained
        :return: None
        """
        test_sets = []
        targets = []
        for test_set in self.training_sets:
            test_sets.append(test_set[0])
            targets.append(get_plot(test_set[1], test_set[2], self.plots).crop_yield)

        model.train(test_sets, targets)

    @staticmethod
    def get_predictions_for_set(model: UnivariateLSTM, test_set: list) -> list:
        """
        Get list of predictions for given test set
        :param model: keras.models.Sequential - Model to predict from test set
        :param test_set: list - Sequence to give to model to predict from
        :return: list - List of predicted values
        """
        predictions = []
        tests_for_each_day = prep_sequence_target_val([test_set], [0 for _, _ in enumerate(test_set)])[0]
        for test_set in tests_for_each_day:
            predictions.append(model.predict(test_set))
        return predictions

    def save_sets(self) -> None:
        """
        Saves the testing and training data to respective files
        :return: None
        """
        test_file_path = 'MachineLearningModule/saved_test_data.txt'
        with open(test_file_path, 'w') as file:
            for tup in self.testing_sets:
                line = ', '.join(map(str, tup))
                file.write(line + '\n')

        training_file_path = 'MachineLearningModule/saved_training_data.txt'
        with open(training_file_path, 'w') as file:
            for tup in self.training_sets:
                line = ', '.join(map(str, tup))
                file.write(line + '\n')

    def load_saved_sets(self) -> None:
        """
        Loads saved testing and training data from their respective files
        :return: None
        """
        temp_max_amt = 14  # Used to limit the amount of data sets that the model is given at once
        amt = 0
        test_file_path = 'MachineLearningModule/saved_test_data.txt'
        with open(test_file_path, 'r') as file:
            for line in file:
                if amt >= temp_max_amt:
                    continue
                tuple_str = line.strip()
                parsed_tuple = ast.literal_eval(tuple_str)
                self.testing_sets.append(parsed_tuple)
                amt += 1

        amt = 0
        training_file_path = 'MachineLearningModule/saved_training_data.txt'
        with open(training_file_path, 'r') as file:
            for line in file:
                if amt >= temp_max_amt:
                    continue
                tuple_str = line.strip()
                parsed_tuple = ast.literal_eval(tuple_str)
                self.training_sets.append(parsed_tuple)
                amt += 1

    def cut_sets_to_level(self):
        # TODO: Func def
        """

        :return:
        """
        yields = []
        for tup in self.training_sets:
            yields.append(get_plot(tup[1], tup[2], self.plots).crop_yield)

        min_val = min(yields)
        max_val = max(yields)
        num_buckets = 7
        buckets = [0] * num_buckets
        for tup in self.training_sets:
            buckets[self.get_bucket_index(get_plot(tup[1], tup[2], self.plots).crop_yield,
                                          min_val, max_val, num_buckets)] += 1
        min_amt = min(buckets)
        to_rmv = []
        for tup in self.training_sets:
            index = self.get_bucket_index(get_plot(tup[1], tup[2], self.plots).crop_yield,
                                          min_val, max_val, num_buckets)
            if buckets[index] > min_amt:
                to_rmv.append(tup)
                buckets[index] -= 1

        for rmv in to_rmv:
            self.training_sets.remove(rmv)
            self.testing_sets.append(rmv)

    def bulk_sets_to_level(self):
        """

        :return:
        """
        # TODO: func def
        yields = []
        for tup in self.training_sets:
            yields.append(get_plot(tup[1], tup[2], self.plots).crop_yield)

        min_val = min(yields)
        max_val = max(yields)
        num_buckets = 7
        buckets = [0] * num_buckets
        for tup in self.training_sets:
            buckets[self.get_bucket_index(get_plot(tup[1], tup[2], self.plots).crop_yield,
                                          min_val, max_val, num_buckets)] += 1
        min_amt = min(buckets)
        to_add = []
        for tup in self.training_sets:
            index = self.get_bucket_index(get_plot(tup[1], tup[2], self.plots).crop_yield,
                                          min_val, max_val, num_buckets)
            if buckets[index] > min_amt:
                to_add.append(tup)
                buckets[index] -= 1

        for add in to_add:
            self.training_sets.append(add)

    @staticmethod
    def fabricate_set_and_out(original_set, original_out, max_deviation=0.03):
        new_set = []
        for val in original_set:
            new_set.append(val + random.uniform(-max_deviation, max_deviation))
        new_out = original_out + random.uniform(-max_deviation * 5, max_deviation * 5)
        return new_set, new_out

    @staticmethod
    def get_bucket_index(num: float, min_value: float, max_value: float, num_buckets: int) -> int:
        # TODO: func def
        """

        :param num:
        :param min_value:
        :param max_value:
        :param num_buckets:
        :return:
        """
        # Calculate the range of each bucket
        bucket_range = (max_value - min_value) / num_buckets

        # Edge case: all numbers are the same
        if bucket_range == 0:
            return 0

        # Calculate the appropriate bucket index
        bucket_index = int((num - min_value) / bucket_range)

        # Make sure the last bucket includes the max_value
        if bucket_index == num_buckets:
            bucket_index -= 1

        return bucket_index
