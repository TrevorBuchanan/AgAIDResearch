import random
import numpy as np

from DataStructures.plot import Plot

from MachineLearningModule.LSTM.Univariate.univariateLSTM import UnivariateLSTM


def prep_sequence_target_val(sequences: list[list], targets: list[float]) -> tuple[np.array, np.array]:
    """
    Split the data into sets of length n_steps and have their target always be yield
    :param sequences: list[list] - List of uni-variate list of numbers
    :param targets: list[float] - List of target amounts that the model is meant to predict towards
    :return: (tuple[np.ndarray, np.ndarray]) - Returns tuple of 2 numpy arrays holding the test
    sequences and the target values for those tests
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

    # TODO: Change back to 50
    know_threshold = 70
    sets = []
    target_outputs = []
    for sequence, target in zip(sequences, targets):
        end_i_set = len(sequence)
        for i, _ in enumerate(sequence):
            if end_i_set - i < know_threshold:  # Stop adding to the set when past know threshold
                break
            seq_set, seq_target_output = sequence[0:end_i_set - i], target
            seq_set = pad_list(seq_set, 0, i, 0)
            if end_i_set < max_len:
                ignore_padding_len = max_len - end_i_set
                seq_set = pad_list(seq_set, 0, ignore_padding_len, 0)
            sets.append(seq_set)
            target_outputs.append(seq_target_output)
    return np.array(sets), np.array(target_outputs)


class DataHandler:
    def __init__(self, plots: list[Plot]) -> None:
        self.plots = plots
        self.training_sets: list[(list, Plot)] = []
        self.testing_sets: list[(list, Plot)] = []

    # def save_sets(self):
    #     pass
    #
    # def load_saved_sets(self):
    #     pass
