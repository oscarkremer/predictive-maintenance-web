import cv2
import numpy as np
import os
import sys
from random import shuffle, randint
from tqdm import tqdm
ALEX_NET = 227
LIMIT = 15000

def create_label(image_name, label):
    result = np.identity(len(label), dtype=float)
    word_label = image_name.split('.')[-3]
    for i in range(len(label)):
        if word_label == label[i]:
            return result[i]

def break_data(data, names, parts=3):
    splited_data, splited_names = [], []
    size = int(data.shape[0]/parts)
    for i in range(parts):
        if i == parts - 1:
            splited_data.append(data[i*size:])
            splited_names.append(names[i*size:])
        else:
            splited_data.append(data[i*size:(i+1)*size])
            splited_names.append(names[i*size:(i+1)*size])
    return splited_data, splited_names


def train_data(folder_path, save_path, label, save=True):
    train_data = []
    for img in tqdm(os.listdir(folder_path)):
        path = os.path.join(folder_path, img)
        img_data = cv2.imread(path)
        train_data.append([np.array(img_data), create_label(img, label)])
    shuffle(train_data)
    if len(os.listdir(folder_path)) > LIMIT:
        train_data = train_data[0:LIMIT]
    if save:
        np.save(save_path, train_data)
    return train_data


def input_data(folder_path, save_path, save=False):
    input_data = []
    for img in tqdm(os.listdir(folder_path)):
        path = os.path.join(folder_path, img)
        img_num = img.split('.')[0]
        img_data = cv2.imread(path)
        input_data.append([np.array(img_data), img_num])
    if save:
        np.save(save_path + '/processed', input_data)
    for i in range(len(input_data)):
        input_data[i][0] = cv2.resize(input_data[i][0], (ALEX_NET, ALEX_NET))
    dataX = np.array([i[0] for i in input_data]
                     ).reshape(-1, ALEX_NET, ALEX_NET, 3)
    dataY = np.array([i[1] for i in input_data])
    return dataX, dataY


def load_data(path):
    data = np.load(path + '.npy')
    for i in range(len(data)):
        data[i][0] = cv2.resize(data[i][0], (ALEX_NET, ALEX_NET))
    dataX = np.array([i[0] for i in data]).reshape(-1, ALEX_NET, ALEX_NET, 3)
    dataY = np.array([i[1] for i in data])
    return dataX, dataY
