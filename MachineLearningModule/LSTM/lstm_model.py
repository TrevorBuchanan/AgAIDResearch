from tensorflow.keras.models import load_model


class LSTMModel:
    def __init__(self, num_epochs: int = 500, verbose: int = 1) -> None:
        self.num_epochs = num_epochs
        self.verbose = verbose
        self.model = None
        self.n_features = 1

    def load_trained_model(self, model_num):
        self.model = load_model(f'MachineLearningModule/LSTM/SavedModels/model_{model_num}.keras')

    def save_trained_model(self, model_num):
        self.model.save(f'MachineLearningModule/LSTM/SavedModels/model_{model_num}.keras')

    def build_model(self, n_steps):
        """
        Builds an LSTM model
        :param n_steps: int - Size of input shape (features=1 because only predicting one value)
        :return: keras.models.Sequential - New built LSTM model
        """
        raise NotImplementedError("No build_model function implemented")

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
