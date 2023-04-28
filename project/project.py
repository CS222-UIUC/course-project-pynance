"""Main Project File"""
# we should probably write a package setup script instead of rerunning imports each and every time
import os
from pathlib import Path
import datetime
import json
import yfinance as yf
import pandas as pd
import mplfinance as mpf
import matplotlib.pyplot as plt
import requests
from sklearn import metrics
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
# from bs4 import BeautifulSoup

def exists_data(stock_name, custom_period, custom_interval):
    """Checks if the stock data for a particular company exists"""

    stocks = os.listdir('data/')
    #print(stocks)
    for i in stocks:
        if i == str(stock_name) + '_' + custom_period + '_' + custom_interval + ".csv":
            return True
    return False

def get_company_data(stock_name, custom_period, custom_interval):
    """Fetches Company Stock Data and Stores it as CSV file"""

    if exists_data(stock_name, custom_period, custom_interval):
        #read File
        stock_data = pd.read_csv('data/' + str(stock_name) + '_' +
                                custom_period + '_' + custom_interval + '.csv')
        return stock_data
    stock_data = yf.download(tickers=stock_name, period=custom_period, interval=custom_interval)
    #print(stock_data)
    #Write it into a file
    filepath = Path('data/' + str(stock_name) + '_' +
                    custom_period + '_' + custom_interval + '.csv')
    filepath.parent.mkdir(parents=True, exist_ok=True)
    stock_data.to_csv(filepath)
    return stock_data

def exists_info(stock_name):
    """Checks if the stock info for a particular company exists"""

    stocks = os.listdir('info/')
    for i in stocks:
        if i == str(stock_name) + ".txt":
            return True
    return False
if __name__ == "__main__":
    def get_company_summary(stock_name):
        """Fetches Company Summary and Stores it as txt file
        Returns the company summary string"""

        if exists_info(stock_name):
            #read info
            with open('info/' + str(stock_name) + '.txt', "r", encoding="utf-8") as file:
                stock_information = file.read()
                return stock_information
        else:
            #FinnHub API key and website url
            api_key = ""
            with open('config.json', 'r', encoding="utf-8") as api_file:
                config = json.load(api_file)
                api_key = config['api_key']
            url = f"https://finnhub.io/api/v1/stock/profile2?symbol={stock_name}&token={api_key}"

            #Used finnhub.io to retreive more information about the stock
            response = requests.get(url, timeout=60)

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
            with open('info/' + str(stock_name) + '.txt', "w", encoding="utf-8") as file:
                file.write(stock_information)
            return stock_information

### Visualization Component ###
if __name__ == "__main__":
    def plot_stocks_df(stocks, period, interval):
        '''Visualization Component'''
        for stock in stocks:
            plt.figure()
            # temp = yf.Ticker(stock)
            hist = yf.download(tickers = stock, period = period, interval = interval)
            mpf.plot(hist,
                        type = 'candle',
                        volume = True,
                        mav = (20,5),
                        title= stock + " " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        tight_layout = True,
                        figratio= (10,5))
            globals()[f"plot_{stock}_{interval}"] = plt.gcf()

# Run Linear Regression
def run_linear_regression(stock_data):
    """Builds and tests linear regression model"""
    x_1 = stock_data[['Open', 'High','Low', 'Volume']]
    y_1 = stock_data['Close']
    train_x, test_x, train_y, test_y = train_test_split(x_1, y_1, test_size=0.15 ,
                                                        shuffle=False,random_state = 0)
    # print(train_x.shape)
    # print(test_x.shape)
    # print(train_y.shape)
    # print(test_y.shape)
    regression = LinearRegression()
    regression.fit(train_x, train_y)
    return (regression, test_x, test_y)

if __name__ == "__main__":
    def get_stats(model, test_x, test_y):
        """Provides Statistics of the Linear Model"""
        print("regression coefficient",model.coef_)
        print("regression intercept",model.intercept_)
        # the coefficient of determination R²
        regression_confidence = model.score(test_x, test_y)
        print("linear regression confidence: ", regression_confidence)

        predicted=model.predict(test_x)
        dfr=pd.DataFrame({'Actual_Price':test_y, 'Predicted_Price':predicted})
        print(dfr.head(10))

        print('Mean Absolute Error (MAE):', metrics.mean_absolute_error(test_y, predicted))

        x_2 = dfr.Actual_Price.mean()
        y_2 = dfr.Predicted_Price.mean()
        print("The accuracy of the model is " , x_2/y_2*100)

    # Visualization
if __name__ == "__main__":
    def get_plots(model, test_x, test_y):
        """Visualizes the Model"""
        predicted=model.predict(test_x)
        dfr=pd.DataFrame({'Actual_Price':test_y, 'Predicted_Price':predicted})
        plt.scatter(dfr.Actual_Price, dfr.Predicted_Price,  color='Darkblue')
        plt.xlabel("Actual Price")
        plt.ylabel("Predicted Price")
        plt.show()

        plt.plot(dfr.Actual_Price, color='black')
        plt.plot(dfr.Predicted_Price, color='lightblue')
        plt.title("Nio prediction chart")
        plt.show()

def get_predicted_price(stock_name, period, interval, predict_open, predict_high, predict_low, predict_vol):
    """Returns the predicted price"""
    stock_data = get_company_data(stock_name, period, interval)
    model, test_x, test_y = run_linear_regression(stock_data)
    predict_df = pd.DataFrame({"Open": [int(predict_open)], "High": [int(predict_high)],
                            "Low": [int(predict_low)], "Volume": [int(predict_vol)]})
    test_x += []
    test_y += []
    return model.predict(predict_df)[0]    


if __name__ == "__main__":
    def main():
        """Main Function"""
        print("How many stocks do you want data on?")
        print("Enter a non-negative integer here: ")
        # n_1 = int(input())
        # while n_1 > 0:
        #     print("------Which stock would you like data on?------")
        #     stock_name = str(input("Please enter it's symbol: "))
        #     period = str(input("""Please enter the period over which you want the data
        #                         (1d -> 1 day; 1m -> 1 month; 1y -> 1 year): """))
        #     interval = str(input("""Please enter the interval between which you want the data
            # (1d -> 1 day; 1m -> 1 month; 1y -> 1 year): """))
            # data = get_company_summary(stock_name)
            # print(data)
            # stock_data = get_company_data(stock_name, period, interval)
            # model, test_x, test_y = run_linear_regression(stock_data)
            # want_stats = input("Would you like the statistics of the model? (y/n)")
            # if want_stats == 'y':
            #     get_stats(model, test_x, test_y)
            # want_plots = input("Would you like the plots of the data? (y/n)")
            # if want_plots == 'y':
            #     get_plots(model, test_x, test_y)
            # predict_open = int(input("Enter the opening price of the stock: "))
            # predict_high = int(input("Enter the high of the stock: "))
            # predict_low = int(input("Enter the low of the stock: "))
            # predict_vol = int(input("Enter the volume the stock: "))
            # predict_df = pd.DataFrame({"Open": [predict_open], "High": [predict_high],
            #                 "Low": [predict_low], "Volume": [predict_vol]})
            # print("The predicted closing price of", stock_name, "is:",
            #     model.predict(predict_df)[0])
            # print("*************")
            # print("Thank you for using this app")
            # print("*************")
            # ### Visualization Component ###
            # n_1 -= 1
            # # period = '1d'
            # period = str(input('Enter a period (1d, 1m, 1y): '))
            # # interval = '5m'
            # interval = str(input('Enter an interval (1d, 1m, 1y): '))

            # # stocks = ['MSFT', 'BTC-USD']
            # stocks = input('Enter stock name
            # abbreviation separated by commas (AAPL, GOOG, AMZN): ')
            # stocks = stocks.replace(' ', '').split(',')

            # plot_stocks_df(stocks, period, interval)
            # keyput = str(input("Would You like data
            # on another stock?[press y if yes, otherwise no]"))
            # if keyput != 'y':
            #     break

if __name__ == "__main__":
    main()
