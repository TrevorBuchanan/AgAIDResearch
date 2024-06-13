from DataStructures.plot import Plot
from numpy import array

class DataPrepper:
    def __init__(self, plots: list[Plot]) -> None:
        self.data_set = plots
    
    def get_univariate_set(variety_block_pair: tuple, target_variate: str) -> list:
        """
        Get a list of values of given variety, block, and target variate
        variety_block_pair (tuple): Set describing the variety and block of a plot
        target_variate (str): The variate type to target in the plot
        return (list): list of target variate values
        """
        pass

    # https://machinelearningmastery.com/how-to-develop-lstm-models-for-time-series-forecasting/
    @staticmethod
    def split_sequence(sequence, n_steps):
        X, y = list(), list()
        for i in range(len(sequence)):
            # find the end of this pattern
            end_ix = i + n_steps
            # check if we are beyond the sequence
            if end_ix > len(sequence)-1:
                break  
            # gather input and output parts of the pattern
            seq_x, seq_y = sequence[i:end_ix], sequence[end_ix]
            X.append(seq_x)
            y.append(seq_y)
        return array(X), array(y)
    
    @staticmethod
    def split_sequence_target_yield(sequence: list, n_steps: int, yeild: float):
        """
        Split the data into sets of length n_steps and have their target always be yeild
        sequence (list): Univariate list of numbers
        n_steps (int): Length of sets that will be fed to the LSTM model
        yeild (float): The target yield amount that the model is meant to predict towards
        """
        pass
        