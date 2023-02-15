import MetaTrader5
import MT5functions
import re
import sys


def OrderSend(symbol, ordertype, lot, orderprice, slipppage, use_custom_stoploss, stoplosss, use_custom_takeprofit, takeeprofitt, orderrcomment, maggicnumberr):

    new_order_type = ordertype.lower()
    pip_value = MT5functions.Get_Pip_Value(symbol)

    def entry_price():  # defining the entry price
        if orderprice == "ask":
            return MetaTrader5.symbol_info_tick(
                symbol).ask  # getting the ask price
        if orderprice == "bid":
            return MetaTrader5.symbol_info_tick(
                symbol).bid  # getting the bid price
        return orderprice

    def stop_loss():  # defining the stop loss
        if use_custom_stoploss:
            return stoplosss
        if not use_custom_stoploss and new_order_type in ["buy", "buy limit", "buy stop"]:
            return entry_price() - stoplosss * pip_value
        if not use_custom_stoploss and new_order_type in ["sell", "sell limit", "sell stop"]:
            return entry_price() + stoplosss * pip_value
        return stoplosss

    def take_profit():  # defining the take profit
        if use_custom_takeprofit:
            return takeeprofitt
        if not use_custom_takeprofit and new_order_type in ["buy", "buy limit", "buy stop"]:
            return entry_price() + takeeprofitt * pip_value
        if not use_custom_takeprofit and new_order_type in ["sell", "sell limit", "sell stop"]:
            return entry_price() - takeeprofitt * pip_value
        return takeeprofitt

    market_execution = MetaTrader5.TRADE_ACTION_DEAL  # market order
    market_limit_order = MetaTrader5.TRADE_ACTION_PENDING  # limit order

    if new_order_type == "buy":
        typee = MetaTrader5.ORDER_TYPE_BUY  # buy market execution order
        order_type = market_execution

    if new_order_type == "buy limit":
        typee = MetaTrader5.ORDER_TYPE_BUY_LIMIT  # buy limit order
        order_type = market_limit_order

    if new_order_type == "buy stop":
        typee = MetaTrader5.ORDER_TYPE_BUY_STOP  # buy stop order
        order_type = market_limit_order

    if new_order_type == "sell":
        typee = MetaTrader5.ORDER_TYPE_SELL  # sell market execution order
        order_type = market_execution

    if new_order_type == "sell limit":
        typee = MetaTrader5.ORDER_TYPE_SELL_LIMIT  # sell limit order
        order_type = market_limit_order

    if new_order_type == "sell stop":
        typee = MetaTrader5.ORDER_TYPE_SELL_STOP  # sell stop order
        order_type = market_limit_order

    if re.search(r"limit|stop", new_order_type):
        request = {
            "action": order_type,  # what type of order
            "symbol": symbol,  # symbol
            "type": typee,  # order type
            "volume": lot,  # lot size
            "price": entry_price(),
            "deviation": slipppage,
            "sl": stop_loss(),
            "tp": take_profit(),
            "comment": orderrcomment,  # order comment
            "magic": maggicnumberr,  # magic number
            # stays active until it is manually closed
            "type_time": MetaTrader5.ORDER_TIME_GTC,
            "type_filling": MetaTrader5.ORDER_FILLING_RETURN
        }
    if re.search(r"buy|sell", new_order_type) and not re.search(r"limit|stop", new_order_type):
        request = {
            "action": order_type,  # what type of order
            "symbol": symbol,  # symbol
            "type": typee,  # order type
            "volume": lot,  # lot size
            "price": entry_price(),
            "deviation": slipppage,
            "sl": stop_loss(),
            "tp": take_profit(),
            "comment": orderrcomment,  # order comment
            "magic": maggicnumberr,  # magic number
            # stays active until it is manually closed
            "type_time": MetaTrader5.ORDER_TIME_GTC,
            "type_filling": MetaTrader5.ORDER_FILLING_IOC
        }
    if not MetaTrader5.order_send(request):  # if it doesnt send an order
        errorrr = str(MetaTrader5.last_error())
        sys.exit(f"Order send failed \n"
            f"Stop loss = {stop_loss()} \n" 
            f"Take profit = {take_profit()} \n" 
            f"Entry price = {entry_price()} \n" 
            f"Lot size = {lot} \n" 
            f"Error code = {errorrr}")  # send error and exit

def OrderModify(pair, ticket, price, stop_loss, take_profit):

    #symboll = MetaTrader5.orders_get(ticket).symbol
    #magicc = MetaTrader5.orders_get(ticket).magic
    #lott = MetaTrader5.orders_get(ticket).volume

    symboll = MT5functions.order_info(pair,"symbol")
    magicc = MT5functions.order_info(pair,"magic number")
    lott = MT5functions.order_info(pair,"lot size")

    # create a TradeRequest object to modify the order
    request = {
        'action' : MetaTrader5.TRADE_ACTION_SLTP, # specify that this is a stop loss/take profit modification
        'type_filling' : MetaTrader5.ORDER_FILLING_RETURN, # replace with the desired order filling type
        'type_time' : MetaTrader5.ORDER_TIME_GTC, # replace with the desired order expiration type
        'magic' : magicc, # replace with the desired order magic number
        'symbol' : symboll, # get the symbol of the order to modify
        'volume' : lott, # get the volume of the order to modify
        'price' : price, # set the new price to modify the order
        'sl' : stop_loss, # set the new stop loss value
        'tp' : take_profit, # set the new take profit value
        'position' : ticket # specify the ticket number of the order to modify
    }

    if not MetaTrader5.order_send(request):  
        errorrr = str(MetaTrader5.last_error())
        sys.exit("Order modify failed, error code = " +
                 errorrr)  # send error and exit
