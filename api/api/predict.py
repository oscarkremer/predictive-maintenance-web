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
from src.data import load_poc_attack, load_poc
from src.features import process_features
from src.utils.cross_val_score import _create_test_dataset, _create_train_dataset

warnings.simplefilter('ignore')

def main(start_point, end_point, points_to_model, label):
    remove_predictions()
    if label == 'poc':
        data = load_poc()
    else:
        data = load_poc_attack()
    predictions = pd.DataFrame()
    for column in data.columns:
        filename = '{}'.format(label)
        models = [LSTM.load(filename), ND.load(filename), Prophet.load(filename), XGB.load(filename)]
        features = process_features(data[column], start_point, end_point)
        log('Predictions for {0} - trace - {1} '.format(label, column))
        predicted = predict(np.array([features.values]), models, len(data[column].values) - end_point + start_point, points_to_model)
        real = np.flip(np.array(data[column].values))
        zeros = np.zeros(end_point - start_point - points_to_model)
        predictions[column] = np.flip(np.concatenate((zeros, predicted)))
        plt.plot(predictions[column].values)
        plt.savefig('{0}/prediction/{1}_{2}.png'.format(path.plots, label, column), transparent=False)
        plt.clf()
    predictions.to_csv('{0}/prediction/{1}.csv'.format(path.predicted, label))


def remove_predictions():
    for filename in os.listdir('{0}/prediction'.format(path.predicted)):
        os.remove('{0}/prediction/{1}'.format(path.predicted, filename))


def predict(trace, models, points_to_predict, points_to_model):
    train_x = _create_train_dataset(trace, points_to_model)
    predictions = []
    error = []
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
    parser.add_argument('--points-to-model', default=6, type=int)
    parser.add_argument('--start-point', default=0, type=int)
    parser.add_argument('--end-point', default=100, type=int)
    parser.add_argument('--dataset', default='poc', type=str)
    args = parser.parse_args()
    with log_time('Predicting'):
        main(args.start_point, args.end_point, args.points_to_model, args.dataset)
