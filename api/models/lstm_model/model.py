import torch
from torch import nn
import numpy as np
from src.utils import processing_device
device = processing_device['lstm']

BATCH_SIZE = 1

class torchLSTM(nn.Module):
    def __init__(self, learning_rate, look_back, hidden_size, num_layers, input_size=1, early_stop_patience=5):
        super(torchLSTM, self).__init__()
        self.learning_rate = learning_rate
        self.look_back = look_back
        self.early_stop_patience = early_stop_patience
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        self.lstm = nn.LSTM(input_size, hidden_size, num_layers, dropout=0.1, batch_first=True)
        self.fc = nn.Linear(hidden_size, 1)
        self.to(device)

    def forward(self, x):
        h0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(device)
        c0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(device)
        out, _ = self.lstm(x, (h0, c0))
        out = self.fc(out[:, -1, :])
        return out

    def predict(self, data):
        data = to_tensor(data).reshape(-1, self.look_back, self.input_size).to(device)
        return self(data).detach().cpu().numpy()

    def fit(self, train_x, train_y, epochs):
        train_x, train_y = to_tensor(train_x).to(device), to_tensor(train_y).to(device)
        criterion = nn.MSELoss()
        optimizer = torch.optim.Adam(self.parameters(), lr=self.learning_rate, betas=[0.9, 0.999])
        lowest_loss = float('inf')
        counter_patience = 0
        for epoch in range(epochs):
            loss = 0
            optimizer.zero_grad()
            batch_idx = np.random.randint(0, train_x.size(0), BATCH_SIZE)
            for product_serie_x, product_serie_y in zip(train_x[batch_idx], train_y[batch_idx]):
                for i, (x, y) in enumerate(zip(product_serie_x, product_serie_y)):
                    x = x.reshape(-1, self.look_back, self.input_size).to(device)
                    y = y.reshape(1, 1).to(device)
                    loss += criterion(self(x), y)
            if loss >= lowest_loss:
                counter_patience += 1
                if counter_patience == self.early_stop_patience:
                    break
            else:
                lowest_loss = loss
                counter_patience = 0
            loss.backward()
            optimizer.step()


def to_tensor(array):
    return torch.from_numpy(array).float()
