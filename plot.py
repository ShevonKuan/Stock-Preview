import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import pandas


def dataset(csv):
    data = np.loadtxt(csv, skiprows=1, delimiter=';', usecols=np.arange(1, 7))[::-1]
    date = np.loadtxt(csv, skiprows=1, delimiter=';', usecols=(0), dtype='str')[::-1]
    madata = data[:, 4]
    ma = np.linspace(5,100,95)
    for i in range(0,95):
        ma[i] = np.mean(madata[i:i+5])
    color = []
    for j in range(0,100):
        if data[j,0]>data[j,4]: # open>close
            color.append('g')
        else:
            color.append('r')
    return data, date, ma, color


def plotstock(data, date, ma, color):
    '''draw the stock figure'''
    plt.style.use('fast')
    
    arange = np.linspace(1, 100, 100)  # x-axis arange

    fig, ax1 = plt.subplots(figsize=(5, 2))
    ax1.set_ylabel('Volume of Bussiness')
    
    plt.ylim(0,1e10)
    ax1.bar(arange, data[:, 5], label='Volume', color=color)  # fig-1 Volume
    ax2 = ax1.twinx()
    ax2.set_ylabel('Price')
    ax2.plot(np.linspace(5,100,95), ma, label='MA5',color='purple')
    #ax2.xaxis.set_major_locator(ticker.MultipleLocator(20))
    plt.xlabel('Date')
    plt.xticks(
        arange[0:100:5],
        date[0:100:5],
        fontsize=5,
    )
    plt.yticks(fontsize=10)
    # final figure shown
    plt.legend()
    handle1, label1 = ax1.get_legend_handles_labels()
    handle2, label2 = ax2.get_legend_handles_labels()
    plt.legend(handle1+handle2, label1+label2)
    plt.tight_layout()
    plt.grid('off')
    plt.show()
