import os
import re
import pandas as pd
import numpy as np
import argparse
import warnings
from sklearn.metrics import mean_squared_error
from src.models import NN
from src.utils import log, path, plot_timeseries, ensure_model_fitting, populate_dict
from src.data import load_test
from src.utils.cross_val_score import _create_test_dataset, _create_train_dataset
from src.features import process_features

warnings.simplefilter('ignore')


def main(start_point, end_point, points_to_predict, label):
    data = load_test()
    column = data.columns[0]
    mean_4 = []
    window = 10
    des = data[column].values
    for i in range(len(des)):
        if i + window <= len(des)-1:
            mean_4.append(np.std(des[i:i+window]))
        else:
            mean_4.append(0)
    filtered = []
    trainX, trainY = [], []
    sensibility = 0.17
    k= 0
    for i, point in enumerate(mean_4):
        if point > sensibility:
            filtered.append(0)
        else:
            k+=1
            filtered.append(des[i])
            trainX.append(i)
            trainY.append(des[i])

    model = NN(data_size=len(trainX), validation_length=5)
    model.fit(np.array(trainX), np.array(trainY))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--start-point', default=6, type=int)
    parser.add_argument('--end-point', default=6, type=int)
    parser.add_argument('--points-to-model', default=6, type=int)
    parser.add_argument('--dataset', default='poc', choices=['poc', 'poc_attack'])
    args = parser.parse_args()
    main(args.start_point, args.end_point, args.points_to_model, args.dataset)
