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