from src.utils import cross_val_score, ensure_model_fitting
from multiprocessing import Pool
from functools import partial
import warnings
import numpy as np
import itertools
import multiprocessing


def grid_search(data, model, options, points_to_predict):
    warnings.filterwarnings("ignore")
    best_error, best_config = _execute_grid_search(data, model, options, points_to_predict)
    return best_error, best_config


def _execute_grid_search(data, model, options, points_to_predict):
    params = list(itertools.product(*list(options.values())))
    if model.__name__ in ['Prophet']:
        pool = Pool(multiprocessing.cpu_count())
        results = pool.map(partial(_cross_val_score, data=data, model=model, options=options, points_to_predict=points_to_predict), params)
        pool.close()
        pool.join()
    else:
        results = map(partial(_cross_val_score, data=data, model=model, options=options, points_to_predict=points_to_predict), params)
    best_error, best_config = list(sorted(list(results), key=lambda result: result[0]))[0]
    return best_error, best_config


def _cross_val_score(params, data, model, options, points_to_predict):
    error, config = float("inf"), None
    config = dict(zip([*options], params))
    current_model = model(**config)
    model_mse = cross_val_score(estimators=[current_model], data=data, points_to_predict=points_to_predict)[model.__name__]
    error = np.average(model_mse)
    return error, config
