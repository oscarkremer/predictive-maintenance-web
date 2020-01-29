import os
import pandas as pd
import numpy as np
import argparse
from src.utils import log, log_time
from src.data import load_raw


def main(filter_points):
    remove_filtered()
    data = load_raw()
    filtered = pd.DataFrame()
    for column in data.columns:
        filtered[column] = mean_filter(data[column].values, 3)
    filtered.to_csv('data/processed/test.csv', index=False)


def remove_filtered():
    for filename in os.listdir('data/processed'):
        os.remove('data/processed/{}'.format(filename))


def mean_filter(data, filter_points):
    filtered = []
    for i in range(len(data)):
        if i <= len(data)-filter_points:
            filtered.append(np.mean(np.array(data[i:i+filter_points])))
        else:
            filtered.append(np.mean(np.array(data[i:])))
    return filtered


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--filter-points', default=3, type=int)
    args = parser.parse_args()
    with log_time(' Moving Average Filter '):
        main(args.filter_points)
