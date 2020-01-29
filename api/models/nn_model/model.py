import numpy as np
from keras.layers import Dense, Input
from keras.layers.merge import Concatenate
from keras.models import Model
from keras import regularizers
from keras.engine.training import Model
from keras.callbacks import ModelCheckpoint
from copy import copy
from tensorflow import sin
from keras.backend import set_value
from sklearn.metrics import mean_squared_error

class kerasNN:
    def __init__(self, data_size, units,
                 epochs, forecast_periods,
                 L1_reg,
                 validation_length,
                 batch_size, optimizer='rmsprop',
                 loss='mean_squared_error'):
        self.n_data = data_size
        self.optimizer = optimizer
        self.loss = loss
        self.units = units
        self.epochs = epochs
        self.forecast_periods = forecast_periods
        self.L1_reg = L1_reg
        self.validation_length = validation_length
        self.batch_size = batch_size

    def create_keras_model(self, trainX, trainY):
        self.data = trainY
        input_data = Input(shape=(1 ,), name='input_data')
        sinusoid = Dense(self.n_data, activation=sin, #np.sin
                         name=None)(input_data)
        linear = Dense(self.units, activation='linear',
                       )(input_data)
        softplus = Dense(self.units, activation='softplus',
                         )(input_data) 
        sigmoid = Dense(self.units, activation='sigmoid',
                        )(input_data) 
        one_layer = Concatenate()([sinusoid, linear,
                                   softplus, sigmoid])
        output_layer = Dense(1, kernel_regularizer=regularizers.l1(self.L1_reg))(one_layer)
        keras_model = Model(inputs=[input_data], outputs=[output_layer])
        keras_model.compile(loss=self.loss, optimizer=self.optimizer)
        keras_model = kerasNN.initialize_weights(
            keras_model, self.n_data, self.units)
        self.keras_model = keras_model
        self.x = trainX
        y, self.max_min_list= kerasNN.scale_data(self.data, self.units)
        return None

    @staticmethod
    def initialize_weights(keras_model, n_data, units):
        if not isinstance(keras_model, Model):
            raise TypeError('Input must be Keras Model!')
        noise = 0.001
        np.random.seed(42)
        set_value(keras_model.weights[0],
            (2 * np.pi * np.floor(np.arange(n_data) / 2))[np.newaxis, :].astype('float32'))
        set_value(keras_model.weights[1],
            (np.pi / 2 + np.arange(n_data) % 2 * np.pi / 2).astype('float32'))
        for layer in range(2, 8):
            if layer == 2:
                set_value(keras_model.weights[layer],
                    (np.ones(shape=(1, units)) + np.random.normal(
                        size=(1, units))*noise).astype('float32')) 
            elif layer in [3, 5, 7]:
                set_value(keras_model.weights[layer],
                    (np.random.normal(size=(units)) * noise).astype('float32'))
            else:
                set_value(keras_model.weights[layer],
                    (np.random.normal(size=(1, units)) * noise).astype('float32'))
        set_value(keras_model.weights[8],
            (np.random.normal(size=(n_data + 3 * units, 1))*noise).astype('float32'))
        set_value(keras_model.weights[9],
            (np.random.normal(size=(1)) * noise).astype('float32'))

        return keras_model

    def train(self):
        y, self.max_min_list= kerasNN.scale_data(self.data, self.units)
        assert len(y) == len(self.data)
        x_val = self.x[-self.validation_length:]
        y_val = y[-self.validation_length:]

        x = self.x[:-self.validation_length]
        y = y[:-self.validation_length]

        weights_path = 'nd_weights.hdf5'
        self.keras_model.fit(
            x, y, epochs=self.epochs, verbose=1,
            batch_size=self.batch_size,
            validation_data=(x_val, y_val))
        self.keras_model.save_weights(weights_path)
        return None

    def predict(self, point):
        self.keras_model.load_weights('nd_weights.hdf5')
        prediction = self.keras_model.predict(point)
        prediction = kerasNN.inverse_scale_data(prediction, self.max_min_list, self.units)
        return prediction

    @staticmethod
    def scale_data(data, units):
        min_value = data.min()
        max_value = data.max()
        scaled_output = (data - min_value) / (max_value - min_value) * units

        return scaled_output, [max_value, min_value]

    @staticmethod
    def inverse_scale_data(data, max_min_list, units):
        if len(max_min_list) != 2:
            raise TypeError('Input must be list and len == 2!')
        if max_min_list[1] > max_min_list[0]:
            raise ValueError('Check values in the input list!')

        # get min and max values
        max_value = max_min_list[0]
        min_value = max_min_list[1]

        inv_scaled_data = data * (max_value - min_value) / units + min_value

        return inv_scaled_data