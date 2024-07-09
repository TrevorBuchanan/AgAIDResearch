from Helpers.utility import shuffle_in_unison

from numpy import array
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import LSTM, Dense, Input, Dropout, BatchNormalization, Masking
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.regularizers import l2

from MachineLearningModule.LSTM.lstm_model import LSTMModel
from MachineLearningModule.data_handler import prep_sequences_target_val


class StackedLSTM(LSTMModel):
    def __init__(self, num_epochs: int = 300, verbose: int = 1):
        super().__init__(num_epochs, verbose)

    def build_model(self, n_steps):
        self.model = Sequential()
        self.model.add(Input(shape=(n_steps, self.n_features)))
        self.model.add(Masking(mask_value=0.0))
        self.model.add(LSTM(50, activation='relu', return_sequences=True, kernel_regularizer=l2(0.01)))
        self.model.add(Dropout(0.2))
        self.model.add(BatchNormalization())
        self.model.add(LSTM(50, activation='relu', kernel_regularizer=l2(0.01)))
        self.model.add(Dropout(0.2))
        self.model.add(BatchNormalization())
        self.model.add(Dense(1, kernel_regularizer=l2(0.01)))
        optimizer = Adam(learning_rate=0.0005)
        self.model.compile(optimizer=optimizer, loss='mse')

    def train(self, training_sequences: list[list], target_values: list[float]):
        sets, target_outs = prep_sequences_target_val(training_sequences, target_values, 2)
        sets, target_outs = shuffle_in_unison(sets, target_outs)
        n_steps = sets.shape[0]
        # TODO: Make sure n steps are right and sets are correct from
        #  sets = sets.reshape((sets.shape[0], sets.shape[1], self.n_features))
        self.n_features = len(training_sequences[0])
        print(sum(target_outs) / len(target_outs))
        # Define model
        if self.model is None:
            self.build_model(n_steps)
        # Early stopping
        early_stopping = EarlyStopping(monitor='val_loss', patience=25, restore_best_weights=True)
        # Fit model with validation split
        self.model.fit(sets, target_outs, epochs=self.num_epochs, verbose=self.verbose,
                       validation_split=0.2, callbacks=[early_stopping])

    def predict(self, sequence: list):
        sequence = array(sequence)
        sequence = sequence.reshape((1, len(sequence), self.n_features))
        predicted = self.model.predict(sequence, verbose=self.verbose)
        return predicted[0][0]

