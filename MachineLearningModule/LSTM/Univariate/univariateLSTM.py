from MachineLearningModule.LSTM.lstm_model import LSTMModel


class UnivariateLSTM(LSTMModel):
    def __init__(self, num_epochs: int = 500, verbose: int = 1) -> None:
        super().__init__(num_epochs, verbose)

    def train(self, training_sequences: list[list], target_values: list[float]) -> None:
        """
        Used to train LSTM on given training sequences targeting corresponding given target values
        :param training_sequences: list[list] - list of sequences that correspond to a target output in target_values
        :param target_values: list[float] - list of target values that lstm tries to train towards
        :return: None
        """
        raise NotImplementedError("No train function implemented")

    def predict(self, sequence: list) -> float:
        """
        Function to be called to get predicted value after training
        :param sequence: list - Sequence of numbers to be tested and predicted for
        :return: float - Result of running the input sequence through the LSTM model
        """
        raise NotImplementedError("No predict function implemented")
