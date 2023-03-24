"""Test Cases for all functions"""
import os
# import sys
# import project
# sys.path.insert(1, "/Users/aryanmalhotra/Desktop/cs222/course-project-pynance/main")


# HAD TO COPY ALL FUNCTIONS TO BE TESTED
# TILL WE FIND A WAY TO LOAD OTHER MODULES

#   FUNCTIONS

def exists_data(stock_name):
    """Checks if the stock data for a particular company exists"""
    stocks = os.listdir('data/')
    #print(stocks)
    for i in stocks:
        if i == str(stock_name) + ".csv":
            return True
    return False

def exists_info(stock_name):
    """Checks if the stock info for a particular company exists"""

    stocks = os.listdir('info/')
    for i in stocks:
        if i == str(stock_name) + ".txt":
            return True
    return False


#   TESTS

def test_exists_data():
    """Tests the exists_data function"""
    print("Running test_exists()...")
    print(".....\n"*3)
    stock_names = ["GOOG", "AAPL","UAL","VWAGY","TSLA","AMZN"]
    expected_results = [True, False, False, False, True, True]
    actual_results = []
    for i in stock_names:
        result = exists_data(i)
        actual_results.append(result)
    for i in range(6):
        assert actual_results[i] == expected_results[i]
    print("test_exists_data(): ALL ASSERTIONS PASSED")

def test_exists_info():
    """Tests the exists_info function"""
    print("Running test_exists_info()...")
    print(".....\n"*3)
    stock_names = ["GOOG", "AAPL","UAL","VWAGY","TSLA","AMZN"]
    expected_results = [True, True, False, True, False, False]
    actual_results = []
    for i in stock_names:
        result = exists_info(i)
        actual_results.append(result)
    for i in range(6):
        assert actual_results[i] == expected_results[i]
    print("test_exists_info(): ALL ASSERTIONS PASSED")

test_exists_data()
test_exists_info()
