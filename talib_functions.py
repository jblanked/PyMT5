import talib
import MetaTrader5 as mt5
import pandas as pd


# on windows i went to
# https://www.lfd.uci.edu/~gohlke/pythonlibs/#ta-lib
# and downloaded TA_Lib-0.4.24-cp39-cp39-win_amd64.whl
# the moved the wheel to a folder
# then opened up command prompt and opened that folder
# then i used pip install TA_Lib-0.4.24-cp39-cp39-win_amd64.whl

# on mac I just used homebrew
# this command in terminal: brew install ta-lib
# then used python3 -m pip install TA-Lib

# i only defined RSI but they have a long list of indicators
# read more about it: https://github.com/TA-Lib/ta-lib-python


def historical_data(symbol, timeframe, current_bar, how_many_bars):

    # Get the historical data for the symbol and timeframe
    rates = mt5.copy_rates_from_pos(
        symbol, timeframe, current_bar, how_many_bars)

    # Convert the data to a pandas DataFrame
    df = pd.DataFrame(rates)

    return df


def iRSI(symbol, timeframe, period, applied_price, shift):

    data_frame = historical_data(symbol, timeframe, shift, 100)

    # Calculate the RSI using TA-Lib

    if applied_price == "PRICE_CLOSE":
        rsi = talib.RSI(data_frame['close'], timeperiod=period)

    if applied_price == "PRICE_OPEN":
        rsi = talib.RSI(data_frame['open'], timeperiod=period)

    if applied_price == "PRICE_LOW":
        rsi = talib.RSI(data_frame['low'], timeperiod=period)

    if applied_price == "PRICE_HIGH":
        rsi = talib.RSI(data_frame['high'], timeperiod=period)

    rsi_price = rsi[99]

    return rsi_price
