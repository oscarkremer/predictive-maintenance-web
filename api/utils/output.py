import numpy as np


def populate_dict(points_to_predict, predict=False):
    results = {}
    models = ['lstm' ,'nd', 'prophet', 'xgb']
    for model in models:
        results[model] = np.zeros(points_to_predict)
        if not predict:
            results['error - ' + model] = np.zeros(points_to_predict)
    return results