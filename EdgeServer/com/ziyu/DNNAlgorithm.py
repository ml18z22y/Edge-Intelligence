import numpy as np
import torch.nn as nn
from torch.utils.data import Dataset


class DHOP(Dataset):
    def __init__(self, df):
        self.df = df

    def __len__(self):
        return len(self.df)

    def __getitem__(self, index):
        arr_value = np.array(list(self.df["value"]))
        x = self.Normalization(arr_value)[index]
        y = np.array(list(self.df["class"]))[index]
        return x, y

    def Normalization(self, arr):
        min = np.array([0.0, -0.74808, -0.55349, -1.3364, 1.0, -72.0, 0.0, 920.25, 0.0])
        ptp = np.array([1739.4, 2.25128, 2.58369, 2.5542, 3.0, 33.5, 6.2817, 5.5, 1.0])
        arr = np.subtract(arr, min)
        arr = np.divide(arr, ptp)
        return arr


class Model(nn.Module):
    def __init__(self):
        super(Model, self).__init__()
        self.layer1 = nn.Sequential(
            nn.Conv1d(1, 3, 3, padding=1),
            nn.ReLU()
        )
        self.layer2 = nn.Sequential(
            nn.Conv1d(3, 5, 3, padding=1),
            nn.ReLU()
        )
        self.layer3 = nn.MaxPool1d(2)
        self.layer4 = nn.Sequential(
            nn.Conv1d(5, 7, 3, padding=1),
            nn.ReLU()
        )
        self.layer5 = nn.Linear(28, 4)

    def forward(self, input):
        out = input.unsqueeze(1)
        # print(out.shape)
        out = self.layer1(out)
        # print(out.shape)
        out = self.layer2(out)
        # print(out.shape)
        out = self.layer3(out)
        # print(out.shape)
        out = self.layer4(out)
        # print(out.shape)
        out = out.reshape(out.size(0), -1)
        out = self.layer5(out)
        return out