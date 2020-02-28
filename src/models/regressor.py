import os
import pandas as pd
import numpy as np
import keras 
from sklearn.externals import joblib
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense
from keras import backend as K 
path = os.path.join(os.path.dirname(__file__), '../../data/knowledge/regressor')

class Regressor:
    def __init__(self):
        self.model = Sequential()
        self.model.add(Dense(8, input_dim=2, activation='relu'))
        self.model.add(Dense(8, activation='relu'))
        self.model.add(Dense(1, activation='sigmoid'))
        self.model.compile(loss='mean_squared_error', optimizer='adam')
        self.scaler = MinMaxScaler()

    def fit(self, data):
        train_XY, train_Z = self.transform(data)
        self.fit_scaler(data)
        X = self.scaler.transform(train_XY[0].reshape((train_XY.shape[1], 1)))
        Y = self.scaler.transform(train_XY[1].reshape((train_XY.shape[1], 1)))
        Z = self.scaler.transform(train_Z.reshape((train_Z.shape[0], 1)))
        train = np.transpose([X, Y]).reshape((train_XY.shape[1], 2))
        self.model.fit(train, Z, epochs=5000, verbose=0)
        self.model.save_weights('{}/weights.h5'.format(path))

    def transform(self, data):
        train_X = np.array(data.drop(columns=['z']).values)
        train_Z = np.array(data['z'].values)
        train_XY = np.transpose(train_X)
        return train_XY, train_Z

    def fit_scaler(self, data):
        data_scaler = np.array([np.array(data.values).reshape((36*3))])
        data_scaler = data_scaler.reshape((108,1))
        self.scaler.fit(data_scaler)
        joblib.dump(self.scaler, '{}/scaler.pkl'.format(path)) 

    def load(self):
        self.scaler = joblib.load('{}/scaler.pkl'.format(path)) 
        self.model.load_weights('{}/weights.h5'.format(path))

    def predict(self, x, y):
        x = self.scaler.transform([[x]])
        y = self.scaler.transform([[y]])
        x_y = np.concatenate((x,y))
        z = np.transpose(x_y).reshape((1,2))
        prediction  = self.scaler.inverse_transform(self.model.predict(z)).reshape((1))[0]
        return prediction

    def __del__(self):
        K.clear_session()
