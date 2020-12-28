from datetime import datetime, timedelta
from app.models import *
import pandas as pd
from scipy import fftpack
import matplotlib.pyplot as plt
import numpy as np

def main():
    measures = Measure.query.filter(Measure.date>datetime.now()-timedelta(minutes=1)).order_by(Measure.id)
    data = {'acel_x': [],
            'acel_y': [],
            'acel_z': [],
            'rot_x': [],
            'rot_y': [],
            'rot_z': [],
            'temperature': [],
            }
    for measure in measures:
        data['acel_x'].append(measure.acel_x)
        data['acel_y'].append(measure.acel_y)
        data['acel_z'].append(measure.acel_z)
        data['rot_x'].append(measure.rot_x)
        data['rot_y'].append(measure.rot_y)
        data['rot_z'].append(measure.rot_z)
    for key in data.keys():
        outlier_anomaly, frequency_anomaly = anomaly_analysis(data[key])
        
        print(key)

def anomaly_analysis(data):
    dataframe = pd.DataFrame()
    dataframe['value'] = data
    Q1 = dataframe.quantile(0.25)
    Q3 = dataframe.quantile(0.75)
    IQR = Q3 - Q1
    df = dataframe[~((dataframe<(Q1-1.5*IQR))|(dataframe>(Q3+1.5*IQR))).any(axis=1)]
    if len(df) < len(dataframe):
        outlier_anomaly = True
    else:
        outlier_anomaly = False
    Data = fftpack.fft(data)
    f_s = 1/5
    freqs = fftpack.fftfreq(len(data))*(1/5)
    dataframe = pd.DataFrame()
    dataframe['freqs'] = freqs
    dataframe['magnitude'] = np.abs(Data)
    filtered = dataframe[dataframe['magnitude']>1]
    if len(filtered) > 2:
        frequency_anomaly = True
    elif len(filtered) == 1:
        if filtered['freqs'].values[0] == 0.0:
            frequency_anomaly = False
        else:
            frequency_anomaly = True
    else:
        frequency_anomaly = False
    return outlier_anomaly, frequency_anomaly


if __name__ == '__main__':
    main()
