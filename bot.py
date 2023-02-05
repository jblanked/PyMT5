import trend
import ordersettings
import login
import password as p




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



currency_pair = "ETHUSD"  # currency pair to trade

# timeframe
# changed one_minute to your time frame
time_frame = trend.MT5functions.one_minute 

order_type_buy = "buy"  # buy market execution order
order_type_sell = "sell"  # sell market execution order
order_type_buy_limit = "buy limit"  # buy limit order
order_type_sell_limit = "sell limit"  # sell lmit order

price = "ask"  # entry price if buying via market execution
price2 = "bid"  # entry price if selling via market execution

use_risk = True  # use percent risk?
risk = 1.0  # risk percent
use_lot_size = False  # use lot size?
lotsizes = 0.05  # lot size~
stoploss = 50  # stop loss
takeprofit = 400  # take profit



use_time = False  # use trading hours?
start_time = "08:00"  # start time (server time)
stop_time = "16:49"  # stop time (server time)

ordercomment = "Python Test"  # order comment
magicnumber = 899811  # magic number




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

# declared the FVG class as a vairable
fair_value_gap_object = trend.FairValueGap()

# fair value gap bullish entry
FVG_bullish_entry = fair_value_gap_object.Bullish_entry(
    symbol=currency_pair,
    timeframe=trend.MT5functions.one_minute,
    middle_body_percent=middlebodypercent,
    first_body_percent=firstbodypercent,
    third_body_percent=thirdbodypercent)

# fair value gap bearish entry
FVG_bearish_entry = fair_value_gap_object.Bearish_entry(
    symbol=currency_pair,
    timeframe=trend.MT5functions.one_minute,
    middle_body_percent=middlebodypercent,
    first_body_percent=firstbodypercent,
    third_body_percent=thirdbodypercent)

# fair value gap bullish SL
FVG_bullish_SL = fair_value_gap_object.Bullish_SL(
    symbol=currency_pair,
    timeframe=trend.MT5functions.one_minute,
    middle_body_percent=middlebodypercent,
    first_body_percent=firstbodypercent,
    third_body_percent=thirdbodypercent)

# fair value gap bearish SL
FVG_bearish_SL = fair_value_gap_object.Bearish_SL(
    symbol=currency_pair,
    timeframe=trend.MT5functions.one_minute,
    middle_body_percent=middlebodypercent,
    first_body_percent=firstbodypercent,
    third_body_percent=thirdbodypercent)

# fair value gap bullish TP
FVG_bullish_TP = fair_value_gap_object.Bullish_TP(
    symbol=currency_pair,
    timeframe=trend.MT5functions.one_minute,
    middle_body_percent=middlebodypercent,
    first_body_percent=firstbodypercent,
    third_body_percent=thirdbodypercent)

# fair value gap bearish TP
FVG_bearish_TP = fair_value_gap_object.Bearish_TP(
    symbol=currency_pair,
    timeframe=trend.MT5functions.one_minute,
    middle_body_percent=middlebodypercent,
    first_body_percent=firstbodypercent,
    third_body_percent=thirdbodypercent)







# doji settings
doji_body_pips = 1.0  # Body lengnth <= X pips
doji_wick_pips = 1.0  # Difference of both wick lengths <= X pips
doji_wickk_length = 1.0  # Both Wick length's >= X pips

doji_object = trend.Doji()  # declared the Doji class as a variable

# doji bullish entry
doji_bullish_entry = doji_object.Bullish_entry(
    currency_pair,
    trend.MT5functions.one_minute,
    doji_body_pips,
    doji_wick_pips,
    doji_wickk_length)

# doji bearish entry
doji_bearish_entry = doji_object.Bearish_entry(
    currency_pair,
    trend.MT5functions.one_minute,
    doji_body_pips,
    doji_wick_pips,
    doji_wickk_length)

# doji bullish SL
doji_bullish_SL = doji_object.Bullish_SL(
    currency_pair,
    trend.MT5functions.one_minute,
    doji_body_pips,
    doji_wick_pips,
    doji_wickk_length)

# doji bearish SL
doji_bearish_SL = doji_object.Bearish_SL(
    currency_pair,
    trend.MT5functions.one_minute,
    doji_body_pips,
    doji_wick_pips,
    doji_wickk_length)


# double flat settings
pip_cushion = 1.0  # pip cushion (double flat within pip range)
double_flat_wick_length = 2.0  # wick length <= X

# declared the Doubleflat class as a variable
double_flat_object = trend.DoubleFlat()

# double flat bullish entry
double_flat_bullish_entry = double_flat_object.Bullish_entry(
    currency_pair,
    trend.MT5functions.one_minute,
    pip_cushion,
    double_flat_wick_length)

# double flat bearish entry
double_flat_bearish_entry = double_flat_object.Bearish_entry(
    currency_pair,
    trend.MT5functions.one_minute,
    pip_cushion,
    double_flat_wick_length)

# double flat bullish SL
double_flat_bullish_SL = double_flat_object.Bullish_SL(
    currency_pair,
    trend.MT5functions.one_minute,
    pip_cushion,
    double_flat_wick_length)

# double flat bearish SL
double_flat_bearish_SL = double_flat_object.Bearish_SL(
    currency_pair,
    trend.MT5functions.one_minute,
    pip_cushion,
    double_flat_wick_length)




# lot size with stop loss in pips
lotsize = trend.MT5functions.Get_Risk(use_risk,use_lot_size,risk,stoploss,lotsizes,currency_pair)



# trading configurations
class Trade:

    def __init__(self) -> None:
        pass

    def FairValueGap(self):
        # this one will buy if there's a bullish fair value gap
        # and sell if there's a bearish fair value gap
        if fair_value_gap_object.trend(currency_pair,
                                       time_frame,
                                       middlebodypercent,
                                       firstbodypercent,~
                                       thirdbodypercent) == "Buy":

            ordersettings.SendCustomOrder(currency_pair, order_type_buy_limit, lotsize, FVG_bullish_entry, 0,
                                          FVG_bullish_SL, FVG_bullish_TP, ordercomment, magicnumber)

        if fair_value_gap_object.trend(currency_pair,
                                       time_frame,
                                       middlebodypercent,
                                       firstbodypercent,
                                       thirdbodypercent) == "Sell":

            ordersettings.SendCustomOrder(currency_pair, order_type_sell_limit, lotsize, FVG_bearish_entry,
                                          0, FVG_bearish_SL, FVG_bearish_TP, ordercomment, magicnumber)

    def DoubleFlat(self):
        # this one will buy if there's a bullish Double flat bottom
        # and sell if theres a bearish double flat top
        if double_flat_object.trend(currency_pair,
                                    time_frame,
                                    pip_cushion,
                                    double_flat_wick_length) == "Buy":

            ordersettings.SendCustomOrderSL(currency_pair, order_type_buy_limit, lotsize, double_flat_bullish_entry, 0,
                                            double_flat_bullish_SL, takeprofit, ordercomment, magicnumber)
        if double_flat_object.trend(currency_pair,
                                    time_frame,
                                    pip_cushion,
                                    double_flat_wick_length) == "Sell":

            ordersettings.SendCustomOrderSL(currency_pair, order_type_buy_limit, lotsize, double_flat_bearish_entry, 0,
                                            double_flat_bearish_SL, takeprofit, ordercomment, magicnumber)

    def Doji(self):
        # this one will buy if there's a bullish Doji candle
        # and sell if there's a bearish doji candle
        if doji_object.trend(currency_pair,
                             time_frame,
                             doji_body_pips,
                             doji_wick_pips,
                             doji_wickk_length) == "Buy":
            ordersettings.SendCustomOrderSL(currency_pair, order_type_buy_limit, lotsize, doji_bullish_entry, 0,
                                            doji_bullish_SL, takeprofit, ordercomment, magicnumber)
        if doji_object.trend(currency_pair,
                             time_frame,
                             doji_body_pips,
                             doji_wick_pips,
                             doji_wickk_length) == "Sell":
            ordersettings.SendCustomOrderSL(currency_pair, order_type_buy_limit, lotsize, doji_bearish_entry, 0,
                                            doji_bearish_SL, takeprofit, ordercomment, magicnumber)

    def MovingAverage(self):
        # this will buy if price is above the moving average
        # and sell if price is below the moving average
        ask_price = trend.MetaTrader5.symbol_info_tick(
            currency_pair).ask  # getting the ask price
        bid_price = trend.MetaTrader5.symbol_info_tick(
            currency_pair).bid  # getting the bid price
        if trend.iMA(currency_pair,
                     time_frame,
                     ma_period,
                     ma_mode,
                     ma_applied_price,
                     0) > ask_price:
            ordersettings.SendOrder(currency_pair, order_type_buy, lotsize, "ask", 0,
                                    stoploss, takeprofit, ordercomment, magicnumber)
        if trend.iMA(currency_pair,
                     time_frame,
                     ma_period,
                     ma_mode,
                     ma_applied_price,
                     0) < bid_price:
            ordersettings.SendOrder(currency_pair, order_type_sell, lotsize, "bid", 0,
                                    stoploss, takeprofit, ordercomment, magicnumber)

    def DailyRange(self):
        # this will set a buy limit at session high
        # and a sell limt  at session low
        daily_low = trend.daily_loww(currency_pair)
        daily_high = trend.daily_highh(currency_pair)
        ordersettings.SendOrder(currency_pair, order_type_buy_limit, lotsize, daily_low, 0,
                                stoploss, takeprofit, ordercomment, magicnumber)
        ordersettings.SendOrder(currency_pair, order_type_sell_limit, lotsize, daily_high, 0,
                                stoploss, takeprofit, ordercomment, magicnumber)


# run trade

# declare trade config class as an object
trade = Trade()

# this will trade if no orders are opened 
def trade_now():
    if trend.MT5functions.allow_time(use_time, start_time, stop_time):
        if not trend.MT5functions.check_if_order_opened(currency_pair,magicnumber):
            trade.MovingAverage()
            return True

# this will make it take a trade again if order is closed
while True:
    trade_now()
