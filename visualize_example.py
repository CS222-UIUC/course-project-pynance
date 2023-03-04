

period = '1d'

interval = '5m'

stocks = ['MSFT', 'BTC-USD']

import os
os.system("pip install yfinance")
os.system("pip install mplfinance")
import datetime
import yfinance as yf
import mplfinance as mpf
import matplotlib.pyplot as plt


def plot_stocks_df(stocks, period='1d' , interval='1m'):
    for stock in stocks:
        plt.figure()
        temp = yf.Ticker(stock)
        hist = yf.download(tickers=stock, period=period, interval=interval)

        mpf.plot(hist, type='candle',
            volume=True, mav=(20,5),title = stock+" "+datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            tight_layout=True, figratio=(10,5))
        globals()[f"plot_{stock}_{interval}"] = plt.gcf()



plot_stocks_df(stocks, period, interval)


