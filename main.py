import csv
import os
import tkinter

import matplotlib
import matplotlib.pyplot as plt
import pandas
import requests
from bs4 import BeautifulSoup

import plot

allData = []


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


def main(code):
    '''insert the stock code'''
    url = 'https://finance.yahoo.com/quote/' + \
        code + '.SS/history?p=' + code + '.SS'
    save_road = "stock_" + code + ".csv"
    html = getHTMLText(url)
    soup = BeautifulSoup(html, "html.parser")
    fillDataList(soup)
    # try:
    printDataList(100)
    # except IndexError:
    #   print"
    writercsv(save_road, 100, title)
    data, date, ma, color = plot.dataset(save_road)
    print(data,date)
    plot.plotstock(data, date, ma, color)
