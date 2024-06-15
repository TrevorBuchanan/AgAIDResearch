from MachineLearningModule.LSTM.Univariate.univariateLSTM import UnivariateLSTM

from numpy import array
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import LSTM, Dense, Input, Dropout, BatchNormalization
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.regularizers import l2

from MachineLearningModule.data_handler import prep_sequence_target_yield


class VanillaLSTM(UnivariateLSTM):
    def __init__(self, num_epochs: int = 500, optimizer: str = 'adam', loss_function: str = 'mse',
                 verbose: int = 1, activation_function: str = 'relu'):
        super().__init__(num_epochs, optimizer, loss_function, verbose, activation_function)
        self.model = None
        self.n_features = 1

    def load_trained_model(self):
        # TODO: Add to base
        self.model = load_model('MachineLearningModule/LSTM/SavedModels/vanilla_model.keras')

    def save_trained_model(self):
        # TODO: Add to base
        self.model.save('MachineLearningModule/LSTM/SavedModels/vanilla_model.keras')

    def train(self, training_sequence: list, target_yield: float):
        sets, target_outs = prep_sequence_target_yield(training_sequence, target_yield)
        sets = sets.reshape((sets.shape[0], sets.shape[1], self.n_features))

        print(f'Training with expected yield: {target_yield}')
        # Define model
        if self.model is None:
            self.model = Sequential()
            self.model.add(Input(shape=((len(training_sequence)), self.n_features)))
            self.model.add(LSTM(100, activation=self.activation_function, kernel_regularizer=l2(0.01)))  # 100 Units (neurons)
            self.model.add(Dropout(0.2))
            self.model.add(BatchNormalization())
            self.model.add(Dense(1))
            optimizer = Adam()
            self.model.compile(optimizer=optimizer, loss=self.loss_function)
            # self.model.compile(optimizer=self.optimizer, loss=self.loss_function)
        # Early stopping
        early_stopping = EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)

        # Fit model with validation split
        self.model.fit(sets, target_outs, epochs=self.num_epochs, verbose=self.verbose,
                       validation_split=0.2, callbacks=[early_stopping])

    def predict(self, sequence: list):
        sequence = array(sequence)
        sequence = sequence.reshape((1, len(sequence), self.n_features))
        predicted = self.model.predict(sequence, self.verbose)
        return predicted
