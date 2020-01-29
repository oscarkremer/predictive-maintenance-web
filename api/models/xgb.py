import xgboost as xgb
import numpy as np
from .model_template import ModelTemplate
from src.utils import processing_device

class XGB(ModelTemplate):
    def __init__(self, learning_rate=0.1, n_estimators=140, max_depth=5, min_child_weight=1, tree_method=processing_device['xgboost']):
        self.model = xgb.XGBRegressor(
            learning_rate=learning_rate,
            n_estimators=n_estimators,
            max_depth=max_depth,
            min_child_weight=min_child_weight,
            tree_method=tree_method)
        self.learning_rate = learning_rate
        self.n_estimators = n_estimators
        self.max_depth = max_depth
        self.min_child_weight= min_child_weight
        self.error = float('inf')

    def fit(self, data, **args):
        self.data = data
        train_x, train_y = self._transform()
        train_x = train_x.reshape(-1, train_x.shape[-1])
        train_y = train_y.reshape(-1, 1)
        self.model.fit(train_x, train_y)

    def predict(self, days):
        values, _ = self._transform()
        predictions = []
        for value in values:
            prediction = []
            past_days = value[-1].copy()
            past_days = np.expand_dims(past_days, axis=0)
            for day in range(days):
                predicted = np.array(self.model.predict(past_days))
                prediction.append(predicted)
                past_days = np.array([np.insert(past_days[:, 1:], 0, predicted)])
            predictions.append(prediction)
        return np.array(predictions).reshape((days))

    def _transform(self):
        all_x, all_y = [], []
        for timeseries in self.data:
            x, y = [], []
            for i in range(len(timeseries) - 1):
                x.append(timeseries[i, :])
                y.append(timeseries[i + 1, :1])
            all_x.append(np.array(x))
            all_y.append(np.array(y))
        return np.array(all_x), np.array(all_y)
