from .model_template import ModelTemplate
from .nn_model.model import kerasNN
import numpy as np

class NN(ModelTemplate):
    def __init__(self, data_size=1000, units=1, epochs=1000, forecast_length=2000, L1_reg=0.1, validation_length=100, batch_size=2):
        self.validation_length = validation_length
        self.forecast_length = forecast_length
        self.data_size = data_size
        self.units = units
        self.L1_reg = L1_reg
        self.batch_size = batch_size
        self.model = kerasNN(data_size, units,
                    epochs, 
                    forecast_length,
                    L1_reg,
                    validation_length,
                    batch_size) 
        self.error = float('inf')

    def fit(self, trainX, trainY):
        self.model.create_keras_model(trainX, trainY)
        self.model.train()

    def predict(self, days=0):
        self.model.forecast_periods = 0
        self.forecast_length = 0 
        self.model.predict()
        return self.model.predictions
