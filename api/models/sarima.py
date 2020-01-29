import numpy as np
import statsmodels.tsa.statespace.sarimax as sarimax_model
from .model_template import ModelTemplate


class SARIMA(ModelTemplate):

    def __init__(self, p=0, q=0, d=1, P=0, Q=0, D=0, m=0):
        self.p = p 
        self.q = q 
        self.d = d 
        self.P = P 
        self.Q = Q 
        self.D = D 
        self.m = m
        self.order = [p, q, d]
        self.seasonal_order = [P, Q, D, m]
        self.error = float('inf')

    def fit(self, data):
        self.data = data
        pass

    def predict(self, points):
        data = self._transform()
        history = list(data.copy())
        model = sarimax_model.SARIMAX(history, order=self.order, seasonal_order = self.seasonal_order,
                enforce_stationarity=False,enforce_invertibility=False).fit(disp=0)
        predictions = model.predict(data.shape[0]-1, points + data.shape[0]-1)[1:]
        return np.array(predictions).reshape(np.array(predictions).shape[0])

    def _transform(self):
        all_x = np.array(self.data[:, :, :1])
        return np.array(all_x).reshape((all_x.shape[1]))