import numpy as np
from sklearn.preprocessing import StandardScaler
from .lstm_model.model import torchLSTM
from .model_template import ModelTemplate

class LSTM(ModelTemplate):

    def __init__(self, learning_rate=0.01, look_back=7, num_layers=2, hidden_size=64, early_stop_patience=10):
        self.model = torchLSTM(
            learning_rate=learning_rate,
            look_back=look_back,
            num_layers=num_layers,
            hidden_size=hidden_size,
            early_stop_patience=early_stop_patience)
        self.look_back = look_back
        self.num_layers = num_layers
        self.hidden_size = hidden_size
        self.scaler = StandardScaler()
        self.error = float('inf')

    def fit(self, data, epochs=100):        
        self.data = data
        train_x, train_y = self._transform(data, fit=True)
        self.model.fit(train_x, train_y, epochs=epochs)

    def predict(self, days):
        products, _ = self._transform(self.data)
        products_predictions = []
        for product in products:
            product_predictions = []
            past_days = product[-1]
            for day in range(0, days):
                predicted = np.array(self.model.predict(past_days))
                predicted.resize(1, 1)
                predicted = self.scaler.inverse_transform(predicted)[0][0]
                product_predictions.append(predicted)
                past_days = np.append(past_days[1:, :], [np.insert(past_days[-1][1:], 0, predicted)], axis=0)
            products_predictions.append(product_predictions)
        products_predictions = np.array(products_predictions)
        return products_predictions.reshape((products_predictions.shape[1]))

    def _transform(self, data, fit=False):
        data = data[:1,:,:1]
        s0, s1, s2 = data.shape[0], data.shape[1], data.shape[2]
        if fit:
            data = self.scaler.fit_transform(data.reshape(s0*s1, s2)).reshape(s0, s1, s2)
            if data.shape[0] == 1:
                data = np.vstack((data, data))
        else:
            data = self.scaler.transform(data.reshape(s0*s1, s2)).reshape(s0, s1, s2)
        all_x, all_y = [], []
        for timeseries in data:
            x, y = [], []
            for i in range(len(timeseries) - self.model.look_back - 1):
                x.append(timeseries[i:(i + self.model.look_back), 0:])
                y.append(timeseries[i + self.model.look_back, :1])
            all_x.append(np.array(x))
            all_y.append(np.array(y))
        all_x = np.array(all_x)
        all_x = all_x[:,:,:,0].reshape((all_x.shape[0], all_x.shape[1], all_x.shape[2], 1))        
        return np.array(all_x), np.array(all_y).squeeze()
