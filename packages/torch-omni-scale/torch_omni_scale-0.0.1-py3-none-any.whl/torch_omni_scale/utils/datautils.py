import os
import numpy as np
import pandas as pd
import math
import random
from datetime import datetime
import pickle
# from utils import pkl_load, pad_nan_to_target
from scipy.io.arff import loadarff
from sklearn.preprocessing import StandardScaler, MinMaxScaler

import torch
import torch.nn as nn
from torch.utils.data import TensorDataset, DataLoader


def load_UCR(dataset, batch_size, device, expand=True):
    train_file = os.path.join('datasets/UCR', dataset, dataset + "_TRAIN.tsv")
    test_file = os.path.join('datasets/UCR', dataset, dataset + "_TEST.tsv")
    train_df = pd.read_csv(train_file, sep='\t', header=None)
    test_df = pd.read_csv(test_file, sep='\t', header=None)
    train_array = np.array(train_df)
    test_array = np.array(test_df)
    # Move the labels to {0, ..., L-1}
    labels = np.unique(train_array[:, 0])
    transform = {}
    for i, l in enumerate(labels):
        transform[l] = i

    train = train_array[:, 1:].astype(np.float64)
    train_labels = np.vectorize(transform.get)(train_array[:, 0])
    test = test_array[:, 1:].astype(np.float64)
    test_labels = np.vectorize(transform.get)(test_array[:, 0])
    
    def create_data_loader(x, y, shuffle):
            x = torch.tensor(x).to(device)
            y = torch.tensor(y).to(device)
            dataset = TensorDataset(x, y)
            data_loader = DataLoader(dataset, batch_size=batch_size, shuffle=shuffle)
            return data_loader

    train_data_loader = create_data_loader(train[..., np.newaxis], train_labels, shuffle=True)
    test_data_loader = create_data_loader(test[..., np.newaxis], test_labels, shuffle=False)

    return train[..., np.newaxis], train_labels, test[..., np.newaxis], test_labels, train_data_loader, test_data_loader
"""
def main():
    dataset = "Chinatown"  # 替换为你要加载的数据集名称
    train, train_labels, test, test_labels = load_UCR(dataset)
    print(train.shape)
    print(train_labels)


if __name__ == "__main__":
    main()

"""
