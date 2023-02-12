import MetaTrader5
import MT5functions
import numpy as np


def get_recent_bars(currency, timeframe, shift, starting_bar):
    candle_data = MetaTrader5.copy_rates_from_pos(
        currency, timeframe, shift, starting_bar)  # from previous to current
    return candle_data


class Trend:
    def __init__(self) -> None:
        pass

    def Bearish(self, symbol, timeframe, how_many_candles):
        i = how_many_candles
        while i > 0:
            close_price_past = iClose(symbol, timeframe, i)
            open_price_past = iOpen(symbol, timeframe, i)

            if close_price_past >= open_price_past:
                return False
            i = i - 1
        return True

    def Bullish(self, symbol, timeframe, how_many_candles):
        i = how_many_candles
        while i > 0:
            close_price_past = iClose(symbol, timeframe, i)
            open_price_past = iOpen(symbol, timeframe, i)

            if close_price_past <= open_price_past:
                return False
            i = i - 1
        return True


def prices_recent_bars(currency, timeframe, shift, starting_bar, mode):
    candle_data = get_recent_bars(
        currency, timeframe, shift, starting_bar)
    if mode == "MODE_CLOSE":
        close_prices = [bar[4] for bar in candle_data]  # candle close price
        return close_prices
    if mode == "MODE_LOW":
        low_prices = [bar[3] for bar in candle_data]  # candle low price
        return low_prices
    if mode == "MODE_HIGH":
        high_prices = [bar[2] for bar in candle_data]  # candle high price
        return high_prices
    if mode == "MODE_OPEN":
        open_prices = [bar[1] for bar in candle_data]  # candle open price
        return open_prices
    if mode == "MODE_DATE":
        # datetime in which it was opened
        date_opened = [bar[0] for bar in candle_data]
        return date_opened


def iClose(symbol, timeframe, shift):
    close = prices_recent_bars(symbol, timeframe, shift, 1, "MODE_CLOSE")
    # return info without brackets
    return float(" ".join(str(price) for price in close))


def iLow(symbol, timeframe, shift):
    low = prices_recent_bars(symbol, timeframe, shift, 1, "MODE_LOW")
    # return info without brackets
    return float(" ".join(str(price) for price in low))


def iHigh(currency, timeframe, shift):
    high = prices_recent_bars(currency, timeframe, shift, 1, "MODE_HIGH")
    # return info without brackets
    return float(" ".join(str(price) for price in high))


def iOpen(symbol, timeframe, shift):
    open_price = prices_recent_bars(symbol, timeframe, shift, 1, "MODE_OPEN")
    # return info without brackets
    return float(" ".join(str(price) for price in open_price))


def iDate(symbol, timeframe, shift):
    open_date = prices_recent_bars(symbol, timeframe, shift, 1, "MODE_DATE")
    # return info without brackets
    return float(" ".join(str(price) for price in open_date))


def get_data(symbol, timeframe, shift, starting_bar, applied_price):
    if applied_price == "PRICE_CLOSE":
        return prices_recent_bars(symbol, timeframe, shift, starting_bar, "MODE_CLOSE")
    if applied_price == "PRICE_OPEN":
        return prices_recent_bars(symbol, timeframe, shift, starting_bar, "MODE_OPEN")
    if applied_price == "PRICE_LOW":
        return prices_recent_bars(symbol, timeframe, shift, starting_bar, "MODE_LOW")
    if applied_price == "PRICE_HIGH":
        return prices_recent_bars(symbol, timeframe, shift, starting_bar, "MODE_HIGH")
    return prices_recent_bars(symbol, timeframe, shift, starting_bar, "MODE_CLOSE")


def iMA(symbol, timeframe, moving_average_period, ma_mode, applied_price, shift):

    def SMA(moving_average_period):  # simple moving average
        prices = get_data(symbol, timeframe, shift,
                          moving_average_period, applied_price)
        moving_average = []
        for i in range(len(prices) - moving_average_period + 1):
            moving_average.append(
                sum(prices[i:i + moving_average_period]) / moving_average_period)
        # return info without brackets
        return float(" ".join(str(price) for price in moving_average))

    def EMA(moving_average_period):  # exponential moving average
        prices = get_data(symbol, timeframe, shift,
                          moving_average_period, applied_price)
        ema = []
        alpha = 2 / (moving_average_period + 1)
        ema.append(prices[0])
        for i in range(1, len(prices)):
            ema.append(alpha * prices[i] + (1 - alpha) * ema[i - 1])
        return ema[-moving_average_period:]

    if ma_mode == "MODE_SMA":
        return SMA(moving_average_period)  # simple moving average

    if ma_mode == "MODE_EMA":
        return EMA(moving_average_period)  # exponential moving average


def iRSI(symbol, timeframe, rsi_period, applied_price, shift):
    rsi_period = rsi_period
    prices = get_data(symbol, timeframe, shift, rsi_period, applied_price)
    deltas = np.diff(prices)
    gain = np.where(deltas > 0, deltas, 0)
    loss = np.where(deltas < 0, -deltas, 0)
    avg_gain = np.mean(gain[:rsi_period])
    avg_loss = np.mean(loss[:rsi_period])
    if avg_loss == 0:
        return 100
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))


class FairValueGap:
    def __init__(self) -> None:
        pass

    def trend(self, symbol, timeframe, middle_body_percent, first_body_percent, third_body_percent):
        candle_one_close = iClose(symbol, timeframe, 3)
        candle_two_close = iClose(symbol, timeframe, 2)
        candle_three_close = iClose(symbol, timeframe, 1)

        candle_one_low = iLow(symbol, timeframe, 3)
        candle_two_low = iLow(symbol, timeframe, 2)
        candle_three_low = iLow(symbol, timeframe, 1)

        candle_one_open = iOpen(symbol, timeframe, 3)
        candle_two_open = iOpen(symbol, timeframe, 2)
        candle_three_open = iOpen(symbol, timeframe, 1)

        candle_one_high = iHigh(symbol, timeframe, 3)
        candle_two_high = iHigh(symbol, timeframe, 2)
        candle_three_high = iHigh(symbol, timeframe, 1)

        first_candle_body_length = (
            abs(candle_one_close - candle_one_open)) * MT5functions.Get_Pip_Value(symbol)
        second_candle_body_length = (
            abs(candle_two_close - candle_two_open)) * MT5functions.Get_Pip_Value(symbol)
        third_candle_body_length = (
            abs(candle_three_close - candle_three_open)) * MT5functions.Get_Pip_Value(symbol)

        bullish_candle_one_high_wick_length = (
            abs(candle_one_high - candle_one_close)) * MT5functions.Get_Pip_Value(symbol)

        bullish_candle_two_high_wick_length = (
            abs(candle_two_high - candle_two_close)) * MT5functions.Get_Pip_Value(symbol)
        bearish_candle_two_high_wick_length = (
            abs(candle_two_high - candle_two_open)) * MT5functions.Get_Pip_Value(symbol)

        bearish_candle_three_high_wick_length = (
            abs(candle_three_high - candle_three_open)) * MT5functions.Get_Pip_Value(symbol)

        bearish_candle_one_low_wick_length = (
            abs(candle_one_low - candle_one_close)) * MT5functions.Get_Pip_Value(symbol)

        bullish_candle_two_low_wick_length = (
            abs(candle_two_low - candle_two_open)) * MT5functions.Get_Pip_Value(symbol)
        bearish_candle_two_low_wick_length = (
            abs(candle_two_low - candle_two_close)) * MT5functions.Get_Pip_Value(symbol)

        bullish_candle_three_low_wick_length = (
            abs(candle_three_low - candle_three_open)) * MT5functions.Get_Pip_Value(symbol)

        if (
            # if all three bullish candles
            candle_one_open < candle_one_close and
            candle_two_open < candle_two_close and
            candle_three_open < candle_three_close and

            # and length of first candle's high wick is less than/equal to X% of the 2nd candle's body
            # and the length of the 2nd candle's low wick is less than/equal to X% of the 1st candle's body

            (bullish_candle_one_high_wick_length <= (second_candle_body_length * (middle_body_percent/100))) and
            (bullish_candle_two_low_wick_length <= (first_candle_body_length * (first_body_percent/100))) and

            # and length of third candle's low wick is less than/equal to X% of the 2nd candle's body
            # and the length of the 2nd candle's low wick is less than/equal to X% of the 3rd candle's body

            (bullish_candle_three_low_wick_length <= (second_candle_body_length * (middle_body_percent/100))) and
            (bullish_candle_two_high_wick_length <=
             (third_candle_body_length * (third_body_percent)))
        ):
            return "Buy"

        if (
            # if all three bullish candles
            candle_one_open > candle_one_close and
            candle_two_open > candle_two_close and
            candle_three_open > candle_three_close and

            # and length of first candle's high wick is less than/equal to X% of the 2nd candle's body
            # and the length of the 2nd candle's low wick is less than/equal to X% of the 1st candle's body

            (bearish_candle_one_low_wick_length <= (second_candle_body_length * (middle_body_percent/100))) and
            (bearish_candle_two_high_wick_length <= (first_candle_body_length * (first_body_percent/100))) and

            # and length of third candle's low wick is less than/equal to X% of the 2nd candle's body
            # and the length of the 2nd candle's low wick is less than/equal to X% of the 3rd candle's body

            (bearish_candle_three_high_wick_length <= (second_candle_body_length * (middle_body_percent/100))) and
            (bearish_candle_two_low_wick_length <=
             (third_candle_body_length * (third_body_percent)))
        ):
            return "Sell"

        return ""

    def Bullish_entry(self, symbol, timeframe, middle_body_percent, first_body_percent, third_body_percent):
        if FairValueGap.trend(self, symbol, timeframe, middle_body_percent, first_body_percent, third_body_percent) == "Buy":
            return iLow(symbol, timeframe, 2)

    def Bearish_entry(self, symbol, timeframe, middle_body_percent, first_body_percent, third_body_percent):
        if FairValueGap.trend(self, symbol, timeframe, middle_body_percent, first_body_percent, third_body_percent) == "Sell":
            return iHigh(symbol, timeframe, 2)

    def Bullish_SL(self, symbol, timeframe, middle_body_percent, first_body_percent, third_body_percent):
        if FairValueGap.trend(self, symbol, timeframe, middle_body_percent, first_body_percent, third_body_percent) == "Buy":
            return iLow(symbol, timeframe, 3)

    def Bearish_SL(self, symbol, timeframe, middle_body_percent, first_body_percent, third_body_percent):
        if FairValueGap.trend(self, symbol, timeframe, middle_body_percent, first_body_percent, third_body_percent) == "Sell":
            return iHigh(symbol, timeframe, 3)

    def Bullish_TP(self, symbol, timeframe, middle_body_percent, first_body_percent, third_body_percent):
        if FairValueGap.trend(self, symbol, timeframe, middle_body_percent, first_body_percent, third_body_percent) == "Buy":
            return iHigh(symbol, timeframe, 1)

    def Bearish_TP(self, symbol, timeframe, middle_body_percent, first_body_percent, third_body_percent):
        if FairValueGap.trend(self, symbol, timeframe, middle_body_percent, first_body_percent, third_body_percent) == "Sell":
            return iLow(symbol, timeframe, 1)


class Doji:
    def __init__(self) -> None:
        pass

    def trend(self, symbol, timeframe, doji_body_within_pipss, doji_wick_within_pipss, doji_wick_lengths):
        open_price = iOpen(symbol, timeframe, 1)
        close_price = iClose(symbol, timeframe, 1)

        combined_prices = (abs(open_price - close_price)) * \
            MT5functions.Get_Pip_Value(symbol)

        high_price = iHigh(symbol, timeframe, 1)
        low_price = iLow(symbol, timeframe, 1)

        distance_high_buy_candle = (
            abs(high_price-close_price)) * MT5functions.Get_Pip_Value(symbol)
        distance_low_buy_candle = (
            abs(open_price-low_price)) * MT5functions.Get_Pip_Value(symbol)

        distance_high_sell_candle = (
            abs(high_price-open_price)) * MT5functions.Get_Pip_Value(symbol)
        distance_low_sell_candle = (
            abs(close_price-low_price)) * MT5functions.Get_Pip_Value(symbol)

        combined_distance_buys = distance_high_buy_candle-distance_low_buy_candle
        combined_distance_sells = distance_high_sell_candle-distance_low_sell_candle

        doji_body_within_pips = doji_body_within_pipss * \
            MT5functions.Get_Pip_Value(symbol)
        doji_wick_within_pips = doji_wick_within_pipss * \
            MT5functions.Get_Pip_Value(symbol)
        doji_wick_length = doji_wick_lengths * \
            MT5functions.Get_Pip_Value(symbol)

        if (
            combined_distance_buys <= doji_wick_within_pips and
            distance_high_buy_candle >= doji_wick_length and
            distance_low_buy_candle >= doji_wick_length and
            combined_prices <= doji_body_within_pips
        ):
            # bullish doji candle
            return "Buy"

        if (
            combined_distance_sells <= doji_wick_within_pips and
            distance_high_sell_candle >= doji_wick_length and
            distance_low_sell_candle >= doji_wick_length and
            combined_prices <= doji_body_within_pips
        ):
            # bearish doji candle
            return "Sell"

    def Bullish_entry(self, symbol, timeframe, doji_body_within_pipss, doji_wick_within_pipss, doji_wick_lengths):
        if Doji.trend(self, symbol, timeframe, doji_body_within_pipss, doji_wick_within_pipss, doji_wick_lengths) == "Buy":
            return iOpen(symbol, timeframe, 1)

    def Bearish_entry(self, symbol, timeframe, doji_body_within_pipss, doji_wick_within_pipss, doji_wick_lengths):
        if Doji.trend(self, symbol, timeframe, doji_body_within_pipss, doji_wick_within_pipss, doji_wick_lengths) == "Sell":
            return iOpen(symbol, timeframe, 1)

    def Bullish_SL(self, symbol, timeframe, doji_body_within_pipss, doji_wick_within_pipss, doji_wick_lengths):
        if Doji.trend(self, symbol, timeframe, doji_body_within_pipss, doji_wick_within_pipss, doji_wick_lengths) == "Buy":
            return iLow(symbol, timeframe, 1)

    def Bearish_SL(self, symbol, timeframe, doji_body_within_pipss, doji_wick_within_pipss, doji_wick_lengths):
        if Doji.trend(self, symbol, timeframe, doji_body_within_pipss, doji_wick_within_pipss, doji_wick_lengths) == "Sell":
            return iHigh(symbol, timeframe, 1)


class DoubleFlat:
    def __init__(self) -> None:
        pass

    def trend(self, symbol, timeframe, body_match_pipss, wick_lengths):

        firstclose = iClose(symbol, timeframe, 2)
        secondclose = iClose(symbol, timeframe, 1)

        firstopen = iOpen(symbol, timeframe, 2)
        secondopen = iOpen(symbol, timeframe, 1)

        firsthigh = iHigh(symbol, timeframe, 2)
        secondhigh = iHigh(symbol, timeframe, 1)

        firstlow = iLow(symbol, timeframe, 2)
        secondlow = iLow(symbol, timeframe, 1)

        wick_length = wick_lengths * MT5functions.Get_Pip_Value(symbol)
        body_match_pips = body_match_pipss * MT5functions.Get_Pip_Value(symbol)

        candle_body_match_length = (
            abs(firstclose-secondopen)) * MT5functions.Get_Pip_Value(symbol)

        wick_down_double_bottom_bearish_length = (
            abs(firstclose-firstlow)) * MT5functions.Get_Pip_Value(symbol)

        wick_down_double_bottom_bullish_length = (
            abs(secondopen - secondlow)) * MT5functions.Get_Pip_Value(symbol)

        wick_down_double_top_bullish_length = (
            abs(firsthigh-firstclose)) * MT5functions.Get_Pip_Value(symbol)

        wick_down_double_top_bearish_length = (
            abs(secondhigh-secondopen)) * MT5functions.Get_Pip_Value(symbol)

        if (
            (candle_body_match_length <= body_match_pips) and
            (secondclose >= secondopen) and
            (firstopen > firstclose) and
            (wick_down_double_bottom_bullish_length <= wick_length) and
            (wick_down_double_bottom_bearish_length <= wick_length)
        ):
            return "Buy"

        if (
            (candle_body_match_length <= body_match_pips) and
            (secondclose <= secondopen) and
            (firstopen < firstclose) and
            (wick_down_double_top_bullish_length <= wick_length) and
            (wick_down_double_top_bearish_length <= wick_length)
        ):
            return "Sell"

    def Bullish_entry(self, symbol, timeframe, body_match_pipss, wick_lengths):
        if DoubleFlat.trend(self, symbol, timeframe, body_match_pipss, wick_lengths) == "Buy":
            return iOpen(symbol, timeframe, 1)

    def Bearish_entry(self, symbol, timeframe, body_match_pipss, wick_lengths):
        if DoubleFlat.trend(self, symbol, timeframe, body_match_pipss, wick_lengths) == "Sell":
            return iOpen(symbol, timeframe, 1)

    def Bullish_SL(self, symbol, timeframe, body_match_pipss, wick_lengths):
        if DoubleFlat.trend(self, symbol, timeframe, body_match_pipss, wick_lengths) == "Buy":
            if iLow(symbol, timeframe, 2) < iLow(symbol, timeframe, 1):
                return iLow(symbol, timeframe, 2)
            if iLow(symbol, timeframe, 2) > iLow(symbol, timeframe, 1):
                return iLow(symbol, timeframe, 1)

    def Bearish_SL(self, symbol, timeframe, body_match_pipss, wick_lengths):
        if DoubleFlat.trend(self, symbol, timeframe, body_match_pipss, wick_lengths) == "Sell":
            if iHigh(symbol, timeframe, 2) < iHigh(symbol, timeframe, 1):
                return iHigh(symbol, timeframe, 1)
            if iHigh(symbol, timeframe, 2) > iHigh(symbol, timeframe, 1):
                return iHigh(symbol, timeframe, 2)
