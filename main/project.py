"""Main Project File"""
import os
from pathlib import Path
import yfinance as yf
import pandas as pd

def get_company_data(stock_name):
    """Fetches Company Stock Data and Stores it as CSV file"""
    if exists(stock_name):
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

        #Write descriptions
        filepath = Path('data/' + str(stock_name) + '.txt')
        filepath.parent.mkdir(parents=True, exist_ok=True)
        #stock_data.to_csv(filepath)  FIGURE OUT HOW TO WRITE STOCK_DATA.INFO TO A TXT FILE
        return stock_data


def exists(stock_name):
    """Checks if the stock data for a particular company exists"""
    stocks = os.listdir('data/')
    print(stocks)
    for i in stocks:
        if i == str(stock_name) + ".csv":
            return True
    return False

def main():
    """Main Function"""

    return 0
