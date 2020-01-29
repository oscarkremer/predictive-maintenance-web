import os
import random
import pandas as pd
import numpy as np
from src.data import load_raw
from src.utils import path

def main():
    i = 1
    predictions = pd.DataFrame()
    prediction_path = 'data/predicted/prediction'
    for filename in os.listdir(prediction_path):
        df = pd.read_csv('{0}/{1}'.format(prediction_path, filename))
        for column in df.columns:
            predictions[column] = df[column]
            print(i)
            i+=1
    predictions.to_csv('data/predicted.csv', index=False)

if __name__ == "__main__":
    main()
