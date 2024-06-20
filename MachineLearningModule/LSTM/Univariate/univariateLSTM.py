class UnivariateLSTM:
    def __init__(self, num_epochs: int = 500, optimizer: str ='adam', loss_function: str ='mse',
                 verbose: int = 1, activation_function: str = 'relu') -> None:
        self.num_epochs = num_epochs   
        self.optimizer = optimizer
        self.loss_function = loss_function
        self.verbose = verbose
        self.activation_function = activation_function
        self.model = None
        self.n_features = 1

    def load_trained_model(self, season: str, vi_formula: str, target_variate: str) -> None:
        """
        Loads trained model
        :param season: str - Season for which the model was trained for
        :param vi_formula: str - VI formula for which the model was trained for
        :param target_variate: str - Variate for which the model was trained for
        :return: None
        """
        raise NotImplementedError("No load_trained_model function implemented")

    def save_trained_model(self, season: str, vi_formula: str, target_variate: str) -> None:
        """
        Saves trained model
        :param season: str - Season for which the model was trained for
        :param vi_formula: str - VI formula for which the model was trained for
        :param target_variate: str - Variate for which the model was trained for
        :return: None
        """
        raise NotImplementedError("No save_trained_model function implemented")

    def build_model(self, n_steps):
        """
        Builds a uni-variate LSTM model
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
    