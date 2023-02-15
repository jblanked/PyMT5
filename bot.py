import trend
import ordersettings
import login
import password as p
import sys
import MT5functions


# account number as integer
# I stored mine in a separate password.py
account_number = p.number()

# account number as string
# I stored mine in a separate password.py
account_password = p.password()  # password

broker_server_name = "Osprey-Demo"  # broker name


# login to your account on MT5 and obtain data
if __name__ == '__main__':
    login.MT5_login(account_number,
                    account_password, broker_server_name)


# checks if your account name is allowed (change in MT5functions.py)
if not trend.MT5functions.Expiry_name():
    sys.exit("You are not allowed to use this EA")


# choose which strategies you want to use
use_moving_average = True
use_fair_value_gap = False
use_doji = False
use_double_flat = False
use_daily_range = False


currency_pair = "US30.mini"  # currency pair to trade

# attempt to enable the display of the symbol in MarketWatch
selected = trend.MetaTrader5.symbol_select(currency_pair,True)
if not selected:
    print(f"Failed to select {currency_pair}, error code = {trend.MetaTrader5.last_error()}")


# changed integer to your time frame (its in minutes)
time_frame = trend.MT5functions.timeframe(1)

order_type_buy = "buy"  # buy market execution order
order_type_sell = "sell"  # sell market execution order
order_type_buy_limit = "buy limit"  # buy limit order
order_type_sell_limit = "sell limit"  # sell lmit order

price = "ask"  # entry price if buying via market execution
price2 = "bid"  # entry price if selling via market execution

use_risk = True  # use percent risk?
risk = 1.00  # risk percent
use_lot_size = False  # use lot size?
lotsizes = 0.05  # lot size
stoploss = 25  # stop loss
takeprofit = 100  # take profit


use_time = False  # use custom trading hours?
start_time = "08:00"  # start time (server time)
stop_time = "16:49"  # stop time (server time)

ordercomment = "Python Test"  # order comment
magicnumber = 899811  # magic number

magicnumber1 = magicnumber + 1
magicnumber2 = magicnumber + 2
magicnumber3 = magicnumber + 3
magicnumber4 = magicnumber + 4
magicnumber5 = magicnumber + 5


# moving average settings
ma_period = 10  # moving average period
ma_applied_price = "PRICE_CLOSE"  # moving average applied price
ma_mode = "MODE_SMA"  # moving average mode
ma_shift = 0  # moving average shift (bars away)


# rsi settings
rsi_period = 7  # rsi period
rsi_applied_price = "PRICE_CLOSE"  # rsi applied price
rsi_shift = 0  # rsi shift (bars away)


# fair value gap settings
middlebodypercent = 10  # 1st/3rd wick less/more than x% of 2nd candle body
firstbodypercent = 10  # 2nd wick less/more than x% of 1st candle body
thirdbodypercent = 10  # 2nd wick less/more than x% of 3rd candle body

# doji settings
doji_body_pips = 1.0  # Body lengnth <= X pips
doji_wick_pips = 1.0  # Difference of both wick lengths <= X pips
doji_wickk_length = 1.0  # Both Wick length's >= X pips

# double flat settings
pip_cushion = 1.0  # pip cushion (double flat within pip range)
double_flat_wick_length = 2.0  # wick length <= X

"======= GRID SETTINGS ======="
use_martingale = True # Use grid?
martinactivate= 1 # Pips in between order and to start
marrtinTP = 1 # new take profit (pips increase/decrease from open price)
maxtrades = 1 # max amount of trades
martinMULTI = 1.5 # Order multiplier


# lot size for stop loss in pips
lotsize = trend.MT5functions.Get_Risk(
    use_risk, use_lot_size, risk, stoploss, lotsizes, currency_pair)

# declared the Doubleflat class as a variable
double_flat_object = trend.DoubleFlat()

# declared the FVG class as a vairable
fair_value_gap_object = trend.FairValueGap()

doji_object = trend.Doji()  # declared the Doji class as a variable


def DoubleFlat_prices(bullish_or_bearish, which_position):

    decision = bullish_or_bearish.lower()
    position = which_position.lower()

    if decision == "bullish":
        if position == "entry":
            # double flat bullish entry
            return double_flat_object.Bullish_entry(
                currency_pair,
                time_frame,
                pip_cushion,
                double_flat_wick_length)

        if position == "stop loss":
            # double flat bullish SL
            return double_flat_object.Bullish_SL(
                currency_pair,
                time_frame,
                pip_cushion,
                double_flat_wick_length)

    if decision == "bearish":
        if position == "entry":
            # double flat bearish entry
            return double_flat_object.Bearish_entry(
                currency_pair,
                time_frame,
                pip_cushion,
                double_flat_wick_length)

        if position == "stop loss":
            # double flat bearish SL
            return double_flat_object.Bearish_SL(
                currency_pair,
                time_frame,
                pip_cushion,
                double_flat_wick_length)


def Doji_prices(bullish_or_bearish, which_position):

    decision = bullish_or_bearish.lower()
    position = which_position.lower()

    if decision == "bullish":
        if position == "entry":
            # doji bullish entry
            return doji_object.Bullish_entry(
                currency_pair,
                time_frame,
                doji_body_pips,
                doji_wick_pips,
                doji_wickk_length)

        if position == "stop loss":
            # doji bullish SL
            return doji_object.Bullish_SL(
                currency_pair,
                time_frame,
                doji_body_pips,
                doji_wick_pips,
                doji_wickk_length)

    if decision == "bearish":
        if position == "entry":
            # doji bearish entry
            return doji_object.Bearish_entry(
                currency_pair,
                time_frame,
                doji_body_pips,
                doji_wick_pips,
                doji_wickk_length)

        if position == "stop loss":
            # doji bearish SL
            return doji_object.Bearish_SL(
                currency_pair,
                time_frame,
                doji_body_pips,
                doji_wick_pips,
                doji_wickk_length)


def FVG_prices(bullish_or_bearish, which_position):

    decision = bullish_or_bearish.lower()
    position = which_position.lower()

    if decision == "bullish":
        if position == "entry":
            # fair value gap bullish entry
            return fair_value_gap_object.Bullish_entry(
                currency_pair,
                time_frame,
                middlebodypercent,
                firstbodypercent,
                thirdbodypercent)
        if position == "stop loss":
            # fair value gap bullish SL
            return fair_value_gap_object.Bullish_SL(
                currency_pair,
                time_frame,
                middlebodypercent,
                firstbodypercent,
                thirdbodypercent)
        if position == "take profit":
            # fair value gap bullish TP
            return fair_value_gap_object.Bullish_TP(
                currency_pair,
                time_frame,
                middlebodypercent,
                firstbodypercent,
                thirdbodypercent)

    if decision == "bearish" and position == "entry":
        # fair value gap bearish entry
        return fair_value_gap_object.Bearish_entry(
            currency_pair,
            time_frame,
            middlebodypercent,
            firstbodypercent,
            thirdbodypercent)

    if decision == "bearish" and position == "stop loss":
        # fair value gap bearish SL
        return fair_value_gap_object.Bearish_SL(
            currency_pair,
            time_frame,
            middlebodypercent,
            firstbodypercent,
            thirdbodypercent)

    if decision == "bearish" and position == "take profit":
        # fair value gap bearish TP
        return fair_value_gap_object.Bearish_TP(
            currency_pair,
            time_frame,
            middlebodypercent,
            firstbodypercent,
            thirdbodypercent)

# trading configurations


class Trade:

    def __init__(self) -> None:
        pass

    def FairValueGap(self):
        # this one will buy if there's a bullish fair value gap
        # and sell if there's a bearish fair value gap
        if not trend.MT5functions.check_if_order_opened(currency_pair, magicnumber4):
            if fair_value_gap_object.trend(currency_pair,
                                           time_frame,
                                           middlebodypercent,
                                           firstbodypercent, ~
                                           thirdbodypercent) == "Buy":

                ordersettings.OrderSend(currency_pair, order_type_buy_limit, lotsize, FVG_prices("bullish", "entry"), 0, True,
                                        FVG_prices("bullish", "stop loss"), True, FVG_prices("bullish", "take profit"), ordercomment, magicnumber4)
                # print(
                #    f"Bullish Fair Value gap... Buying {currency_pair} at {FVG_bullish_entry}")

            if fair_value_gap_object.trend(currency_pair,
                                           time_frame,
                                           middlebodypercent,
                                           firstbodypercent,
                                           thirdbodypercent) == "Sell":

                ordersettings.OrderSend(currency_pair, order_type_sell_limit, lotsize, FVG_prices("bearish", "entry"),
                                        0, True, FVG_prices("bearish", "stop loss"), True, FVG_prices("bearish", "take profit"), ordercomment, magicnumber4)

    def DoubleFlat(self):
        # this one will buy if there's a bullish Double flat bottom
        # and sell if theres a bearish double flat top
        if not trend.MT5functions.check_if_order_opened(currency_pair, magicnumber3):
            if double_flat_object.trend(currency_pair,
                                        time_frame,
                                        pip_cushion,
                                        double_flat_wick_length) == "Buy":

                ordersettings.OrderSend(currency_pair, order_type_buy_limit, lotsize, DoubleFlat_prices("bullish", "entry"), 0, True,
                                        DoubleFlat_prices("bullish", "stop loss"), False, takeprofit, ordercomment, magicnumber3)

            if double_flat_object.trend(currency_pair,
                                        time_frame,
                                        pip_cushion,
                                        double_flat_wick_length) == "Sell":

                ordersettings.OrderSend(currency_pair, order_type_buy_limit, lotsize, DoubleFlat_prices("bearish", "entry"), 0, True,
                                        DoubleFlat_prices("bearish", "stop loss"), False, takeprofit, ordercomment, magicnumber3)

    def Doji(self):
        # this one will buy if there's a bullish Doji candle
        # and sell if there's a bearish doji candle
        if not trend.MT5functions.check_if_order_opened(currency_pair, magicnumber2):
            if doji_object.trend(currency_pair,
                                 time_frame,
                                 doji_body_pips,
                                 doji_wick_pips,
                                 doji_wickk_length) == "Buy":
                ordersettings.OrderSend(currency_pair, order_type_buy_limit, lotsize, Doji_prices("bullish", "entry"), 0, True,
                                        Doji_prices("bullish", "stop loss"), False, takeprofit, ordercomment, magicnumber2)

            if doji_object.trend(currency_pair,
                                 time_frame,
                                 doji_body_pips,
                                 doji_wick_pips,
                                 doji_wickk_length) == "Sell":
                ordersettings.OrderSend(currency_pair, order_type_buy_limit, lotsize, Doji_prices("bearish", "entry"), 0, True,
                                        Doji_prices("bearish", "stop loss"), False, takeprofit, ordercomment, magicnumber2)

    def MovingAverage(self):
        # this will buy if price is above the moving average
        # and sell if price is below the moving average
        ask_price = trend.MetaTrader5.symbol_info_tick(
            currency_pair).ask  # getting the ask price
        bid_price = trend.MetaTrader5.symbol_info_tick(
            currency_pair).bid  # getting the bid price
        if not trend.MT5functions.check_if_position_opened(currency_pair, magicnumber):
            if trend.iMA(currency_pair,
                         time_frame,
                         ma_period,
                         ma_mode,
                         ma_applied_price,
                         0) > ask_price:
                ordersettings.OrderSend(currency_pair, order_type_buy, lotsize, "ask", 0, False,
                                        stoploss, False, takeprofit, ordercomment, magicnumber)
                # print(f"Buying {currency_pair} at {trend.MT5functions.get_order_open_price()}... price is in the Moving Average buy setup")
            if trend.iMA(currency_pair,
                         time_frame,
                         ma_period,
                         ma_mode,
                         ma_applied_price,
                         0) < bid_price:
                ordersettings.OrderSend(currency_pair, order_type_sell, lotsize, "bid", 0, False,
                                        stoploss, False, takeprofit, ordercomment, magicnumber)

    def DailyRange(self):
        # this will set a buy limit at session high
        # and a sell limt  at session low~
        daily_low = trend.iLow(
            currency_pair, trend.MT5functions.timeframe(1440), 0)
        daily_high = trend.iHigh(
            currency_pair, trend.MT5functions.timeframe(1440), 0)
        if not trend.MT5functions.check_if_order_opened(currency_pair, magicnumber1):
            ordersettings.OrderSend(currency_pair, order_type_buy_limit, lotsize, daily_low, 0, False,
                                    stoploss, False, takeprofit, ordercomment, magicnumber1)
            ordersettings.OrderSend(currency_pair, order_type_sell_limit, lotsize, daily_high, 0, False,
                                    stoploss, False, takeprofit, ordercomment, magicnumber1)


# run trade

# declare trade config class as an~ object
trade = Trade()


def allow_trades():
    if trend.MT5functions.allow_time(use_time, start_time, stop_time):
        if use_daily_range:
            trade.DailyRange()
        if use_moving_average:
            trade.MovingAverage()
        if use_doji:
            trade.Doji()
        if use_double_flat:
            trade.DoubleFlat()
        if use_fair_value_gap:
            trade.FairValueGap()

def allow_martingale():
    if use_martingale:
        order_stop_loss = MT5functions.order_info(currency_pair,"stop loss")
        MT5functions.use_martingale(currency_pair,magicnumber,order_stop_loss,martinMULTI,martinactivate,marrtinTP,maxtrades,ordercomment)
        MT5functions.use_martingale(currency_pair,magicnumber1,order_stop_loss,martinMULTI,martinactivate,marrtinTP,maxtrades,ordercomment)
        MT5functions.use_martingale(currency_pair,magicnumber2,order_stop_loss,martinMULTI,martinactivate,marrtinTP,maxtrades,ordercomment)
        MT5functions.use_martingale(currency_pair,magicnumber3,order_stop_loss,martinMULTI,martinactivate,marrtinTP,maxtrades,ordercomment)
        MT5functions.use_martingale(currency_pair,magicnumber4,order_stop_loss,martinMULTI,martinactivate,marrtinTP,maxtrades,ordercomment)
        MT5functions.use_martingale(currency_pair,magicnumber5,order_stop_loss,martinMULTI,martinactivate,marrtinTP,maxtrades,ordercomment)

while True:
    allow_trades()
    allow_martingale()
    