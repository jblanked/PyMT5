from datetime import datetime, time
import MetaTrader5
import re




# timeframes
# you can even do times in between each, like 2 hour, 3 hour, 2 minute, etc
one_minute = MetaTrader5.TIMEFRAME_M1
five_minute = MetaTrader5.TIMEFRAME_M5
fifthteen_minute = MetaTrader5.TIMEFRAME_M15
thirty_minute = MetaTrader5.TIMEFRAME_M30
one_hour = MetaTrader5.TIMEFRAME_H1
four_hour = MetaTrader5.TIMEFRAME_H4
daily = MetaTrader5.TIMEFRAME_D1
weekly = MetaTrader5.TIMEFRAME_W1
monthly = MetaTrader5.TIMEFRAME_MN1



def get_account_info():
    total_info = MetaTrader5.account_info()
    return total_info

def get_account_number():
    account_number = get_account_info().login
    return account_number

def get_account_equity():
    account_equity = get_account_info().equity
    return account_equity

def get_tick_value(symbol):
    tick = MetaTrader5.symbol_info_tick(symbol)
    ask_price = tick.ask
    ask_price_str = str(ask_price)
    decimal_places = len(ask_price_str.split(".")[1])
    tick_value = round(ask_price * 10**(-1 * decimal_places), 2)
    return tick_value






def get_account_company():
    account_company = get_account_info().company
    return account_company

def get_account_balance():
    account_balance = get_account_info().balance
    return account_balance

def get_account_name():
    account_name = get_account_info().name
    return account_name

def get_account_profit():
    account_profit = get_account_info().profit
    return account_profit

def get_order_magic_number():
    magicnumber = MetaTrader5.positions_get(symbol = "ETHUSD")
    for items in magicnumber:
        return items.magic

def get_order_stop_loss():
    magicnumber = MetaTrader5.positions_get(symbol = "ETHUSD")
    for items in magicnumber:
        return items.sl

def get_order_take_profit():
    magicnumber = MetaTrader5.positions_get(symbol = "ETHUSD")
    for items in magicnumber:
        return items.tp

def get_order_comment():
    magicnumber = MetaTrader5.positions_get(symbol = "ETHUSD")
    for items in magicnumber:
        return items.comment

def get_order_lot_size():
    magicnumber = MetaTrader5.positions_get(symbol = "ETHUSD")
    for items in magicnumber:
        return items.volume

def get_order_type():
    magicnumber = MetaTrader5.positions_get(symbol = "ETHUSD")
    for items in magicnumber:
        return items.type

def get_order_symbol():
    magicnumber = MetaTrader5.positions_get(symbol = "ETHUSD")
    for items in magicnumber:
        return items.symbol

def get_order_open_price():
    magicnumber = MetaTrader5.positions_get(symbol = "ETHUSD")
    for items in magicnumber:
        return items.price_open

def get_order_current_price():
    magicnumber = MetaTrader5.positions_get(symbol = "ETHUSD")
    for items in magicnumber:
        return items.price_current


def check_if_order_opened(symbol, magicnumberr):
    magic = get_order_magic_number()
    order_symbol = get_order_symbol()
    total_orders = MetaTrader5.positions_total()
    if total_orders > 0 and order_symbol == symbol and magic == magicnumberr:
        return True
    return False

def get_order_status():
    if get_order_open_price() <= 0:
        return True
    return False

        



current_time = datetime.now().time()

def allow_time(useTimer, start_time, stop_time):
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

    if re.search(r"US30|NAS100|SPX500|JPN225|UK100|FRA40|ESP35|US30.mini|NAS100.mini|BTCUSD|ETHUSD|LTCUSD|BNBUSD|U30USD.HKT|NASUSD.HKT|SPXUSD.HKT|225JPY.HKT|100GBP.HKT|F40EUR.HKT|E35EUR.HKT|US100.cash|US30.cash|US30.e8|US100.e8|US500.e8|GER40.e8|EU50.e8",current_symbol_string):
        return 1
    if current_symbol_string in ("XAUUSD" , "XAUUSD.HKT"):
        return 0.10
    return 0.01


def Get_Risk(useRisk, useLotSize, percentrisk, stoplosss, lotsizee, symbol):
    current_symbol_string = str(MetaTrader5.symbol_info(symbol))
    tickk_valuee = get_tick_value(symbol)
    if useRisk and not useLotSize:
        equity = get_account_equity()
        decimal_risk = percentrisk / 100
        account_risk = equity * decimal_risk
       
        if get_account_company() == "Hankotrade LLC" and Get_Pip_Value(symbol) == 1:
            tickk_valuee = tickk_valuee * 100
        if get_account_company() == "FTMO S.R.O." and Get_Pip_Value(symbol) == 1:
            tickk_valuee = tickk_valuee * 100
        if get_account_company() == "Traders Global Group Incorporated" and Get_Pip_Value(symbol) == 1:
            tickk_valuee = tickk_valuee * 10

        if current_symbol_string == "US30.mini":
            tickk_valuee = tickk_valuee * 100
        if current_symbol_string == "NAS100.mini":
            tickk_valuee = tickk_valuee * 100

        max_loss_in_quote_currency =  division(account_risk,tickk_valuee)
        get_risk = max_loss_in_quote_currency / (stoplosss * Get_Pip_Value(symbol)) / lotsizee
        return round(get_risk,2)

    if useLotSize and not useRisk:
        gett_riskk = lotsizee
        return gett_riskk

    return lotsizee



def division(numerator, denominator):
    if denominator == 0:
        return 0
    else:
        return numerator/denominator





def Get_US30(symbol):
    current_symbol_string = str(MetaTrader5.symbol_info(symbol))
    if get_account_company() == "FTMO S.R.O.":
        return "US30.cash"

    if get_account_company() == "Hankotrade LLC":
        return "U30USD.HKT"

    if get_account_company() == "E8 Funding Ltd":
        return "US30.e8"

    if current_symbol_string == "US30.mini":
        return "US30.mini"

    else:
        return "US30"

def Get_NAS100(symbol):
    current_symbol_string = str(MetaTrader5.symbol_info(symbol))
    if get_account_company() == "FTMO S.R.O.":
        return "US100.cash"

    if get_account_company() == "Hankotrade LLC":
        return "NASUSD.HKT"

    if get_account_company() == "E8 Funding Ltd":
        return "US100.e8"

    if current_symbol_string == "NAS100.mini":
        return "NAS100.mini"

    else:
        return "NAS100"




def Get_SPX500 ():
    if get_account_company() == "FTMO S.R.O.":
        return "US500.cash"

    if get_account_company() == "Hankotrade LLC":
        return "SPXUSD.HKT"

    if get_account_company() == "E8 Funding Ltd":
        return "US500.e8"

    else:
        return "SPX500"




def Get_Pair_Extension():

    if get_account_company() == "Hankotrade LLC":

        return ".HKT"

    if get_account_company() == "E8 Funding Ltd":

        return ".e8"

    if get_account_company() == "FTMO S.R.O.":

        return ".cash"

    else:

        return ""
