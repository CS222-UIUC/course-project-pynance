"""Test Cases for all functions"""
import math
import project
#   TESTS

def test_exists_data():
    """Tests the exists_data function"""
    print("Running test_exists()...")
    print(".....\n"*3)
    stock_names = ["GOOG", "AAPL","MSFT","VWAGY","TSLA","AMZN"]
    expected_results = [True, True, True, True, True, True]
    actual_results = []
    for i in stock_names:
        result = project.exists_data(i, "5y", "1d")
        if not result:
            result = project.exists_data(i, "10y", "1d")
        actual_results.append(result)
    for i in range(6):
        assert actual_results[i] == expected_results[i]
    print("....."*3)
    print("test_exists_data(): ALL ASSERTIONS PASSED")

def test_exists_info():
    """Tests the exists_info function"""
    print("Running test_exists_info()...")
    print("....."*3)
    stock_names = ["GOOG", "AAPL","UAL","VWAGY","TSLA","AMZN"]
    expected_results = [True, True, False, True, False, True]
    actual_results = []
    for i in stock_names:
        result = project.exists_info(i)
        actual_results.append(result)
    for i in range(6):
        assert actual_results[i] == expected_results[i]
    print("....."*3)
    print("test_exists_info(): ALL ASSERTIONS PASSED")

def test_regression_plots():
    """
    Tests the Scatter Plot for the Linear Regression Model generated
    for Google, Apple, United Airlines, Volkswagen, Tesla, and Amazon
    """
    print("Running test_regression_plots()...")
    print(".....\n"*3)
    stock_names = ["GOOG", "AAPL","UAL","VWAGY","TSLA","AMZN"]
    for i in stock_names:
        stock_data = project.get_company_data(i, "5y", "1d")
        model, test_x, test_y = project.run_linear_regression(stock_data)
        predicted=model.predict(test_x)
        dfr=project.pd.DataFrame({'Actual_Price':test_y, 'Predicted_Price':predicted})
        project.plt.scatter(dfr.Actual_Price, dfr.Predicted_Price,  color='Darkblue')
        project.plt.xlabel("Actual Price")
        project.plt.ylabel("Predicted Price")
        #Check if the plot has been created / is not null
        plot = project.plt.gcf()
        assert plot
        #Check if the actual Closing Prices are close to the expected Close Prices
        #Basically the same as the model results,
        #but this allows for points over the individual tolerance to be plotted
        #as long as more than 95% of the points are within the tolerance
        count_within_tol = 0
        for j, (actual, pred) in enumerate(zip(test_y, predicted)):
            if math.isclose(actual, pred, rel_tol=0.05):
                count_within_tol += 1
            j = j + 1 - 1
        assert count_within_tol/len(test_y) >= 0.95
        print("test_regression_plots_" + i + ": ALL ASSERTIONS PASSED")
    print("....."*3)
    print("test_regression_plots(): ALL ASSERTIONS PASSED")

def test_regression():
    """
    Tests Linear Regression Model for Google, Apple,
    United Airlines, Volkswagen, Tesla, and Amazon
    """
    print("Running test_regression()...")
    print(".....\n"*3)
    stock_names = ["GOOG", "AAPL","UAL","VWAGY","TSLA","AMZN"]
    for i in stock_names:
        stock_data = project.get_company_data(i, "5y", "1d")
        model, test_x, test_y = project.run_linear_regression(stock_data)
        y_pred = model.predict(test_x)
        for pred, exp in zip(y_pred, test_y):
            assert math.isclose(pred, exp, rel_tol=0.05) #Model works within 5% tolerance
        #Score should be greater than 95%
        assert math.isclose(model.score(test_x, test_y), 1, rel_tol=0.05)
        print("test_regression_" + i + ": ALL ASSERTIONS PASSED")
    print("....."*3)
    print("test_regression(): ALL ASSERTIONS PASSED")

def execute_all_tests():
    """Executes tests for all functionalities"""
    test_exists_data()
    test_exists_info()
    test_regression_plots()
    test_regression()


execute_all_tests()
