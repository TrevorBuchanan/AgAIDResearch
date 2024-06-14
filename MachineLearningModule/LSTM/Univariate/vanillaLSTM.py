from MachineLearningModule.LSTM.Univariate.univariateLSTM import UnivariateLSTM

from numpy import array
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import LSTM, Dense, Input, Dropout, BatchNormalization
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping

from MachineLearningModule.data_handler import prep_sequence_target_yield

class VanillaLSTM(UnivariateLSTM):
    def __init__(self, num_epochs: int = 1000, optimizer: str ='adam', loss_function: str ='mse',
                 verbose: int = 1, activation_function: str = 'relu'):
        super().__init__(num_epochs, optimizer, loss_function, verbose, activation_function)
        self.model = None
        self.n_features = 1

    def load_trained_model(self):
        self.model = load_model('vanilla_model.keras')

    def train(self, training_sequence: list, target_yield: float):
        sets, target_outs = prep_sequence_target_yield(training_sequence, target_yield)

        sets = sets.reshape((sets.shape[0], sets.shape[1], self.n_features))

        # Define model
        if self.model is None:
            self.model = Sequential()
            self.model.add(Input(shape=((len(training_sequence)), self.n_features)))
            self.model.add(LSTM(100, activation=self.activation_function))  # 100 Units (neurons)
            self.model.add(Dropout(0.2))
            self.model.add(BatchNormalization())
            self.model.add(Dense(1))
            optimizer = Adam(learning_rate=0.001)
            self.model.compile(optimizer=optimizer, loss=self.loss_function)
            # self.model.compile(optimizer=self.optimizer, loss=self.loss_function)
        # Fit model
        early_stopping = EarlyStopping(monitor='loss', patience=10)
        self.model.fit(sets, target_outs, epochs=self.num_epochs, verbose=self.verbose, callbacks=[early_stopping])
        # Save model
        self.model.save('vanilla_model.keras')

    def predict(self, sequence: list):
        sequence = array(sequence)
        sequence = sequence.reshape((1, len(sequence), self.n_features))
        predicted = self.model.predict(sequence, self.verbose)
        return predicted

