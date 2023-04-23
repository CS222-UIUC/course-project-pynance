import dearpygui
import dearpygui.dearpygui as dpg
import project
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import mplfinance as mpf
import yfinance as yf
import datetime
import matplotlib.pyplot as plt

dpg.create_context()


def show_data(sender, data):
    inputvalue = dpg.get_value("ticker1")
    period = dpg.get_value("period1")
    interval = dpg.get_value("interval1")
    dpg.delete_item("Primary Window")
    with dpg.window(tag = "Data"):
        dpg.set_primary_window("Data", True)
        comdata = project.get_company_data(inputvalue,period,interval)
        dpg.add_text(comdata)
        dpg.add_button(tag = "return3",label = "Return", callback = returnmenu)

def show_vis(sender, data):
    inputvalue = dpg.get_value("ticker3")
    period = dpg.get_value("period3")
    interval = dpg.get_value("interval3")
    hist = project.get_company_data(inputvalue,period,interval)

    
    date =  [float(10 + i*(600/len(hist))) for i in range(len(hist))]
    opens = hist["Open"].to_list()
    open = [float(x) for x in opens]
    closes = hist["Close"].to_list()
    close = [float(x) for x in closes]
    lows = hist["Low"].to_list()
    low = [float(x) for x in lows]
    highs = hist["High"].to_list()
    high = [float(x) for x in highs]

    dpg.delete_item("Primary Window")
    with dpg.window(tag = "Visualization"):
        dpg.set_primary_window("Visualization", True)
        with dpg.plot(label="CandlePlot", width=-1, height=-1) as plot_id:
            dpg.add_plot_legend()
            dpg.add_plot_axis(dpg.mvXAxis, tag="Dates", time=True)
            
            dpg.add_plot_axis(dpg.mvYAxis, tag="Prices")
            
            dpg.add_candle_series(dates=date,opens=open, highs=high, lows=low, closes=close, label="Candlesticks",
                              parent=dpg.last_item())

def show_summ(sender, data):
    inputvalue = dpg.get_value("ticker2")
    dpg.delete_item("Primary Window")
    with dpg.window(tag = "Summary"):
        dpg.set_primary_window("Summary", True)
        summary = project.get_company_summary(inputvalue)
        dpg.add_text(summary)
        dpg.add_button(tag = "return2",label = "Return", callback = returnmenu)


def mainmenu():
    with dpg.window(tag="Primary Window"):
        dpg.set_primary_window("Primary Window", True)
        dpg.add_text("Welcome to Pynance")
        with dpg.tab_bar():
            with dpg.tab(label="Data"):
                dpg.add_text("Enter the Ticker, Period, and Interval for the stock below")
                dpg.add_input_text(tag = "ticker1")
                dpg.add_input_text(tag = "period1")
                dpg.add_input_text(tag = "interval1")
                dpg.add_button(tag = "submit2", label = "Submit", callback = show_data)

            with dpg.tab(label="Summary"):
                dpg.add_text("Enter the ticker for the stock below")
                dpg.add_input_text(tag = "ticker2")
                dpg.add_button(tag = "submit1", label = "Submit", callback = show_summ)

            with dpg.tab(label="Visualization"):
                dpg.add_text("Enter the Ticker, Period, and Interval for the stock below")
                dpg.add_input_text(tag = "ticker3")
                dpg.add_input_text(tag = "period3")
                dpg.add_input_text(tag = "interval3")
                dpg.add_button(tag = "submit3", label = "Submit", callback = show_vis)
            with dpg.tab(label="Prediction"):
                dpg.add_text("Enter the Ticker, Period, and Interval for the stock below")




def returnmenu(sender):
    dpg.delete_item("Data")
    dpg.delete_item("Visualization")
    dpg.delete_item("Summary")
    with dpg.window(tag="Primary Window"):
        dpg.set_primary_window("Primary Window", True)
        dpg.add_text("Welcome to Pynance")
        with dpg.tab_bar():
            with dpg.tab(label="Data"):
                dpg.add_text("Enter the Ticker, Period, and Interval for the stock below")
                dpg.add_input_text(tag = "ticker1")
                dpg.add_input_text(tag = "period1")
                dpg.add_input_text(tag = "interval1")
                dpg.add_button(tag = "submit2", label = "Submit", callback = show_data)

            with dpg.tab(label="Summary"):
                dpg.add_text("Enter the ticker for the stock below")
                dpg.add_input_text(tag = "ticker2")
                dpg.add_button(tag = "submit1", label = "Submit", callback = show_summ)

            with dpg.tab(label="Visualization"):
                dpg.add_text("Enter the Ticker, Period, and Interval for the stock below")
                dpg.add_input_text(tag = "ticker3")
                dpg.add_input_text(tag = "period3")
                dpg.add_input_text(tag = "interval3")
                dpg.add_button(tag = "submit3", label = "Submit", callback = show_vis)
            with dpg.tab(label="Prediction"):
                dpg.add_text("Enter the Ticker, Period, and Interval for the stock below")


mainmenu()

dpg.create_viewport(title='PyNance', width=900, height=900)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("Primary Window", True)
dpg.start_dearpygui()
dpg.destroy_context()