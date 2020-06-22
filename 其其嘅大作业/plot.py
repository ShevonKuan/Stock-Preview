
import numpy as np


def dataset(csv):
    data = np.loadtxt(csv, skiprows=1, delimiter=';',
                      usecols=np.arange(1, 7))[::-1]
    date = np.loadtxt(csv, skiprows=1, delimiter=';',
                      usecols=(0), dtype='str')[::-1]
    madata = data[:, 4]
    ma5 = np.linspace(5, 100, 95)
    for i in range(0, 95):
        ma5[i] = np.mean(madata[i:i+5])
    ma10 = np.linspace(10, 100, 90)
    for i in range(0, 90):
        ma10[i] = np.mean(madata[i:i+10])
        
    color = []
    for j in range(0, 100):
        if data[j, 0] > data[j, 4]:  # open>close
            color.append('g')
        else:
            color.append('r')
    return data, date, ma5, ma10, color



