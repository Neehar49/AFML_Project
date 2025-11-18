import pandas as pd
import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import Dataset

class YieldDataset(Dataset):
    def __init__(self, df, crop_to_idx):
        self.df = df.reset_index(drop=True)
        self.crop_to_idx = crop_to_idx

        self.feature_cols = [
            "temp_mean", "rain_total", "humidity_mean",
            "wind_mean", "solar_mean", "ndvi_mean"
        ]

    def __len__(self):
        return len(self.df)

    def __getitem__(self, ix):
        row = self.df.iloc[ix]

        # Numeric features
        x_num = row[self.feature_cols].values.astype(np.float32)

        # Crop one-hot
        crop_vec = np.zeros(len(self.crop_to_idx), dtype=np.float32)
        crop_idx = self.crop_to_idx[row["crop"]]
        crop_vec[crop_idx] = 1.0

        x = np.concatenate([x_num, crop_vec], axis=0)
        y = np.float32(row["yield"])
        region = row["region"]
        return torch.from_numpy(x), torch.tensor(y), region


class Encoder(nn.Module):
    def __init__(self, input_dim, hidden=64, embed=32):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(input_dim, hidden),
            nn.ReLU(),
            nn.Linear(hidden, embed),
            nn.ReLU()
        )

    def forward(self, x):
        return self.net(x)


class Head(nn.Module):
    def __init__(self, embed=32):
        super().__init__()
        self.fc = nn.Linear(embed, 1)

    def forward(self, z):
        return self.fc(z).squeeze(-1)


class FullModel(nn.Module):
    def __init__(self, input_dim, hidden=64, embed=32):
        super().__init__()
        self.encoder = Encoder(input_dim, hidden, embed)
        self.head = Head(embed)

    def forward(self, x):
        z = self.encoder(x)
        return self.head(z)
