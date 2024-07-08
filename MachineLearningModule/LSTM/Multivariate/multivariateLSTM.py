from MachineLearningModule.LSTM.lstm_model import LSTMModel


class MultivariateLSTM(LSTMModel):
    def __init__(self, num_epochs: int = 500, verbose: int = 1) -> None:
        super().__init__(num_epochs, verbose)
