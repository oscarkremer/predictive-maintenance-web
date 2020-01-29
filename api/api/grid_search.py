import os
import numpy as np
import argparse
import time
import pandas as pd
from sklearn.metrics import mean_squared_error
from src.data import load_analysis
from src.features import process_features
from src.models import LSTM, SARIMA, XGB, Prophet, ND
from src.utils import log, log_time, grid_search, path, populate_dict
from src.utils.cross_val_score import _create_test_dataset, _create_train_dataset
from src.utils.plotter import plot, plot_timeseries

def main(points, train, step):

    remove_datasets()
    data = load_analysis()
    columns_to_process = 5
    for j, column in enumerate(data.columns):
        filename = '{}'.format(column)
        for i in range(int((points-train)/step)):
            features = process_features(data[column], 0, train + i*step)
            log('Running grid search for POC - trace - {} '.format(column))
            save_best_models(np.array([features.values]), filename, step)
            models = [SARIMA.load(filename), LSTM.load(filename), ND.load(filename), Prophet.load(filename), XGB.load(filename)]
            if check_emptyness(models):
                features = process_features(data[column], 0, train + (i+1)*step)
                log('Evaluations for POC - trace - {} '.format(column))
                evaluate(np.array([features.values]), models, step, train+(i+1)*step, filename)
        data=data.drop(columns=[column])
        if j >= columns_to_process-1:
            break
    data.to_csv('data/analysis/train.csv', index=False)
        

def check_emptyness(models):
    i = 0
    for model in models:
        if model is None:
            i+=1
    if i==5:
        return False 
    else:
        return True

def remove_datasets():
    for filename in os.listdir('{0}/evaluation'.format(path.predicted)):
        os.remove('{0}/evaluation/{1}'.format(path.predicted, filename))

    for filename in os.listdir('data/plots/evaluation'):
        os.remove('data/plots/evaluation/{0}'.format(filename))

    for filename in os.listdir('{0}/grid_search'.format(path.predicted)):
        os.remove('{0}/grid_search/{1}'.format(path.predicted, filename))

def evaluate(data, models, points_to_predict, points_train, filename):
    train_x = _create_train_dataset(data, points_to_predict)
    _, test_y = _create_test_dataset(data, points_to_predict)
    error, predictions, legends = [], [], []
    results = pd.DataFrame()
    results['trace'] = [filename]
    results['points'] = [points_train]
    legends.append('real-DES')
    for model in models:
        if model is not None:
            if model.name == 'nd':
                model.model.n_data = model.model.n_data + points_to_predict
            start_time = time.time()
            model.fit(train_x)
            prediction = model.predict(points_to_predict)
            results['time-' + model.name] = [time.time()-start_time]
            results['error-' + model.name] =  [mean_squared_error(y_true=test_y.reshape(test_y.shape[1]), y_pred=prediction)]
            legends.append(model.name)
            predictions.append(prediction)
            error.append(model.error)
            log('Evaluations for POC - model - {0} - error - {1} '.format(model.name, results['error-' + model.name].values[0]))
            plot(data[:,:, 0].reshape(-1), prediction, points_to_predict, model.name , "/evaluation/{}_{}_{}".format(points_train, model.name, filename))
    plot_timeseries(data[:, :, 0].reshape(-1), predictions, points_to_predict, legends, "/evaluation/{0}_{1}".format(points_train, filename))
    
    predictions = pd.DataFrame(results, columns = results.keys())
    if os.path.isfile('{0}/evaluation/validation.csv'.format(path.predicted)):
        predictions.to_csv('{0}/evaluation/validation.csv'.format(path.predicted), mode='a', index=False, header=False)
    else:
        predictions.to_csv('{0}/evaluation/validation.csv'.format(path.predicted), mode='w', index=False)
           
def save_best_models(data, filename, points_to_model):
    if data.shape[0] == 0:
        return
    grid_models = [        
#    {'model': ND, 'options': {'data_size': [data.shape[1]-points_to_model], 'units': [1], 'epochs': [200], 'forecast_length': [points_to_model], 
#       'L1_reg': [0.1, 0.05, 0.01], 'validation_length': [1], 'batch_size': [2]}},
    {'model': SARIMA, 'options': {'p': [0], 'd': [0], 'q': [0], 'P': [2], 'D': [1], 'Q': [2], 'm':[2]}}
#    {'model': LSTM, 'options': {'look_back': [3, 5, 9], 'hidden_size': [8, 16, 32], 'num_layers': [1, 2]}},
#    {'model': Prophet, 'options': {'yearly_seasonality': list(range(15, 30)), 'trending': [False],  'seasonality_mode': ['additive']}},
#    {'model': XGB, 'options': {'learning_rate': [0.01, 0.001, 0.1, 0.3, 0.4], 'n_estimators': [5, 10, 15, 20, 50, 75], 
#        'max_depth': [5, 10, 15, 20, 50, 75], 'min_child_weight': [5, 10, 15, 20, 50, 75]}}
    ]
    for grid_model in grid_models:
        log('Running grid search for ' + str(grid_model['model'].__name__))
        log('Checking best ' + str(grid_model['model'].__name__) + ' hyper-params')
        error, config = grid_search(model=grid_model['model'], options=grid_model['options'], data=data, points_to_predict=points_to_model)
        log('Best Config is: ' + str(config) + ' with RMSE: ' + str(error))
        if error != float('inf'):
            best_model = grid_model['model'](**config)
            best_model.error = error
            best_model.save(filename)
            df = pd.DataFrame()
            df['trace'] = [filename]
            df['error'] = [best_model.error]
            df['points_used'] = [data.shape[1]-points_to_model]

            if grid_model['model'].__name__=='ND':
                df['data_size'] = [best_model.data_size]
                df['units'] = [best_model.units]
                df['L1_reg'] = [best_model.L1_reg]
                df['batch_size'] = [best_model.batch_size]
                
            if grid_model['model'].__name__=='SARIMA':
                df['p'] = [best_model.p]
                df['q'] = [best_model.q]
                df['d'] = [best_model.d]
                df['P'] = [best_model.P]
                df['Q'] = [best_model.Q]
                df['D'] = [best_model.D]
                df['m'] = [best_model.m]
                
            if grid_model['model'].__name__=='LSTM':
                df['look_back'] = [best_model.look_back]
                df['hidden_size'] = [best_model.hidden_size]
                df['num_layers'] = [best_model.num_layers]
            
            if grid_model['model'].__name__=='Prophet':
                df['yearly_seasonality'] = [best_model.yearly_seasonality]
                df['trending'] = [best_model.trending]
                df['seasonality_mode'] = [best_model.seasonality_mode]
            
            if grid_model['model'].__name__=='XGB':
                df['learning_rate'] = [best_model.learning_rate]
                df['n_estimators'] = [best_model.n_estimators]
                df['max_depth'] = [best_model.max_depth]
                df['min_child_weight'] = [best_model.min_child_weight]
            
            if os.path.isfile('{0}/grid_search/{1}.csv'.format(path.predicted, grid_model['model'].__name__)):
                df.to_csv('{0}/grid_search/{1}.csv'.format(path.predicted, grid_model['model'].__name__), mode='a', index=False, header=False)
            else:
                df.to_csv('{0}/grid_search/{1}.csv'.format(path.predicted, grid_model['model'].__name__), mode='w', index=False)
         
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--start-point', default=0, type=int)
    parser.add_argument('--end-point', default=100, type=int)
    parser.add_argument('--points-to-model', default=60, type=int)
    parser.add_argument('--dataset', default='poc', type=str)
    args = parser.parse_args()
    points = 100
    train = 40
    step = 20
    with log_time('grid searching'):
        main(points, train, step)
