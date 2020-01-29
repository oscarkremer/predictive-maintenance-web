import os
import random
import pandas as pd
import numpy as np
from src.data import load_raw
from src.utils import path

def main(dataset_size):
    remove_dataset()
    data = load_raw()
    modelling_dataset = pd.DataFrame()
    data_columns = list(data.columns)
    random.shuffle(data_columns)
    for column in data_columns:
        modelling_dataset[column] = data[column]
        if len(modelling_dataset.columns) >= dataset_size:
            break
    modelling_dataset.to_csv('data/analysis/train.csv', index=False)

def remove_dataset():
    for filename in os.listdir('data/test'):
        os.remove('data/test/{1}'.format(path.predicted, filename))

if __name__ == "__main__":
    main(1000)
