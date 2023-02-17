import time
import pandas as pd
import MetaTrader5
import numpy as np
import matplotlib.pyplot as plt
import pytz


def historical_data(symbol, timeframe, current_bar, how_many_bars):

    # Get the historical data for the symbol and timeframe
    rates = MetaTrader5.copy_rates_from_pos(
        symbol, timeframe, current_bar, how_many_bars)

    # Convert the data to a pandas DataFrame
    df = pd.DataFrame(rates)

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

    # convert the Unix timestamps to pandas datetime objects
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


def plot(symbol, timeframe, applied_price, amount_of_bars):
    while True:
        plot_chart(symbol, timeframe, applied_price, amount_of_bars)
        time.sleep(1)
