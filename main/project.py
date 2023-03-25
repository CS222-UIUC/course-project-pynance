"""Main Project File"""
# we should probably write a package setup script instead of rerunning imports each and every time
import os
from pathlib import Path
import yfinance as yf
import pandas as pd
import mplfinance as mpf
import matplotlib.pyplot as plt
import requests
import datetime
# from bs4 import BeautifulSoup

def exists_data(stock_name):
    """Checks if the stock data for a particular company exists"""

    stocks = os.listdir('data/')
    #print(stocks)
    for i in stocks:
        if i == str(stock_name) + ".csv":
            return True
    return False

def get_company_data(stock_name):
    """Fetches Company Stock Data and Stores it as CSV file"""

    if exists_data(stock_name):
        #read File
        stock_data = pd.read_csv('data/' + str(stock_name) + '.csv')
        return stock_data
    else:
        stock_data = yf.download(tickers=stock_name, period='1d', interval='1m')
        #print(stock_data)
        #Write it into a file
        filepath = Path('data/' + str(stock_name) + '.csv')
        filepath.parent.mkdir(parents=True, exist_ok=True)
        stock_data.to_csv(filepath)
        return stock_data

def exists_info(stock_name):
    """Checks if the stock info for a particular company exists"""

    stocks = os.listdir('../info/')
    for i in stocks:
        if i == str(stock_name) + ".txt":
            return True
    return False

def get_company_summary(stock_name):
    """Fetches Company Summary and Stores it as txt file
    Returns the company summary string"""

    if exists_info(stock_name):
        #read info
        file = open('../info/' + str(stock_name) + '.txt', "r", encoding="utf-8")
        stock_information = file.read()
        file.close()
        return stock_information
    else:
        #FinnHub API key and website url
        api_key = "cg5s5d1r01qoqcgjb6cgcg5s5d1r01qoqcgjb6d0"
        url = f"https://finnhub.io/api/v1/stock/profile2?symbol={stock_name}&token={api_key}"

        #Used finnhub.io to retreive more information about the stock
        response = requests.get(url)

        #Parse the data in json and store it
        data = response.json()
        stock_information = ""
        for key in data:
            stock_information += str(key) + ": " + str(data[key]) + "\n"
        # Web Scraping
        # #Get the website url of the company
        # url = data['weburl']

        # #Used the Company Website to get summary
        # response = requests.get(url)
        # print("WEB URL", url)

        # #Web Scraping using bs4 library
        # #Web Scrape the company's website get summary
        # soup = BeautifulSoup(response.content, 'html.parser')
        # stock_information = soup.find('meta', attrs={'name': 'description'})['content']
        # stock = yf.Ticker(stock_name)
        # stock_information = stock.info

        #write data
        file = open('../info/' + str(stock_name) + '.txt', "w", encoding="utf-8")
        file.write(stock_information)
        file.close()
        return stock_information

### Visualization Component ###

def plot_stocks_df(stocks, period, interval):
    for stock in stocks:
        plt.figure()
        temp = yf.Ticker(stock)
        hist = yf.download(tickers = stock, period = period, interval = interval)
        mpf.plot(hist, 
                    type = 'candle',
                    volume = True,
                    mav = (20,5),
                    title= stock + " " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    tight_layout = True,
                    figratio= (10,5))
        globals()[f"plot_{stock}_{interval}"] = plt.gcf()

def main():
    """Main Function"""

    print("------Which stock would you like data on?------")
    stock_name = str(input("Please enter it's symbol: "))
    data = get_company_summary(stock_name)
    print(data)

    ### Visualization Component ###

    # period = '1d'
    period = str(input('Enter a period (1d, 1m, 1y): '))
    # interval = '5m'
    interval = str(input('Enter an interval (1d, 1m, 1y): '))

    # stocks = ['MSFT', 'BTC-USD']
    stocks = input('Enter stock name abbreviation separated by commas (AAPL, GOOG, AMZN): ')
    stocks = stocks.replace(' ', '').split(',')

    plot_stocks_df(stocks, period, interval)

main()
