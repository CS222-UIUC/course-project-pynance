# course-project-pynance

# Introduction

Project Name - Pynance 

Investors, traders, and other people interested in the stock market need to look up the data for a particular stock in the United States. With Pynance, users can look up information, visualize stock data, and predict the future stock price for a company before making any investments.

Functionality

1) Users will receive a description of the company when looking up a stock.
2) Users can see the most recent record of a company’s stock
3) Users have access to a visualization of the trends of stock prices
4) Users will be able to see predictions for future stock prices
5) Proper GUI through either terminal and website for prediction and visualization.

Alternatives and Precedents

There exist few financial visualization applications and services that implement statistical frameworks that allow for prediction on previously seen data. Our take on the project was to build and test such models so as to provide this missing prediction component, and to build a refined visualization and an interface on the side so as to provide a tangible evidence of its accuracy.

# Technical Architecture

1) Frontend (Website, GUI, Terminal): Initially we used the terminal to display results. For our stretch goals, we created a basic website that sends requests to the backends and displays the result. (uses dearpygui)
2) yfinance API: interacts with the visualization and prediction component because it provides the data.
3) Visualization displays trends and graphs for stock analysis (uses Matplotlib.pyplot)
4) Prediction runs linear regression to get predicted values (uses sklearn, pandas, finance, mplfinance)


# Installation Instructions

** Run the following commands for prediction and visualization functionality:

1) pip install yfinance
2) pip install pandas
3) pip install mplfinance
4) pip install scikit
5) pip install requests

** Run the following command for GUI:

pip install dearpygui

** Run the following for setting up the website:

1) Install NodeJS
2) npm install
3) npm i

# Work Distribution
  
1) Aryan Malhotra: Frontend (Website and Terminal), Linear Regression Prediction and Analysis, Yfinance and Finnhub APIs
2) Jose Ines Martinez: Linear Regression Analysis and Visualization, Yfinance APIs
3) Julian Marquez: Frontend (Terminal and GUI), Yfinance APIs, Linear Regression Analysis
4) Nikhita Punati: Linear Regression Prediction, Analysis, and Visualization
