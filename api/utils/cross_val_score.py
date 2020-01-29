import numpy as np
from sklearn.metrics import mean_squared_error, mean_absolute_error
from src.utils import ensure_model_fitting

def cross_val_score(estimators, data, points_to_predict):
    """
    Returns an dict with array of scores (RMSE) for each estimator (model)
    If data does not have sufficient products, excute without foldering
    Keyword arguments:
    estimators -- models that has fit and predict method
    data -- dataset
    points_to_predict -- how many days to predict and compare with the real value
    """
    models_rmses = dict.fromkeys([type(model).__name__ for model in estimators], [])
    for model in estimators:
        models_rmses[type(model).__name__].append(
                _handle_model(model, data, points_to_predict))
    return models_rmses


def _handle_model(model, data, points_to_predict):
    """
    Returns the RMSE for this input session using the model
    Keyword arguments:
    model -- model to be evaluated
    data -- pure data (products, timeserie)
    points_to_predict -- how many days to predict and compare with the real value
    """
    train_x = _create_train_dataset(data, points_to_predict)
    _, test_y = _create_test_dataset(data, points_to_predict)
    with ensure_model_fitting():
        model.fit(train_x)
        predictions = model.predict(points_to_predict)
        return _bucket_rmse(predictions=predictions, test_y=test_y)
    return float('inf')

def _create_train_dataset(data, points_to_predict):
    """
    Returns the train products for the given train fold
    Keyword arguments:
    data -- pure data (products, timeserie)
    points_to_predict -- how many days to predict and compare with the real value
    """
    return np.array(data[:, :-points_to_predict, :])


def _create_test_dataset(data, points_to_predict):
    """
    Returns the test_x and test_y products for the given test fold
    Keyword arguments:
    data -- pure data (products, timeserie)
    points_to_predict -- how many days should be considered for y(real output)
    """
    x = data[:, -points_to_predict:, :]
    y = data[:, -points_to_predict:, :1]
    return np.array(x), np.array(y)


def _bucket_rmse(predictions, test_y):
    """
    Returns a tuple containing the average of Root Mean Squared Errors from the products,
    and a array with every product RMSE, but represented in percentage.
    Keyword arguments:
    predictions -- an array of products predictions with their predictions
                   (every product should have n predictions)
    test_y -- an array of products with their respective real values
    """
    return mean_squared_error(y_true=test_y.reshape(test_y.shape[1]), y_pred=predictions)
