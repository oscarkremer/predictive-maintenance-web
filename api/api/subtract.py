import os
import re
import pandas as pd
import numpy as np
import argparse
import warnings
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error
from src.models import LSTM, SARIMA, XGB, Prophet, ND
from src.utils import log, log_time, path, ensure_model_fitting, populate_dict
from src.data import load_raw, load_analysis
from src.features import process_features
from src.utils.cross_val_score import _create_test_dataset, _create_train_dataset

warnings.simplefilter('ignore')

def main(start_point, end_point, points_to_model):
    i = 0
    data = load_raw()
    subtracted = pd.DataFrame()
    for column in data.columns:
        models = [SARIMA(p=0, q=0, d=0, P=3, Q=0, D=3, m=2)]
        features = process_features(data[column], start_point, end_point)
        log('Predictions for trace - {0} '.format(column))
        predicted = predict(np.array([features.values]), models, len(data[column].values)-end_point+start_point, points_to_model)
        real = np.flip(np.array(data[column].values))
        zeros = np.zeros(end_point-start_point - points_to_model)
        sub = real[end_point - points_to_model:] - predicted
        subtracted[column] = np.flip(np.concatenate((zeros, sub)))
    subtracted.to_csv('data/predicted/subtraction/subtracted.csv', index=False)
    subtracted.to_csv('notebooks/subtracted.csv', index=False)

def remove_predictions():
    for filename in os.listdir('{0}/subtraction'.format(path.predicted)):
        os.remove('{0}/subtraction/{1}'.format(path.predicted, filename))

def predict(trace, models, points_to_predict, points_to_model):
    log('Predicting  - for ' + str(points_to_predict))
    train_x = _create_train_dataset(trace, points_to_model)
    predictions, error = [], []
    for model in models:
        if model is not None:
            model.fit(train_x)
            predictions.append(model.predict(points_to_predict + points_to_model))
            error.append(model.error)

    if predictions:
        weights = [1.0] if len(error) == 1 else np.ones(len(error)) - (np.array(error) / np.array(error).sum())
        predictions = np.nan_to_num(predictions) 
        predicted = [*map(float, np.average(predictions.reshape(predictions.shape[0], points_to_predict+points_to_model), axis=0, weights=weights))]
        return predicted    

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--points-to-model', default=15, type=int)
    parser.add_argument('--start-point', default=0, type=int)
    parser.add_argument('--end-point', default=90, type=int)
    args = parser.parse_args()
    with log_time('Predicting'):
        main(args.start_point, args.end_point, args.points_to_model)
