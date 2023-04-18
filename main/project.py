"""Main Project File"""
# we should probably write a package setup script instead of rerunning imports each and every time
import os
from pathlib import Path
import datetime
import yfinance as yf
import pandas as pd
import mplfinance as mpf
import matplotlib.pyplot as plt
import requests
from sklearn import metrics
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from tensorflow import keras
import tensorflow as tf
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
    else:
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

def get_company_summary(stock_name):
    """Fetches Company Summary and Stores it as txt file
    Returns the company summary string"""   

    if exists_info(stock_name):
        #read info
        file = open('info/' + str(stock_name) + '.txt', "r", encoding="utf-8")
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
        file = open('info/' + str(stock_name) + '.txt', "w", encoding="utf-8")
        file.write(stock_information)
        file.close()
        return stock_information

### Visualization Component ###

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
    print(train_x.shape)
    print(test_x.shape)
    print(train_y.shape)
    print(test_y.shape)
    regression = LinearRegression()
    regression.fit(train_x, train_y)
    print("regression coefficient",regression.coef_)
    print("regression intercept",regression.intercept_)
    # the coefficient of determination R²
    regression_confidence = regression.score(test_x, test_y)
    print("linear regression confidence: ", regression_confidence)

    predicted=regression.predict(test_x)
    dfr=pd.DataFrame({'Actual_Price':test_y, 'Predicted_Price':predicted})
    print(dfr.head(10))

    print('Mean Absolute Error (MAE):', metrics.mean_absolute_error(test_y, predicted))

    x_2 = dfr.Actual_Price.mean()
    y_2 = dfr.Predicted_Price.mean()
    accuracy_1 = x_2/y_2*100
    print("The accuracy of the model is " , accuracy_1)

    # Visualization

    plt.scatter(dfr.Actual_Price, dfr.Predicted_Price,  color='Darkblue')
    plt.xlabel("Actual Price")
    plt.ylabel("Predicted Price")
    plt.show()

    plt.plot(dfr.Actual_Price, color='black')
    plt.plot(dfr.Predicted_Price, color='lightblue')
    plt.title("Nio prediction chart")
    plt.show()

def run_lstm(stock_data):
    df = pd.read_csv(stock_data)
    feature_keys = [
        "Open",
        "High",
        "Low",
        "Volume",
    ]
    split_fraction = 0.715
    print(df.shape[0])
    train_split = int(split_fraction * int(df.shape[0]))
    print(train_split)
    step = 6

    past = 20
    future = 5
    learning_rate = 0.001
    batch_size = 256
    epochs = 10

    date_time_key = "Date"

    features = df[feature_keys]
    features.index = df[date_time_key]
    features.head()

    features = lstm_helper_normalize(features.values, train_split)
    features = pd.DataFrame(features)
    features.head()

    train_data = features.loc[0 : train_split - 1]
    val_data = features.loc[train_split:]

    start = past + future
    end = start + train_split

    x_train = train_data[[i for i in range(3)]].values
    y_train = features.iloc[start:end][[1]]


    sequence_length = int(past / step)

    dataset_train = keras.preprocessing.timeseries_dataset_from_array(
    x_train,
    y_train,
    sequence_length=sequence_length,
    sampling_rate=step,
    batch_size=batch_size,)

    x_end = len(val_data) - past - future

    label_start = train_split + past + future

    x_val = val_data.iloc[:x_end][[i for i in range(3)]].values
    y_val = features.iloc[label_start:][[1]]

    dataset_val = keras.preprocessing.timeseries_dataset_from_array(
        x_val,
        y_val,
        sequence_length=sequence_length,
        sampling_rate=step,
        batch_size=batch_size,
    )

    inputs = keras.layers.Input(shape=(inputs.shape[1], inputs.shape[2]))
    lstm_out = keras.layers.LSTM(32)(inputs)
    outputs = keras.layers.Dense(1)(lstm_out)

    model = keras.Model(inputs=inputs, outputs=outputs)
    model.compile(optimizer=keras.optimizers.Adam(learning_rate=learning_rate), loss="mse")
    model.summary()

    history = model.fit(
    dataset_train,
    epochs=epochs,
    validation_data=dataset_val,)       

    for x, y in dataset_val.take(5):
        lstm_helper_show_plot(
            [x[0][:, 1].numpy(), y[0].numpy(), model.predict(x)[0]],
            12,
            "Single Step Prediction",
        )

    return; 


def lstm_helper_normalize(data, train_split):
    data_mean = data[:train_split].mean(axis=0)
    data_std = data[:train_split].std(axis=0)
    return (data - data_mean) / data_std

def lstm_helper_show_plot(plot_data, delta, title):
    labels = ["History", "True Future", "Model Prediction"]
    marker = [".-", "rx", "go"]
    time_steps = list(range(-(plot_data[0].shape[0]), 0))
    if delta:
        future = delta
    else:
        future = 0

    plt.title(title)
    for i, val in enumerate(plot_data):
        if i:
            plt.plot(future, plot_data[i], marker[i], markersize=10, label=labels[i])
        else:
            plt.plot(time_steps, plot_data[i].flatten(), marker[i], label=labels[i])
    plt.legend()
    plt.xlim([time_steps[0], (future + 5) * 2])
    plt.xlabel("Time-Step")
    plt.show()
    return

def main():
    """Main Function"""

    while True:
        print("------Which stock would you like data on?------")
        stock_name = str(input("Please enter it's symbol: "))
        period = str(input("""Please enter the period over which you want the data
                            (1d -> 1 day; 1m -> 1 month; 1y -> 1 year): """))
        interval = str(input("""Please enter the interval between which you want the data
        (1d -> 1 day; 1m -> 1 month; 1y -> 1 year): """))
        # data = get_company_summary(stock_name)
        # print(data)
        stock_data = get_company_data(stock_name, period, interval)
        run_linear_regression(stock_data)
        break
        # ### Visualization Component ###

        # # period = '1d'
        # period = str(input('Enter a period (1d, 1m, 1y): '))
        # # interval = '5m'
        # interval = str(input('Enter an interval (1d, 1m, 1y): '))

        # # stocks = ['MSFT', 'BTC-USD']
        # stocks = input('Enter stock name abbreviation separated by commas (AAPL, GOOG, AMZN): ')
        # stocks = stocks.replace(' ', '').split(',')

        # plot_stocks_df(stocks, period, interval)
        # keyput = str(input("Would You like data on another stock?[press y if yes, otherwise no]"))
        # if keyput != 'y':
        #     break

main()
