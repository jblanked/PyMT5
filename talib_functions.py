import talib
import charts


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


def iRSI(symbol, timeframe, period, applied_price, shift,how_many_bars, year, month, day, testing_type):

    test_type = testing_type.lower()
    price = 0

    if test_type == "control points":
        data_frame = charts.historical_data(symbol, timeframe, shift, how_many_bars)

        # Calculate the RSI using TA-Lib

        if applied_price == "PRICE_CLOSE":
            price = talib.RSI(data_frame['close'], timeperiod=period)

        if applied_price == "PRICE_OPEN":
            price = talib.RSI(data_frame['open'], timeperiod=period)

        if applied_price == "PRICE_LOW":
            price = talib.RSI(data_frame['low'], timeperiod=period)

        if applied_price == "PRICE_HIGH":
            price = talib.RSI(data_frame['high'], timeperiod=period)

    if test_type == "every tick":
        data_frame = charts.tick_data(symbol,year,month,day)

        price = talib.RSI(data_frame['ask'], timeperiod=period)
    
    return price