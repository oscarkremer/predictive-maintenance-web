import os
import pandas as pd
import numpy as np
import scipy.io as sio
from src.utils import log, log_time, path, ensure_model_fitting, populate_dict
from src.data import load_subtracted

def main():
    subtracted = load_subtracted()
    for column in subtracted.columns:
        sub = np.array(subtracted[column].values)
        noise = np.random.normal(np.mean(sub[:30]), 0.5*np.std(sub[:30]), 75)
        signal = (np.concatenate((sub[:-75], noise)))
        log('Saving trace - {0} '.format(column))
        sio.savemat('data/traces/traces_DES_{}.mat'.format(column), {'trace':signal})

if __name__ == "__main__":
    with log_time('Passing subtracted information to .mat file format'):
        main()
