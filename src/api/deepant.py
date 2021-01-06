import numpy as np
import pandas as pd
import torch
from sklearn.preprocessing import MinMaxScaler
import time
import datetime
import os
from app.models import *
from datetime import timedelta, datetime

def read_modulate_data(data_file):
    """
        Data ingestion : Function to read and formulate the data
    """
    print('here')
    measures = Measure.query.filter(Measure.date>datetime.now()-timedelta(days=1)).order_by(Measure.id)
    rot_x = []
    rot_y = []
    rot_z = []
    acel_x = []
    acel_y = []
    acel_z = []
    temperature= []
    down_acel_x = []
    upper_acel_x = []
    down_acel_y = []
    upper_acel_y = []
    down_acel_z = []
    upper_acel_z = []
    down_rot_x = []
    upper_rot_x = []
    down_rot_y = []
    upper_rot_y = []
    down_rot_z = []
    upper_rot_z = []
    down_temperature = []
    upper_temperature = []
    dates = []
    for index, measure in enumerate(measures):
        print(index)
        rot_x.append(measure.rot_x)
        rot_y.append(measure.rot_y)
        rot_z.append(measure.rot_z)
        acel_x.append(measure.acel_x)
        acel_y.append(measure.acel_y)
        acel_z.append(measure.acel_z)
        down_acel_x.append(measure.down_acel_x)
        upper_acel_x.append(measure.upper_acel_x)
        down_acel_y.append(measure.down_acel_y)
        upper_acel_y.append(measure.upper_acel_y)
        down_acel_z.append(measure.down_acel_z)
        upper_acel_z.append(measure.upper_acel_z)
        down_rot_x.append(measure.down_rot_x)
        upper_rot_x.append(measure.upper_rot_x)
        down_rot_y.append(measure.down_rot_y)
        upper_rot_y.append(measure.upper_rot_y)
        down_rot_z.append(measure.down_rot_z)
        upper_rot_z.append(measure.upper_rot_z)
        down_temperature.append(measure.down_temperature)
        upper_temperature.append(measure.upper_temperature)
        temperature.append(measure.temperature)
        dates.append(measure.date)
    print('finished')
    data = pd.DataFrame()
    data['LOCAL_DATE'] = dates
    data['rot_x'] = rot_x
    data['rot_y'] = rot_y
    data['rot_Z'] = rot_z
    data['acel_x'] = acel_x
    data['acel_y'] = acel_y
    data['acel_z'] = acel_z
    print('finished1')
    data['down_acel_x'] = down_acel_x
    data['upper_acel_x'] = upper_acel_x
    data['down_acel_y'] = down_acel_y
    data['upper_acel_y'] = upper_acel_y
    print('finished2')
    data['down_acel_z'] = down_acel_z
    data['upper_acel_z'] = upper_acel_z
    print('finished3')
    data['down_rot_x'] = down_rot_x
    data['upper_rot_x'] = upper_rot_x
    data['down_rot_y'] = down_rot_y
    data['upper_rot_y'] = upper_rot_y
    data['down_rot_z'] = down_rot_z  
    data['upper_rot_z'] = upper_rot_z
    print('finished4')
    data['down_temperature'] = down_temperature
    data['upper_temperature'] = upper_temperature
    print('finished5')
    data['temperature'] = temperature
    data.set_index("LOCAL_DATE", inplace=True)
    return data


def data_pre_processing(df):
    """
        Data pre-processing : Function to create data for Model
    """
    try:
        scaled_data = MinMaxScaler(feature_range = (0, 1))
        data_scaled_ = scaled_data.fit_transform(df)
        df.loc[:,:] = data_scaled_
        _data_ = df.to_numpy(copy=True)
        X = np.zeros(shape=(df.shape[0]-LOOKBACK_SIZE,LOOKBACK_SIZE,df.shape[1]))
        Y = np.zeros(shape=(df.shape[0]-LOOKBACK_SIZE,df.shape[1]))
        timesteps = []
        for i in range(LOOKBACK_SIZE-1, df.shape[0]-1):
            timesteps.append(df.index[i])
            Y[i-LOOKBACK_SIZE+1] = _data_[i+1]
            for j in range(i-LOOKBACK_SIZE+1, i+1):
                X[i-LOOKBACK_SIZE+1][LOOKBACK_SIZE-1-i+j] = _data_[j]
        return X,Y,timesteps
    except Exception as e:
        print("Error while performing data pre-processing : {0}".format(e))
        return None, None, None

class DeepAnT(torch.nn.Module):
    """
        Model : Class for DeepAnT model
    """
    def __init__(self, LOOKBACK_SIZE, DIMENSION):
        super(DeepAnT, self).__init__()
        self.conv1d_1_layer = torch.nn.Conv1d(in_channels=LOOKBACK_SIZE, out_channels=16, kernel_size=3)
        self.relu_1_layer = torch.nn.ReLU()
        self.maxpooling_1_layer = torch.nn.MaxPool1d(kernel_size=2)
        self.conv1d_2_layer = torch.nn.Conv1d(in_channels=16, out_channels=16, kernel_size=3)
        self.relu_2_layer = torch.nn.ReLU()
        self.maxpooling_2_layer = torch.nn.MaxPool1d(kernel_size=2)
        self.flatten_layer = torch.nn.Flatten()
        self.dense_1_layer = torch.nn.Linear(48, 40)
        self.relu_3_layer = torch.nn.ReLU()
        self.dropout_layer = torch.nn.Dropout(p=0.25)
        self.dense_2_layer = torch.nn.Linear(40, DIMENSION)
        
    def forward(self, x):
        x = self.conv1d_1_layer(x)
        x = self.relu_1_layer(x)
        x = self.maxpooling_1_layer(x)
        x = self.conv1d_2_layer(x)
        x = self.relu_2_layer(x)
        x = self.maxpooling_2_layer(x)
        x = self.flatten_layer(x)
        x = self.dense_1_layer(x)
        x = self.relu_3_layer(x)
        x = self.dropout_layer(x)
        return self.dense_2_layer(x)

class LSTMAE(torch.nn.Module):
    """
        Model : Class for LSTMAE model
    """
    def __init__(self, LOOKBACK_SIZE, DIMENSION):
        super(LSTMAE, self).__init__()
        self.lstm_1_layer = torch.nn.LSTM(DIMENSION, 128, 1)
        self.dropout_1_layer = torch.nn.Dropout(p=0.2)
        self.lstm_2_layer = torch.nn.LSTM(128, 64, 1)
        self.dropout_2_layer = torch.nn.Dropout(p=0.2)
        self.lstm_3_layer = torch.nn.LSTM(64, 64, 1)
        self.dropout_3_layer = torch.nn.Dropout(p=0.2)
        self.lstm_4_layer = torch.nn.LSTM(64, 128, 1)
        self.dropout_4_layer = torch.nn.Dropout(p=0.2)
        self.linear_layer = torch.nn.Linear(128, DIMENSION)
        
    def forward(self, x):
        x, (_,_) = self.lstm_1_layer(x)
        x = self.dropout_1_layer(x)
        x, (_,_) = self.lstm_2_layer(x)
        x = self.dropout_2_layer(x)
        x, (_,_) = self.lstm_3_layer(x)
        x = self.dropout_3_layer(x)
        x, (_,_) = self.lstm_4_layer(x)
        x = self.dropout_4_layer(x)
        return self.linear_layer(x)

def make_train_step(model, loss_fn, optimizer):
    """
        Computation : Function to make batch size data iterator
    """
    def train_step(x, y):
        model.train()
        yhat = model(x)
        loss = loss_fn(y, yhat)
        loss.backward()
        optimizer.step()
        optimizer.zero_grad()
        return loss.item()
    return train_step

def compute(X,Y):
    """
        Computation : Find Anomaly using model based computation 
    """
    if str(MODEL_SELECTED) == "lstmae":
        model = LSTMAE(10,21)
        criterion = torch.nn.MSELoss(reduction='mean')
        optimizer = torch.optim.Adam(model.parameters(), lr=1e-5)
        train_data = torch.utils.data.TensorDataset(torch.tensor(X.astype(np.float32)), torch.tensor(X.astype(np.float32)))
        train_loader = torch.utils.data.DataLoader(dataset=train_data, batch_size=32, shuffle=False)
        train_step = make_train_step(model, criterion, optimizer)
        for epoch in range(30):
            loss_sum = 0.0
            ctr = 0
            for x_batch, y_batch in train_loader:
                loss_train = train_step(x_batch, y_batch)
                loss_sum += loss_train
                ctr += 1
            print("Training Loss: {0} - Epoch: {1}".format(float(loss_sum/ctr), epoch+1))
        hypothesis = model(torch.tensor(X.astype(np.float32))).detach().numpy()
        loss = np.linalg.norm(hypothesis - X, axis=(1,2))
        return loss.reshape(len(loss),1)
    elif str(MODEL_SELECTED) == "deepant":
        model = DeepAnT(10,21)
        criterion = torch.nn.MSELoss(reduction='mean')
        optimizer = torch.optim.Adam(list(model.parameters()), lr=1e-5)
        train_data = torch.utils.data.TensorDataset(torch.tensor(X.astype(np.float32)), torch.tensor(Y.astype(np.float32)))
        train_loader = torch.utils.data.DataLoader(dataset=train_data, batch_size=32, shuffle=False)
        train_step = make_train_step(model, criterion, optimizer)
        for epoch in range(200):
            loss_sum = 0.0
            ctr = 0
            for x_batch, y_batch in train_loader:
                loss_train = train_step(x_batch, y_batch)
                loss_sum += loss_train
                ctr += 1
            print("Training Loss: {0} - Epoch: {1}".format(float(loss_sum/ctr), epoch+1))
        hypothesis = model(torch.tensor(X.astype(np.float32))).detach().numpy()
        loss = np.linalg.norm(hypothesis - Y, axis=1)
        return loss.reshape(len(loss),1)
    else:
        print("Selection of Model is not in the set")
        return None

def deepant():
    data_file = ""
    MODEL_SELECTED = "deepant" # Possible Values ['deepant', 'lstmae']
    LOOKBACK_SIZE = 10
    data = read_modulate_data(data_file)
    X,Y,T = data_pre_processing(data)
    loss = compute(X, Y)
    loss_df = pd.DataFrame(loss, columns = ["loss"])
    loss_df.index = T
    loss_df.index = pd.to_datetime(loss_df.index)
    loss_df["timestamp"] = T
    loss_df["timestamp"] = pd.to_datetime(loss_df["timestamp"])
    sns.set_style("darkgrid")
    print(loss_df['loss'])
    print(loss_df['loss'].values[-1])

if __name__=='__main__':
    data_file = ""
    MODEL_SELECTED = "deepant" # Possible Values ['deepant', 'lstmae']
    LOOKBACK_SIZE = 10
    data = read_modulate_data(data_file)
    X,Y,T = data_pre_processing(data)
    loss = compute(X, Y)
    loss_df = pd.DataFrame(loss, columns = ["loss"])
    loss_df.index = T
    loss_df.index = pd.to_datetime(loss_df.index)
    loss_df["timestamp"] = T
    loss_df["timestamp"] = pd.to_datetime(loss_df["timestamp"])
    sns.set_style("darkgrid")
    print(loss_df['loss'])
    print(loss_df['loss'].values[-1])
    ax = sns.distplot(loss_df["loss"], bins=100, label="Frequency")
    ax.set_title("Frequency Distribution | Kernel Density Estimation")
    ax.set(xlabel='Anomaly Confidence Score', ylabel='Frequency (sample)')
    plt.legend()
    plt.show()

    ax = sns.lineplot(x="timestamp", y="loss", data=loss_df, color='g', label="Anomaly Score")
    ax.set_title("Anomaly Confidence Score vs Timestamp")
    ax.set(ylabel="Anomaly Confidence Score", xlabel="Timestamp")
    plt.legend()
    plt.show()




