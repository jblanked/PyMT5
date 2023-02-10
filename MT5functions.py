from datetime import datetime, time
import MetaTrader5
import re


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
    new_type = option.lower()

    if new_type == "number":
        return account_data.login

    if new_type == "equity":
        return account_data.equity

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

    if new_type == "open price":
        for items in data:
            return items.price_open

    if new_type == "current price":
        for items in data:
            return items.price_current

    if new_type == "status":
        for items in data:
            if items.price_open <= 0:
                return False
            return True


def get_tick_value(symbol):
    tick_value = MetaTrader5.symbol_info(symbol).trade_tick_value
    return tick_value


def get_max_lotsize(symbol):
    lots = MetaTrader5.symbol_info(symbol).volume_max
    return lots/10


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
    total_list = [total_market_orders]

    magic = order_info(symbol, "magic number")
    order_symbol = order_info(symbol, "symbol")

    for open_orders in total_list:
        if total_market_orders == 0:
            return False

        if total_market_orders != 0 and int(magic) == magicnumberr and symbol == str(order_symbol):
            return True
    return False


def allow_time(useTimer, start_time, stop_time):
    current_time = datetime.now().time()
    start_time = datetime.strptime(start_time, "%H:%M").time()
    stop_time = datetime.strptime(stop_time, "%H:%M").time()
    if not useTimer:
        return True
    if useTimer and stop_time >= current_time >= start_time:
        return True
    return False


def Get_Pip_Value(symbol):
    current_symbol = MetaTrader5.symbol_info(symbol)
    current_symbol_string = str(MetaTrader5.symbol_info(symbol))

    digits = current_symbol.digits

    if digits >= 4:
        return 0.0001

    if re.search(r"US30|NAS100|SPX500|JPN225|UK100|FRA40|ESP35|US30.mini|NAS100.mini|BTCUSD|ETHUSD|LTCUSD|BNBUSD|U30USD.HKT|NASUSD.HKT|SPXUSD.HKT|225JPY.HKT|100GBP.HKT|F40EUR.HKT|E35EUR.HKT|US100.cash|US30.cash|US30.e8|US100.e8|US500.e8|GER40.e8|EU50.e8", current_symbol_string):
        return 1
    if current_symbol_string in ("XAUUSD", "XAUUSD.HKT"):
        return 0.10
    return 0.01


def Get_Risk(useRisk, useLotSize, percentRisk, stopLosss, lotsizeee, symbol):
    accEquity = get_account_info("equity")
    decimalRisk = percentRisk / 100
    accountRisk = accEquity * decimalRisk
    lotSizes = get_max_lotsize(symbol)
    tickValue = get_tick_value(symbol)
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
    getRisk = quoteDivision / lotSizes

    if useRisk and not useLotSize:
        return round(getRisk, 2)
    if useLotSize and not useRisk:
        return round(lotsizeee, 2)
    return lotsizeee


def division(numerator, denominator):
    if denominator == 0:
        return 0
    else:
        return numerator/denominator


def Get_US30(symbol):
    current_symbol_string = str(MetaTrader5.symbol_info(symbol))
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
    current_symbol_string = str(MetaTrader5.symbol_info(symbol))
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
    account_name_1 = "Jacobie Barksdale"
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
