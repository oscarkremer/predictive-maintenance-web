import os
import re
import pandas as pd
import numpy as np
import argparse
import warnings
from sklearn.metrics import mean_squared_error
from src.models import LSTM, XGB, Prophet, ND
from src.utils import log, path, plot_timeseries, ensure_model_fitting, populate_dict
from src.data import load_poc, load_poc_attack
from src.utils.cross_val_score import _create_test_dataset, _create_train_dataset
from src.features import process_features

warnings.simplefilter('ignore')


def main(start_point, end_point, points_to_predict, label):
    remove_evaluations()
    if label == 'poc':
        data = load_poc()
    else:
        data = load_poc_attack()
    for column in data.columns:
        filename = '{}'.format(label)
        models = [LSTM.load(filename), ND.load(filename), Prophet.load(filename), XGB.load(filename)]
        if check_emptyness(models):
            features = process_features(data[column], start_point, end_point)
            log('Evaluations for {0} - trace - {1} '.format(label, column))
            evaluate(np.array([features.values]), models, points_to_predict, '{}_{}'.format(label,column))

def check_emptyness(models):
    i = 0
    for model in models:
        if model is None:
            i+=1
    if i==4:
        return False 
    else:
        return True
    

def remove_evaluations():
    for filename in os.listdir('{0}/evaluation'.format(path.predicted)):
        os.remove('{0}/evaluation/{1}'.format(path.predicted, filename))


def evaluate(data, models, points_to_predict, filename):
    train_x = _create_train_dataset(data, points_to_predict)
    _, test_y = _create_test_dataset(data, points_to_predict)
    predictions = []
    error = []
    results = populate_dict(points_to_predict)
    for model in models:
        if model is not None:
            print(train_x)
            model.fit(train_x)
            prediction = model.predict(points_to_predict)
            results[model.name] = prediction
            results['error - ' + model.name] = model.error
            predictions.append(prediction)
            error.append(model.error)
            plot_timeseries(data[:, :, 0].reshape(-1), prediction, "/evaluation/{0}_{1}".format(model.name, filename))
    if predictions:
        weights = [1.0] if len(error) == 1 else np.ones(len(error)) - (np.array(error) / np.array(error).sum())
        predictions = np.nan_to_num(predictions)
        predicted = [*map(float, np.average(predictions.reshape(predictions.shape[0], points_to_predict), axis=0, weights=weights))]
        real = [*map(float, test_y.reshape(-1))]
        results['real'] = real
        results['predicted'] = predicted
        results['error'] = np.sqrt(mean_squared_error(y_true=real, y_pred=predicted))        
        plot_timeseries(data[:, :, 0].reshape(-1), predicted, "/evaluation/{0}_{1}".format('full', filename))
        predictions = pd.DataFrame(results, columns = results.keys())
        if os.path.isfile(path.predicted + 'evaluated.csv'):
            predictions.to_csv('{0}/evaluation/{1}.csv'.format(path.predicted, filename), mode='a', index=False, header=False)
        else:
            predictions.to_csv('{0}/evaluation/{1}.csv'.format(path.predicted, filename), mode='w', index=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--start-point', default=6, type=int)
    parser.add_argument('--end-point', default=6, type=int)
    parser.add_argument('--points-to-model', default=6, type=int)
    parser.add_argument('--dataset', default='poc', choices=['poc', 'poc_attack'])
    args = parser.parse_args()
    main(args.start_point, args.end_point, args.points_to_model, args.dataset)
