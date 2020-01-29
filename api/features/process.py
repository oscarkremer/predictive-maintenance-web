import os
import datetime
import itertools
import pandas as pd
import numpy as np
import multiprocessing as mp
from src.utils import path, log
import matplotlib.pyplot as plt

    
def process_features(data, start_point, end_point):
    des = pd.DataFrame()
    des['points'] = np.array(list(range(0, len(data.values), 1)))
    des['value'] = np.flip(np.array(data.values))
    df = create_timeseries(des, start_point, end_point)
    return df

def create_timeseries(des, start_point, end_point):
    features = []
    points = np.array(list(range(start_point, end_point, 1)))   
    for point in points:
        current_des = des.loc[(des['points'] == point)]
        past_des = des.loc[(des['points'] <= point)]
        last_des = des.loc[des['points'] == (point - 1)]
        
        value, mean, median, z_score, des_max, des_min, mode, delta = 0, 0, 0, 0, 0, 0, 0, 0

        if len(current_des) > 1:
            log('Error! Found more than 1 sales for this product')

        if len(current_des) and len(past_des):
            mean = past_des['value'].mean()
            std = past_des['value'].std()
            median = past_des['value'].median()
            des_max = past_des['value'].max()
            des_min = past_des['value'].min()
            des_mode = past_des['value'].mode()
            mode  = des_mode[0]
            des_mean = past_des['value'].mean()
            if abs(std) > 0.0001:
                z_score = (current_des.iloc[0]['value'] - mean) / std
            else:
                z_score = 0
           
        if len(current_des) and len(last_des):
            delta = current_des.iloc[0]['value'] - last_des.iloc[0]['value']

        if len(current_des):
            value = current_des.iloc[0]['value']

        features.append([value, mean, median, z_score, des_max, des_min, mode, delta])

    return pd.DataFrame(
        features,
        columns=['value', 'mean', 'median', 'z_score', 'des_max', 'des_min', 'mode', 'delta'])
