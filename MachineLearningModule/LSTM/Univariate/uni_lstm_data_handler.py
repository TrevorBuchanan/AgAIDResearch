import random
import ast
import heapq

from DataStructures.plot import Plot

from Helpers.utility import get_plot, percent_error

from MachineLearningModule.LSTM.Univariate.univariateLSTM import UnivariateLSTM
from MachineLearningModule.data_handler import DataHandler, prep_sequence_target_val


class UniLSTMDataHandler(DataHandler):
    def __init__(self, plots: list[Plot]) -> None:
        super().__init__(plots)
        self.plots = plots
        self.training_sets: list[tuple[list, int, int]] = []
        self.testing_sets: list[tuple[list, int, int]] = []
        self.predictions: list[tuple[list, int, int, float]] = []
        self.accuracies: list[tuple[list, int, int]] = []

    def make_sets(self, target_variate: str, training_percentage_amt: int) -> None:
        """
        Makes a set of uni-variate training and testing sets with given target variate and saves
        them to training_sets and testing_sets
        :param training_percentage_amt: int - The amount of data that is used to train with
        :param target_variate: str - The variate to target when creating the training sets
        :return: None
        """

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
        # self.cut_sets_to_level()
        # self.bulk_sets_to_level()
        print(f'Number of training sets: {len(self.training_sets)}')
        print(f'Number of testing sets: {len(self.testing_sets)}')

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

    def make_predictions_and_accuracies_for_test_sets(self, model: UnivariateLSTM) -> None:
        """
        Populate self's list of predictions for test sets (also populates accuracies)
        :param model: keras.models.Sequential - Model to predict with
        :return: None
        """
        self.clear_predictions()
        for test_set in self.testing_sets:
            test_sets_for_each_day, _ = prep_sequence_target_val([test_set[0]], [0 for _, _ in enumerate(test_set)], 0)
            predictions = []
            accuracies = []
            expected = get_plot(test_set[1], test_set[2], self.plots).crop_yield
            for t_set in reversed(test_sets_for_each_day):
                prediction = model.predict(t_set)
                predictions.append(prediction)
                accuracies.append(percent_error(prediction, expected))
            self.predictions.append((predictions, test_set[1], test_set[2], expected))
            self.accuracies.append((accuracies, test_set[1], test_set[2]))

    def make_predictions_and_accuracies_for_training_sets(self, model: UnivariateLSTM) -> None:
        """
        Populate self's list of predictions for test sets (also populates accuracies)
        :param model: keras.models.Sequential - Model to predict with
        :return: None
        """
        self.clear_predictions()
        for test_set in self.training_sets:
            test_sets_for_each_day, _ = prep_sequence_target_val([test_set[0]], [0 for _, _ in enumerate(test_set)], 0)
            predictions = []
            accuracies = []
            expected = get_plot(test_set[1], test_set[2], self.plots).crop_yield
            for t_set in reversed(test_sets_for_each_day):
                prediction = model.predict(t_set)
                predictions.append(prediction)
                accuracies.append(percent_error(prediction, expected))
            self.predictions.append((predictions, test_set[1], test_set[2], expected))
            self.accuracies.append((accuracies, test_set[1], test_set[2]))

    def clear_predictions(self) -> None:
        """
        Clears the predictions and accuracies
        :return: None
        """
        self.predictions.clear()
        self.accuracies.clear()

    def save_sets(self, model_num: int) -> None:
        """
        Saves the testing and training data to respective files
        :return: None
        """
        test_file_path = f'MachineLearningModule/saved_test_data_{model_num}.txt'
        with open(test_file_path, 'w') as file:
            for tup in self.testing_sets:
                line = ', '.join(map(str, tup))
                file.write(line + '\n')

        training_file_path = f'MachineLearningModule/saved_training_data_{model_num}.txt'
        with open(training_file_path, 'w') as file:
            for tup in self.training_sets:
                line = ', '.join(map(str, tup))
                file.write(line + '\n')

    def load_saved_sets(self, max_training_data_amt: int, model_num: int) -> None:
        """
        Loads saved testing and training data from their respective files
        :param: max_training_data_amt: Used to limit the amount of data sets that the model is given at once
        :param: model_num: The identification number of the model
        :return: None
        """
        test_file_path = f'MachineLearningModule/SavedDataForModels/saved_test_data_{model_num}.txt'
        with open(test_file_path, 'r') as file:
            for line in file:
                tuple_str = line.strip()
                parsed_tuple = ast.literal_eval(tuple_str)
                self.testing_sets.append(parsed_tuple)

        amt = 0
        training_file_path = f'MachineLearningModule/SavedDataForModels/saved_training_data_{model_num}.txt'
        with open(training_file_path, 'r') as file:
            for line in file:
                if amt >= max_training_data_amt:
                    continue
                tuple_str = line.strip()
                parsed_tuple = ast.literal_eval(tuple_str)
                self.training_sets.append(parsed_tuple)
                amt += 1
        print(f'Number of training sets: {len(self.training_sets)}')
        print(f'Number of testing sets: {len(self.testing_sets)}')

    def cut_sets_to_level(self):
        """
        Balances the distribution of crop yields across the training sets by moving some sets to the testing sets.
        :return: None
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
        Balances the distribution of crop yields across the training sets by fabricating new sets.
        :return: None
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
        to_add = []
        max_amt = max(buckets)
        for tup in self.training_sets:
            index = self.get_bucket_index(get_plot(tup[1], tup[2], self.plots).crop_yield,
                                          min_val, max_val, num_buckets)
            amt = buckets[index]
            if amt < max_amt:
                for _ in range(max_amt - amt):
                    to_add.append(self.fabricate_set(tup))
                    buckets[index] += 1

        for add in to_add:
            self.training_sets.append(add)

    @staticmethod
    def fabricate_set(original_set: tuple[list, int, int], max_deviation: float = 0.01) -> tuple[list, int, int]:
        """
        Fabricates a new set by slightly modifying the values of the original set within a specified deviation range.
        :param original_set: A tuple containing a list of values and two integers.
        :param max_deviation: The maximum deviation for adjusting the values in the original set.
        :return: A new set with adjusted values and the same integers as the original set.
        """
        new_set = []
        for val in original_set[0]:
            new_set.append(val + random.uniform(-max_deviation, max_deviation))
        return new_set, original_set[1], original_set[2]

    @staticmethod
    def get_bucket_index(num: float, min_value: float, max_value: float, num_buckets: int) -> int:
        """
        Calculates the bucket index for a given number within a specified range and number of buckets.
        :param num: The number to categorize.
        :param min_value: The minimum value of the range.
        :param max_value: The maximum value of the range.
        :param num_buckets: The number of buckets to divide the range into.
        :return: The index of the bucket where the number falls.
        """
        bucket_range = (max_value - min_value) / num_buckets
        if bucket_range == 0:  # All numbers are the same
            return 0
        bucket_index = int((num - min_value) / bucket_range)
        # Make sure the last bucket includes the max_value
        if bucket_index == num_buckets:
            bucket_index -= 1
        return bucket_index

    def continue_training_on_weak_sets(self, model, num_worst):
        def avg(acc_set):
            return sum(acc_set[0]) / len(acc_set[0])

        # Min-heap to keep track of the lowest 3 averages
        lowest_avgs = []
        for accuracy_set in self.accuracies:
            current_avg = avg(accuracy_set)
            if len(lowest_avgs) < num_worst:
                heapq.heappush(lowest_avgs, (current_avg, accuracy_set))
            else:
                heapq.heappushpop(lowest_avgs, (current_avg, accuracy_set))
        lowest_avg_sets = [set_info[1] for set_info in lowest_avgs]


