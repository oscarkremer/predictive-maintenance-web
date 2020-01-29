from .model_template import ModelTemplate
from .nd_model.model import kerasND
import numpy as np

class ND(ModelTemplate):
    def __init__(self, data_size=1000, units=10, epochs=10, forecast_length=2000, L1_reg=0.01, validation_length=100, batch_size=32):
        self.validation_length = validation_length
        self.forecast_length = forecast_length
        self.data_size = data_size
        self.units = units
        self.L1_reg = L1_reg
        self.batch_size = batch_size
        
        self.model = kerasND(data_size, units,
                    epochs, 
                    forecast_length,
                    L1_reg,
                    validation_length,
                    batch_size) 
        self.error = float('inf')

    def fit(self, data):
        training = self._transform(data)
        training = training.reshape((training.shape[1]))
        self.model.create_keras_model(training)
        self.model.train()

    def predict(self, days=0):
        self.model.forecast_periods = days
        self.forecast_length = days
        self.model.predict()
        return self.model.predictions[-self.forecast_length:]

    def _transform(self, data, days=0):
        """
        Returns all inputs and expected outputs, The shape should be
        (products, window, features), (products, window, 1)
        Keyword arguments:
        data -- dataset containing Products and its time series
        days -- relative to how many days will be returned as True values
        """
        all_x = data[:, :, :1]
        return np.array(all_x)