import numpy as np
import pandas as pd
from scipy import stats
from src.data import load_raw, load_filtered, load_subtracted
from src.entropy import app_entropy
from src.entropy import sample_entropy
import matplotlib.pyplot as plt

def mean_filter(data, filter_points):
    filtered = []
    for i in range(len(data)):
        if i <= len(data)-filter_points:
            filtered.append(np.mean(np.array(data[i:i+filter_points])))
        else:
            filtered.append(np.mean(np.array(data[i:])))
    return filtered

def frequency_filter(data, fc=0.8, b=0.08):
    N = int(np.ceil((4 / b)))
    if N%2 != 0: 
        N += 1
    n = np.arange(N)
    sinc_func = np.sinc(2*fc*(n-(N-1)/2.))
    window = 0.42 - 0.5 * np.cos(2*np.pi*n / (N - 1)) + 0.08 * np.cos(4 * np.pi * n / (N - 1))
    sinc_func = sinc_func * window
    sinc_func = sinc_func / np.sum(sinc_func)
    return np.convolve(data, sinc_func)[int(N/2):-int(N/2)+1]

def moving_cumulant(data, filter_points):
    cumulant = []
    for i in range(len(data)):
        if i <= len(data)-filter_points:
            cumulant.append(stats.kstat(np.array(data[i:i+filter_points]), 4))
        else:
            cumulant.append(stats.kstat(np.array(data[i:]), 4))
    return cumulant

def entropy_analysis(original, subtracted, start, points):
    sample_order=3
    entropy, data = [], []
    dataframe = pd.DataFrame()
    for column in subtracted.columns:
        print(column)
        entropy.append(sample_entropy(np.array(original[column].values[start:points]), order=sample_order))
        data.append('No Filter')
        entropy.append(sample_entropy(mean_filter(np.array(original[column].values[start:points]), 2), order=sample_order))
        data.append('MAF - N=2')
        entropy.append(sample_entropy(mean_filter(np.array(original[column].values[start:points]), 3), order=sample_order))
        data.append('MAF - N=3')
        entropy.append(sample_entropy(mean_filter(np.array(original[column].values[start:points]), 4), order=sample_order))
        data.append('MAF - N=4')
        entropy.append(sample_entropy(mean_filter(np.array(original[column].values[start:points]), 5), order=sample_order))
        data.append('MAF - N=5')
        entropy.append(sample_entropy(frequency_filter(np.array(original[column].values[start:points]), fc=0.8), order=sample_order))
        data.append('FDF - fc=0.8')
        entropy.append(sample_entropy(frequency_filter(np.array(original[column].values[start:points]), fc=0.75), order=sample_order))
        data.append('FDF - fc=0.75')
        entropy.append(sample_entropy(np.array(subtracted[column].values[start:points]), order=sample_order))        
        data.append('Proposed Method')

    dataframe['Sample Entropy'] = entropy
    dataframe['Filter Type'] = data
    dataframe.to_csv('notebooks/entropy_{}.csv'.format(sample_order))

if __name__=='__main__':
    data = load_raw()
    subtracted = load_subtracted()
    start = 0
    points = 400
    entropy_analysis(data, subtracted, start, points)

