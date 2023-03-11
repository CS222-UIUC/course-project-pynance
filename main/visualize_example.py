# import os
# os.system("pip install yfinance")
# os.system("pip install mplfinance")
# we should write a package setup script for this, if already installed runtime is long and checks are redundant
import datetime
import yfinance as yf
import mplfinance as mpf
import matplotlib.pyplot as plt

# period = '1d'
period = str(input('Enter a period (1d, 1m, 1y): '))

# interval = '5m'
interval = str(input('Enter an interval (1d, 1m, 1y): '))

# stocks = ['MSFT', 'BTC-USD']
stocks = input('Enter stock name abbreviation separated by commas (AAPL, GOOG, AMZN): ')
stocks = stocks.replace(' ', '').split(',')

def plot_stocks_df(stocks, period, interval):
    for stock in stocks:
        plt.figure()
        temp = yf.Ticker(stock)
        hist = yf.download(tickers=stock, period=period, interval=interval)

        mpf.plot(hist, type='candle',
            volume=True, mav=(20,5),title = stock+" "+datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            tight_layout=True, figratio=(10,5))

        globals()[f"plot_{stock}_{interval}"] = plt.gcf()

plot_stocks_df(stocks, period, interval)