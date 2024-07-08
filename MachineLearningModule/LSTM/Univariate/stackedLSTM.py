from Helpers.utility import shuffle_in_unison
from MachineLearningModule.LSTM.Univariate.univariateLSTM import UnivariateLSTM
from numpy import array
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import LSTM, Dense, Input, Dropout, BatchNormalization, Masking
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.regularizers import l2
from sklearn.model_selection import GridSearchCV
from scikeras.wrappers import KerasClassifier
from MachineLearningModule.data_handler import prep_sequence_target_val


class StackedLSTM(UnivariateLSTM):
    def __init__(self, model_number, num_epochs: int = 500, optimizer: str = 'adam', loss_function: str = 'mse',
                 verbose: int = 1, activation_function: str = 'relu'):
        super().__init__(model_number, num_epochs, optimizer, loss_function, verbose, activation_function)

    def build_model(self, n_steps):
        model = Sequential()
        model.add(Input(shape=(n_steps, self.n_features)))
        model.add(Masking(mask_value=0.0))
        model.add(LSTM(50, activation=self.activation_function, return_sequences=True,
                       kernel_regularizer=l2(0.01)))
        model.add(Dropout(0.2))
        model.add(BatchNormalization())
        model.add(LSTM(50, activation=self.activation_function, kernel_regularizer=l2(0.01)))
        model.add(Dropout(0.2))
        model.add(BatchNormalization())
        model.add(Dense(1, kernel_regularizer=l2(0.01)))
        optimizer = Adam(learning_rate=0.0005)
        model.compile(optimizer=optimizer, loss=self.loss_function)
        return model

    def train(self, training_sequences: list[list], target_values: list[float]):
        sets, target_outs = prep_sequence_target_val(training_sequences, target_values, 2)
        sets, target_outs = shuffle_in_unison(sets, target_outs)
        n_steps = sets.shape[1]
        sets = sets.reshape((sets.shape[0], sets.shape[1], self.n_features))
        print(sum(target_outs) / len(target_outs))
        # Define model
        if self.model is None:
            self.model = self.build_model(n_steps)

        # # Early stopping
        # early_stopping = EarlyStopping(monitor='loss', patience=100, restore_best_weights=True)
        # # Fit model with validation split
        # self.model.fit(sets, target_outs, epochs=self.num_epochs, verbose=self.verbose, callbacks=[early_stopping])

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

