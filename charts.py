import time
import pandas as pd
import MetaTrader5
import numpy as np
import matplotlib.pyplot as plt
import pytz
from datetime import datetime
import matplotlib.animation as animation


def historical_data(symbol, timeframe, current_bar, how_many_bars):

    # Get the historical data for the symbol and timeframe
    rates = MetaTrader5.copy_rates_from_pos(
        symbol, timeframe, current_bar, how_many_bars)

    # Convert the data to a pandas DataFrame
    df = pd.DataFrame(rates)

    return df

def tick_data(symbol, year, month, day):

    # set time zone to UTC
    timezone = pytz.timezone("Etc/UTC")

    # create 'datetime' objects in UTC time zone to avoid the implementation of a local time zone offset
    utc_from = datetime(year, month, day, tzinfo=timezone) 

    now = datetime.now()

    # Get the tick data for the symbol
    ticks = MetaTrader5.copy_ticks_range(
        symbol, utc_from, now, MetaTrader5.COPY_TICKS_ALL)

    # Convert the data to a pandas DataFrame
    df = pd.DataFrame(ticks)

    return df

def plot_chart(symbol, timeframe, applied_price, amount_of_bars):
    chart_data = historical_data(symbol, timeframe, 0, amount_of_bars)

    if applied_price == "PRICE_CLOSE":
        final_data = chart_data['close']
        plt.title(f"{symbol} Close Prices")

    if applied_price == "PRICE_HIGH":
        final_data = chart_data['high']
        plt.title(f"{symbol} High Prices")

    if applied_price == "PRICE_LOW":
        final_data = chart_data['low']
        plt.title(f"{symbol} Low Prices")

    if applied_price == "PRICE_OPEN":
        final_data = chart_data['open']
        plt.title(f"{symbol} Open Prices")

    # convert the Unix timestamps to pandas datetime objecsts
    data_time = chart_data['time']
    edited_time = pd.to_datetime(data_time, unit='s')

    # localize the pandas datetime objects to the UTC timezone
    localized_time = edited_time.dt.tz_localize('UTC')

    # convert the localized pandas datetime objects to datetime objects with timezone information
    new_time = localized_time.dt.tz_convert(pytz.utc)

    array = np.array([final_data]).flatten()

    if 'line' not in plt.gca().__dict__:
        plt.gca().__dict__['line'], = plt.plot(new_time, array)
    else:
        plt.gca().line.set_data(new_time, array)
    plt.pause(1)  # pause the plot for 1 second
    return True


def plot_candles(num, symbol, timeframe, how_many_bars, ax):
    ax.clear()
    prices = historical_data(symbol, timeframe, 0, how_many_bars)

    # define width of candlestick elements
    width = .4
    width2 = .05

    # define up and down prices
    up = prices[prices['close']>=prices['open']]
    down = prices[prices['close']<prices['open']]

    # convert the Unix timestamps to pandas datetime objects
    data_time = prices['time']
    edited_time = pd.to_datetime(data_time, unit='s')

    # localize the pandas datetime objects to the UTC timezone
    localized_time = edited_time.dt.tz_localize('UTC')

    # convert the localized pandas datetime objects to datetime objects with timezone information
    new_time = localized_time.dt.tz_convert(pytz.utc)

    # define colors to use
    col1 = 'green'
    col2 = 'red'

    # plot up prices
    ax.bar(up.index,up['close']-up['open'],width,bottom=up['open'],color=col1)
    ax.bar(up.index,up['high']-up['close'],width2,bottom=up['close'],color=col1)
    ax.bar(up.index,up['low']-up['open'],width2,bottom=up['open'],color=col1)

    # plot down prices
    ax.bar(down.index,down['close']-down['open'],width,bottom=down['open'],color=col2)
    ax.bar(down.index,down['high']-down['open'],width2,bottom=down['open'],color=col2)
    ax.bar(down.index,down['low']-down['close'],width2,bottom=down['close'],color=col2)

    ax.set_facecolor("#2E2E2E")

    # rotate x-axis tick labels
    plt.xticks(rotation=45, ha='right')

    plt.title(f"{symbol}")



def candlestick_chart(symbol, timeframe, how_many_bars):
    fig, ax = plt.subplots()
    animate = animation.FuncAnimation(fig, plot_candles, fargs=[symbol, timeframe, how_many_bars, ax], interval=1000, save_count=how_many_bars)
    plt.show()


def price_chart(symbol, timeframe, applied_price, amount_of_bars):
    while True:
        plot_chart(symbol, timeframe, applied_price, amount_of_bars)
        time.sleep(1)

def tick_chart(symbol, year, month, day):
    while True:
        plot_ticks(symbol, year, month, day)
        time.sleep(1)
