import time
import numpy as np
import pandas as pd
import torch
from datetime import datetime, timedelta
from app.models import *
import pandas as pd
from scipy import fftpack
from app import db
from twilio.rest import Client
from config import BaseConfig
from sklearn.preprocessing import MinMaxScaler
LOOKBACK_SIZE = 10

def twillio_message(variable, algorithm):
    try:
        client = Client()
        from_whatsapp_number='whatsapp:+14155238886'
        users = User.query.filter(User.alarms==True).order_by(User.id)
        for user in users:
            to_whatsapp_number='whatsapp:{}{}'.format(user.telephone[:5], user.telephone[6:])
            if variable[0] == 'T':
                client.messages.create(body='Anomaly detected regarding temperature readings, please check if there is any heat sources near your equipment! If your device has any gears or moving parts it may be helpfull to call the maintenance staff and check the lubrication. {}'.format(algorithm),
                    from_=from_whatsapp_number,
                                to=to_whatsapp_number)

            elif variable[0] == 'A':
                client.messages.create(body='The accelerometer in your equipment pointed an anomaly, please check your device and all the surroundings, in special the screws used for support, its possible that something is loose. {}'.format(algorithm),
                                from_=from_whatsapp_number,
                                to=to_whatsapp_number)

            elif variable[0] == 'R':
                client.messages.create(body='The gyroscope in your equipment pointed an anomaly, please check your device and all the surroundings, in special the screws used for support, its possible that something is loose. {}'.format(algorithm),
                        from_=from_whatsapp_number,
                        to=to_whatsapp_number)
            else:
                client.messages.create(body='DeepAnT algorithm modelled a fault in your system! Contact directly your maintenance staff!',
                        from_=from_whatsapp_number,
                        to=to_whatsapp_number)
    except Exception as e:
        print('excecao twillio - {}'.format(e))

def anomaly(measure_id):
    measures = Measure.query.filter(Measure.date > datetime.now()-timedelta(hours=4), Measure.id<=measure_id).order_by(Measure.id)
    data = {'Acceleration': {'acel_x': [],
            'acel_y': [],
            'acel_z': []},
            'Rotation': {'rot_x': [],
            'rot_y': [],
            'rot_z': []},
            'Temperature': {'temp':[]},
            'id': []
            }
    for measure in measures:
        data['Acceleration']['acel_x'].append(measure.acel_x)
        data['Acceleration']['acel_y'].append(measure.acel_y)
        data['Acceleration']['acel_z'].append(measure.acel_z)
        data['Rotation']['rot_x'].append(measure.rot_x)
        data['Rotation']['rot_y'].append(measure.rot_y)
        data['Rotation']['rot_z'].append(measure.rot_z)
        data['Temperature']['temp'].append(measure.temperature)
        data['id'].append(measure.id)
    if len(data['id']) > 100:
        for variable in ['Acceleration', 'Rotation', 'Temperature', '-']:   
            last_anomaly = Anomaly.query.filter(Anomaly.variable==variable).order_by(Anomaly.id.desc()).first()
            if variable=='-':
                deep_tag = deepant()
                if deep_tag:
                    anomaly = Anomaly(behavior='DeepAnT', variable=variable, measure_id=measure_id, date=datetime.now())
                    db.session.add(anomaly)
                    db.session.commit()
            else:
                outlier_anomaly, frequency_anomaly = anomaly_analysis(data[variable])
                if outlier_anomaly:
                    anomaly = Anomaly(behavior='Outlier', variable=variable, measure_id=measure_id, date=datetime.now())
                    db.session.add(anomaly)
                    db.session.commit()
                if variable != 'Temperature':
                    if frequency_anomaly:
                        anomaly = Anomaly(behavior='Frequency', variable=variable, measure_id=measure_id, date=datetime.now())
                        db.session.add(anomaly)
                        db.session.commit()
            if last_anomaly:
                if datetime.now() - timedelta(minutes=5) > last_anomaly.date:
                    if variable == '-':
                        if deep_tag:
                            twillio_message(variable, 'DeepAnT')
                    else:
                        if frequency_anomaly or outlier_anomaly:
                            if frequency_anomaly and outlier_anomaly:
                                twillio_message(variable, 'Frequency and Outlier - Algorithm')
                            else:
                                if frequency_anomaly:
                                    twillio_message(variable, 'Frequency - Algorithm')
                                else:
                                    twillio_message(variable, 'Outlier - Algorithm')
            else:
                if variable == '-':
                    if deep_tag:
                        twillio_message(variable, 'DeepAnT')
                else:
                    if frequency_anomaly or outlier_anomaly:
                        if frequency_anomaly and outlier_anomaly:
                            twillio_message(variable, 'Frequency and Outlier - Algorithm')
                        else:
                            if frequency_anomaly:
                                twillio_message(variable, 'Frequency - Algorithm')
                            else:
                                twillio_message(variable, 'Outlier - Algorithm')

def anomaly_analysis(data):
    frequency_tag, outlier_tag = False, False
    for key in data.keys():
        if outlier_function(data[key]):
            outlier_tag = True
        if frequency_function(data[key]): 
            frequency_tag = True
        if frequency_tag and outlier_tag:
            break
    return outlier_tag, frequency_tag

def outlier_function(data):
    dataframe = pd.DataFrame()
    dataframe['value'] = data
    Q1 = dataframe.quantile(0.25).value
    Q3 = dataframe.quantile(0.75).value
    IQR = Q3 - Q1
    if Q1-1.5*IQR< data[-1] < Q3+1.5*IQR:
        outlier_anomaly = False
    else:
        outlier_anomaly = True
    return outlier_anomaly

def frequency_function(data):
    Data = fftpack.fft(data)
    f_s = 1
    freqs = fftpack.fftfreq(len(data), 0.1)
    dataframe = pd.DataFrame()
    dataframe['freqs'] = freqs
    dataframe['magnitude'] = np.abs(Data)
    filtered = dataframe[dataframe['magnitude']>500]
    if len(filtered) > 2:
        frequency_anomaly = True
    elif len(filtered) == 1:
        if filtered['freqs'].values[0] == 0.0:
            frequency_anomaly = False
        else:
            frequency_anomaly = True
    else:
        frequency_anomaly = False
    return frequency_anomaly

def read_modulate_data(data_file):
    measures = Measure.query.filter(Measure.date>datetime.now()-timedelta(hours=7)).order_by(Measure.id)
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
    data = pd.DataFrame()
    data['LOCAL_DATE'] = dates
    data['rot_x'] = rot_x
    data['rot_y'] = rot_y
    data['rot_Z'] = rot_z
    data['acel_x'] = acel_x
    data['acel_y'] = acel_y
    data['acel_z'] = acel_z
    data['down_acel_x'] = down_acel_x
    data['upper_acel_x'] = upper_acel_x
    data['down_acel_y'] = down_acel_y
    data['upper_acel_y'] = upper_acel_y
    data['down_acel_z'] = down_acel_z
    data['upper_acel_z'] = upper_acel_z
    data['down_rot_x'] = down_rot_x
    data['upper_rot_x'] = upper_rot_x
    data['down_rot_y'] = down_rot_y
    data['upper_rot_y'] = upper_rot_y
    data['down_rot_z'] = down_rot_z  
    data['upper_rot_z'] = upper_rot_z
    data['down_temperature'] = down_temperature
    data['upper_temperature'] = upper_temperature
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
    model = DeepAnT(10,21)
    criterion = torch.nn.MSELoss(reduction='mean')
    optimizer = torch.optim.Adam(list(model.parameters()), lr=1e-5)
    train_data = torch.utils.data.TensorDataset(torch.tensor(X.astype(np.float32)), torch.tensor(Y.astype(np.float32)))
    train_loader = torch.utils.data.DataLoader(dataset=train_data, batch_size=32, shuffle=False)
    train_step = make_train_step(model, criterion, optimizer)
    for epoch in range(100):
        loss_sum = 0.0
        ctr = 0
        for x_batch, y_batch in train_loader:
            loss_train = train_step(x_batch, y_batch)
            loss_sum += loss_train
            ctr += 1
        if float(loss_sum/ctr) < 0.06:
            break
    hypothesis = model(torch.tensor(X.astype(np.float32))).detach().numpy()
    loss = np.linalg.norm(hypothesis - Y, axis=1)
    return loss.reshape(len(loss),1), float(loss_sum/ctr)

def deepant():
    try:
        data_file = ""
        MODEL_SELECTED = "deepant" # Possible Values ['deepant', 'lstmae']
        data = read_modulate_data(data_file)
        X,Y,T = data_pre_processing(data)
        loss, train_loss = compute(X, Y)
        if train_loss < 0.06:
            loss_df = pd.DataFrame(loss, columns = ["loss"])
            print('loss',train_loss)
            if loss_df['loss'].values[-1] > loss_df.quantile(0.99).loss:
                return True
            else:
                return False
        else:
            print('Not converged', train_loss)
            return False
    except Exception as e:
        print('excecao deepant', e)
        return False

if __name__ == '__main__':
#    anomaly()
    deepant([])
