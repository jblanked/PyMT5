from datetime import datetime
import MetaTrader5
import re
import pytz  # working with timezones


# timeframes
def timeframe(minutes):
    if minutes == 1:
        return MetaTrader5.TIMEFRAME_M1
    if minutes == 5:
        return MetaTrader5.TIMEFRAME_M5
    if minutes == 15:
        return MetaTrader5.TIMEFRAME_M15
    if minutes == 30:
        return MetaTrader5.TIMEFRAME_M30
    if minutes == 60:
        return MetaTrader5.TIMEFRAME_H1
    if minutes == 240:
        return MetaTrader5.TIMEFRAME_H4
    if minutes == 1440:
        return MetaTrader5.TIMEFRAME_D1
    if minutes == 10080:
        return MetaTrader5.TIMEFRAME_W1
    return MetaTrader5.TIMEFRAME_MN1


def get_account_info(option):
    account_data = MetaTrader5.account_info()

    if account_data is not None:
        new_type = option.lower()

        if new_type == "number":
            return account_data.login

        if new_type == "equity":
            return account_data.equity

        if new_type == "currency":
            return account_data.currency

        if new_type == "company":
            return account_data.company

        if new_type == "balance":
            return account_data.balance

        if new_type == "name":
            return account_data.name

        if new_type == "profit":
            return account_data.profit
        return account_data


def order_info(currency_pairr, option):
    if MetaTrader5.positions_total() or MetaTrader5.orders_total() > 0:

        position_data = MetaTrader5.positions_get(symbol=currency_pairr)
        order_data = MetaTrader5.orders_get(symbol=currency_pairr)

        new_type = option.lower()

        if position_data is None:
            data = order_data

        if order_data is None:
            data = position_data

        else:
            data = position_data + order_data

        if new_type == "magic number":
            for items in data:
                return items.magic

        if new_type == "stop loss":
            for items in data:
                return items.sl

        if new_type == "take profit":
            for items in data:
                return items.tp

        if new_type == "comment":
            for items in data:
                return items.comment

        if new_type == "lot size":
            for items in data:
                return items.volume

        if new_type == "type":
            for items in data:
                return items.type

        if new_type == "symbol":
            for items in data:
                return items.symbol

        if new_type == "swap":
            for items in data:
                return items.swap

        if new_type == "commission":
            for items in data:
                return items.commission

        if new_type == "ticket":
            for items in data:
                return position_data[0].ticket

        if new_type == "open price":
            for items in data:
                return items.price_open

        if new_type == "current price":
            for items in data:
                return items.price_current

        if new_type == "profit":
            for items in data:
                return position_data[0].profit

        if new_type == "status":
            for items in data:
                if items.price_open <= 0:
                    return False
                return True


def symbol_info(currency_pairr, option):
    new_type = option.lower()
    data = MetaTrader5.symbol_info(currency_pairr)

    if new_type == "tick value":
        return data.trade_tick_value

    if new_type == "spread":
        return data.spread

    if new_type == "bid":
        return data.bid

    if new_type == "ask":
        return data.ask

    if new_type == "point":
        return data.point

    if new_type == "front":
        return data.currency_base

    if new_type == "end":
        return data.currency_profit

    if new_type == "digits":
        return data.digits

    if new_type == "max lot size":
        return 100  # on most broker this is 100, will test this


def check_if_order_opened(symbol, magicnumberr):
    total_limit_orders = MetaTrader5.orders_total()
    total_list = [total_limit_orders]

    magic = order_info(symbol, "magic number")
    order_symbol = order_info(symbol, "symbol")

    for open_orders in total_list:
        if total_limit_orders == 0:
            return False

        if total_limit_orders != 0 and int(magic) == magicnumberr and symbol == str(order_symbol):
            return True
    return True


def check_if_position_opened(symbol, magicnumberr):
    total_market_orders = MetaTrader5.positions_total()

    i = 0

    while i < total_market_orders:

        magic = order_info(symbol, "magic number")
        order_symbol = order_info(symbol, "symbol")

        if total_market_orders != 0 and int(magic) == magicnumberr and symbol == str(order_symbol):
            return True
    return False


def allow_time(useTimer, start_time, stop_time):
    current_time = datetime.now(pytz.utc).time()
    start_time = datetime.strptime(
        start_time, "%H:%M").time().replace(tzinfo=pytz.utc)
    stop_time = datetime.strptime(
        stop_time, "%H:%M").time().replace(tzinfo=pytz.utc)
    if not useTimer:
        return True
    if useTimer and stop_time >= current_time >= start_time:
        return True
    return False


def Get_Pip_Value(symbol):
    digits = symbol_info(symbol, 'digits')

    lowercase_symbol = symbol.lower()

    if digits >= 4:
        return 0.0001

    if re.search(r"us30|nas100|spx500|jpn225|uk100|fra40|esp35|us30.mini|nas100.mini|btcusd|ethusd|ltcusd|bnbusd|u30usd.hkt|nasusd.hkt|spxusd.hkt|225jpy.hkt|100gbp.hkt|f40eur.hkt|e35eur.hkt|us100.cash|us30.cash|us30.e8|us100.e8|us500.e8|ger40.e8|eu50.e8", lowercase_symbol):
        return 1
    if lowercase_symbol in ("xauusd", "xauusd.hkt"):
        return 0.10
    return 0.01


def Get_Risk(useRisk, useLotSize, percentRisk, stopLosss, lotsizeee, symbol):
    accEquity = get_account_info("equity")
    decimalRisk = percentRisk / 100
    accountRisk = accEquity * decimalRisk
    lotSizes = symbol_info(symbol, "max lot size")
    tickValue = symbol_info(symbol, "tick value")
    account_company = get_account_info("company")
    pip_value = Get_Pip_Value(symbol)

    if account_company == "Hankotrade LLC" and pip_value == 1:
        tickValue *= 100

    if symbol == "US30.mini":
        tickValue *= 100

    if symbol == "NAS100.mini":
        tickValue *= 100

    if account_company == "FTMO S.R.O." and pip_value == 1:
        tickValue *= 100

    if account_company == "Traders Global Group Incorporated" and pip_value == 1:
        tickValue *= 10

    maxLossInQuoteCurr = accountRisk / tickValue
    quoteDivision = maxLossInQuoteCurr / (stopLosss * pip_value)
    getRisk = round((quoteDivision / lotSizes), 2)

    if useRisk and not useLotSize:
        return getRisk
    if useLotSize and not useRisk:
        return round(lotsizeee, 2)
    return lotsizeee


def division(numerator, denominator):
    if denominator == 0:
        return 0
    return numerator/denominator


def Get_US30(symbol):
    current_symbol_string = str(symbol_info(symbol, "symbol"))
    if get_account_info("company") == "FTMO S.R.O.":
        return "US30.cash"

    if get_account_info("company") == "Hankotrade LLC":
        return "U30USD.HKT"

    if get_account_info("company") == "E8 Funding Ltd":
        return "US30.e8"

    if current_symbol_string == "US30.mini":
        return "US30.mini"

    else:
        return "US30"


def Get_NAS100(symbol):
    current_symbol_string = str(symbol_info(symbol, "symbol"))
    if get_account_info("company") == "FTMO S.R.O.":
        return "US100.cash"

    if get_account_info("company") == "Hankotrade LLC":
        return "NASUSD.HKT"

    if get_account_info("company") == "E8 Funding Ltd":
        return "US100.e8"

    if current_symbol_string == "NAS100.mini":
        return "NAS100.mini"

    else:
        return "NAS100"


def Get_SPX500():
    if get_account_info("company") == "FTMO S.R.O.":
        return "US500.cash"

    if get_account_info("company") == "Hankotrade LLC":
        return "SPXUSD.HKT"

    if get_account_info("company") == "E8 Funding Ltd":
        return "US500.e8"

    else:
        return "SPX500"


def Get_Pair_Extension():

    if get_account_info("company") == "Hankotrade LLC":

        return ".HKT"

    if get_account_info("company") == "E8 Funding Ltd":

        return ".e8"

    if get_account_info("company") == "FTMO S.R.O.":

        return ".cash"

    else:

        return ""


def Expiry_name():
    account_name_1 = ""
    account_name_2 = ""
    account_name_3 = ""
    account_name_4 = ""
    account_name_5 = ""
    account_name_6 = ""
    account_name_7 = ""
    account_name_8 = ""
    account_name_9 = ""
    account_name_10 = ""
    account_name_11 = ""
    account_name_12 = ""
    account_name_13 = ""
    account_name_14 = ""
    account_name_15 = ""
    account_name_16 = ""
    account_name_17 = ""
    account_name_18 = ""
    account_name_19 = ""
    account_name_20 = ""

    account = get_account_info("name")

    if account not in [account_name_1,
                       account_name_2, account_name_3,
                       account_name_4, account_name_5,
                       account_name_6, account_name_7,
                       account_name_8, account_name_9,
                       account_name_10, account_name_11,
                       account_name_12, account_name_13,
                       account_name_14, account_name_15,
                       account_name_16, account_name_17,
                       account_name_18, account_name_19,
                       account_name_20
                       ]:
        return False
    return True


def profit_in_dollars(symbol, lotsize):


    base = symbol_info(symbol,"base")
    
    if get_account_info("company") == "Osprey Ltd":

        commission = lotsize * 100 * 0.07

        if get_account_info("currency") == 'USD':

            if symbol in ['US30', "NAS100"]:
                return 100 * lotsize - commission # this is $1 per pip on smallest lot

            if base == "USD":
                return 1000 * lotsize - commission # this is $1 per 10 pips on smallest lot

            if base == "CAD":
                return 1347.45 * lotsize - commission # this is $1 per 10 pips on smallest lot

            if base == "JPY":
                return 1341.05 * lotsize - commission # this is $1 per 10 pips on smallest lot

            if base == "AUD":
                return 1453.7 * lotsize - commission # this is $1 per 10 pips on smallest lot

            if base == "CHF":
                return 924.94 * lotsize - commission # this is $1 per 10 pips on smallest lot

            if base == "NZD":
                return 1601.28 * lotsize - commission # this is $1 per 10 pips on smallest lot
            

    