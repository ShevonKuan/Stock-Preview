import csv
import os
import tkinter as tk
import tkinter.messagebox
import time
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import pandas
import requests
from bs4 import BeautifulSoup
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

import plot




def statuschange(str):
    status.config(text='Status: ' + str)



var = 0  # initial $var

#fig = plt.figure(figsize=(2,1),dpi=80)
#ax1 = fig.add_subplot(111)
fig, ax1 = plt.subplots(figsize=(2,1),dpi=80)


allData = []
''' WEB SCRAPING '''

def getHTMLText(url):
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        r.encoding = 'utf-8'
        return r.text
    except:
        return ""


def fillDataList(soup):
    data = soup.find_all('tr')
    for tr in data:
        ltd = tr.find_all('td')
        if len(ltd) == 0:
            continue
        singleData = []
        for td in ltd:
            singleData.append(td.string)
        allData.append(singleData)


def printDataList(num):
    print("{:^13}{:^8}{:^8}{:^8}{:^8}{:^13}{:^13}".format(
        "Date", "Open", "High", "Low", "Close*", "Adj Close**", "Volume"))
    for i in range(num):
        u = allData[i]
        print("{:^13}{:^8}{:^8}{:^8}{:^8}{:^13}{:^13}".format(
            u[0], u[1], u[2], u[3], u[4], u[5], u[6]))


def writercsv(save_road, num, title):
    with open(save_road, 'w', newline='')as f:
        csv_write = csv.writer(f, dialect='excel', delimiter=";")
        csv_write.writerow(title)
        for i in range(num):
            u = allData[i]
            u[6] = u[6].replace(',', '')
            u[0] = u[0].replace(', 2020', '')
            csv_write.writerow(u)


title = ["Date", "Open", "High", "Low", "Close*", "Adj Close**", "Volume"]

save_road, data, date, ma5, ma10, color = 0, 0, 0, 0, 0, 0  # initial $save_load


def search(code):
    '''search the stock code'''
    global save_road, data, date, ma5, ma10, color
    url = 'https://finance.yahoo.com/quote/' + \
        code + '.SS/history?p=' + code + '.SS'
    save_road = "stock_" + code + ".csv"
    statuschange('Acquiring Data...')
    html = getHTMLText(url)
    soup = BeautifulSoup(html, "html.parser")
    fillDataList(soup)
    printDataList(100)
    writercsv(save_road, 100, title)
    statuschange('Processing Data')
    data, date, ma5, ma10, color = plot.dataset(save_road)
    print(data, date)
    plotstock()


def plotstock():
    '''draw the stock figure'''
    global fig, ax1
    ax1.clear()
    statuschange('Rendering Figure...')
    plt.style.use('fast')

    arange = np.linspace(1, 100, 100)  # x-axis arange

    ax1.set_ylabel('Volume of Bussiness')

    plt.ylim(0, 1e10)
    ax1.bar(arange, data[:, 5], label='Volume', color=color)  # fig-1 Volume
    ax2 = ax1.twinx()
    ax2.set_ylabel('Price')
    ax2.plot(np.linspace(5, 100, 95), ma5, label='MA5', color='purple',linewidth=0.5)
    #ax2.plot(np.linspace(10, 100, 90), ma10, label='MA10', color='blue',linewidth=0.5)
    # ax2.xaxis.set_major_locator(ticker.MultipleLocator(20))
    plt.xlabel('Date')
    plt.xticks(
        arange[0:100:10],
        date[0:100:10],
        #fontsize=0.5,
    )
    plt.yticks(fontsize=1)
    # final figure shown
    plt.legend()
    handle1, label1 = ax1.get_legend_handles_labels()
    handle2, label2 = ax2.get_legend_handles_labels()
    plt.legend(handle1+handle2, label1+label2)
    plt.tight_layout()
    plt.grid('off')
    figure.draw()
    statuschange('IDLE')


def insert():
    '''data transport to $var'''
    global var
    var = e.get()

    # try:
    #     
    statuschange('Accessing Server...')
    time.sleep(2)
    search(var)
    # except:
    #     tk.messagebox.showerror(title='Some thing error',
    #                             message='Can\'t find the stock, please retry.')

window = tk.Tk()
window.title('Stock Info Acquisition 1.0')
window.geometry('1920x1080')
figure = FigureCanvasTkAgg(fig, window)
figure.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.YES)
l = tk.Label(window,
             text='Stock Information Acquisition System',
             font=('Arial', 16))
l.pack()
e = tk.Entry(window, show=None, font=('Arial', 20))
e.pack()
status = tk.Label(window, text='Status: IDLE', width=20,font=('Arial', 16))
status.pack()


# Button
tk.Button(window, text='Search', width=20, height=2,
          command=insert).pack()  # search & draw volumn


#tk.Label(window,text='The Lattest Data',font=('Arial', 16)).pack()
#tk.Label(window,text='Open: ' + str(data[100,0]),font=('Arial', 16)).pack()
#t = tk.Text(window, height=3)
# t.pack()
window.mainloop()