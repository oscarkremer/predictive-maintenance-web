import os
import numpy as np
import fbprophet as fbp
from .model_template import ModelTemplate
from pandas import DataFrame
import datetime


class Prophet(ModelTemplate):

    def __init__(self, n_changepoints=25, changepoint_range=0.8,
                 yearly_seasonality=100, weekly_seasonality="auto",
                 daily_seasonality="auto", seasonality_mode="additive",
                 seasonality_prior_scale=0.05, trending = True, verbose=False):

        self.model_config = {
            "n_changepoints": n_changepoints,
            "changepoint_range": changepoint_range,
            "yearly_seasonality": yearly_seasonality,
            "weekly_seasonality": weekly_seasonality,
            "daily_seasonality": daily_seasonality,
            "seasonality_mode": seasonality_mode,
            "seasonality_prior_scale": seasonality_prior_scale,
        }
        self.yearly_seasonality = yearly_seasonality
        self.seasonality_mode = seasonality_mode
        self.trending = trending
        self.verbose = verbose
        self.error = float('inf')

    def __get_date_interval__(self, days):
        def new_day(i): return datetime.datetime.now() + datetime.timedelta(i)
        day_list = [new_day(i).isoformat()[0:10] for i in range(days)]
        return day_list

    def fit(self, data):
        self.data = data
        pass

    def predict(self, days):
        def __predict__(days):
            values = self._transform(self.data)
            bucket_predictions = []
            for value in values:
                history = np.reshape(list(value.copy()), -1, 1)
                dataframe = DataFrame(value, columns=['y'])
                dataframe['ds'] = self.__get_date_interval__(len(history))
                dataframe['floor'] = 0
                model = fbp.Prophet(**self.model_config)
                model.fit(dataframe)
                future = model.make_future_dataframe(periods=days)
                forecast = model.predict(future)
                if self.trending:
                    result = np.array(forecast['yhat'][-days:].values)
                else:
                    result = np.array(forecast['yhat'][-days:].values - forecast['trend'][-days:].values)      
                bucket_predictions.append(result)
            return np.array(bucket_predictions).reshape((days))
        if self.verbose:
            return __predict__(days)
        else:
            with suppress_stdout_stderr():
                return __predict__(days)

    def _transform(self, data, days=0):
        all_x = data[:1,:,:1]
        return np.array(all_x)


class suppress_stdout_stderr(object):
    def __init__(self):
        self.null_fds = [os.open(os.devnull, os.O_RDWR) for x in range(2)]
        self.save_fds = [os.dup(1), os.dup(2)]

    def __enter__(self):
        os.dup2(self.null_fds[0], 1)
        os.dup2(self.null_fds[1], 2)

    def __exit__(self, *_):
        os.dup2(self.save_fds[0], 1)
        os.dup2(self.save_fds[1], 2)
        for fd in self.null_fds + self.save_fds:
            os.close(fd)
