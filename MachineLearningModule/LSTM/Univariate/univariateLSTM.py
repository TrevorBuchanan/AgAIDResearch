from numpy import array
from keras.models import Sequential
from keras.layers import LSTM
from keras.layers import Dense
from keras.layers import Bidirectional
from keras.layers import Input


class UnivariateLSTM:
    def __init__(self, num_epochs: int = 500, optimizer: str ='adam', loss_function: str ='mse', 
                 verbose: int = 1, activation_function: str = 'relu') -> None:
        self.num_epochs = num_epochs   
        self.optimizer = optimizer
        self.loss_function = loss_function
        self.verbose = verbose
        self.activation_function = activation_function

    def train():
        """
        Used to train LSTM
        """    
        raise NotImplementedError
        
        # define input sequence
        raw_seq = [10, 20, 30, 40, 50, 60, 70, 80, 90]
        # choose a number of time steps
        n_steps = 3
        # split into samples
        X, y = split_sequence(raw_seq, n_steps)
        # reshape from [samples, timesteps] into [samples, timesteps, features]
        n_features = 1
        X = X.reshape((X.shape[0], X.shape[1], n_features))
        # define model
        model = Sequential()
        model.add(Input(shape=(n_steps, n_features)))
        model.add(Bidirectional(LSTM(50, activation='relu')))
        model.add(Dense(1))
        model.compile(optimizer='adam', loss='mse')
        # fit model
        model.fit(X, y, epochs=500, verbose=1)
        # demonstrate prediction
        x_input = array([90, 80, 70])
        x_input = x_input.reshape((1, n_steps, n_features))
        yhat = model.predict(x_input, verbose=1)
        print(yhat)

    def use():
        """
        Function to be called to get predicted value after training
        """
        raise NotImplementedError
        


