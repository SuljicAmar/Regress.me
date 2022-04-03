import pandas as pd
import math


def Standardize(data, dataframe = False):
    if dataframe == False:
        N = len(data)
        u = sum(data)/N
        standardized_data = []
        std = StandardDeviation(data)
        for i in data:
            standardized_data.append((i-u)/std)
        return standardized_data
    else:
        dfs = []
        for i in data.columns:
            N = data[i].shape[0]
            u = data[i].sum()/N
            standardized_data = []    
            std = StandardDeviation(data[i].values)
            for k in data[i].values:
                standardized_data.append((k-u)/std)
            dfs.append(pd.DataFrame({i: standardized_data}))
        return pd.concat(dfs, axis=1)

def MinMax(data, dataframe = False):
    if dataframe == False:
        min_x = min(data)
        max_x = max(data)
        scaled_data = []
        for i in data:
            scaled_data.append((i-min_x)/(max_x - min_x))
        return scaled_data
    else:
        dfs = []
        for i in data.columns:
            min_x = data[i].min()
            max_x = data[i].max()
            scaled_data = []
            for k in data[i].values:
                scaled_data.append((k-min_x)/(max_x - min_x))
            dfs.append(pd.DataFrame({i: scaled_data}))
        return pd.concat(dfs, axis=1)


def StandardDeviation(data):
    N = len(data)
    u = sum(data)/N 
    sm = 0
    for i in data:
       sm += (i - u) **2
    div = sm/(N-1)
    return math.sqrt(div)