import MetaTrader5
import MT5functions
import re



def SendOrder(symbol,ordertype, lot, orderprice,slipppage, stoplosss,takeeprofitt,orderrcomment,maggicnumberr): 

    
    if orderprice == "ask":
        trade_price = MetaTrader5.symbol_info_tick(symbol).ask # getting the ask price
    if orderprice == "bid":
        trade_price = MetaTrader5.symbol_info_tick(symbol).bid # getting the bid price

    buy_market = MetaTrader5.ORDER_TYPE_BUY # buy market execution order
    buy_limit = MetaTrader5.ORDER_TYPE_BUY_LIMIT # buy limit order
    buy_stop = MetaTrader5.ORDER_TYPE_BUY_STOP # buy stop order

    sell_market = MetaTrader5.ORDER_TYPE_SELL # sell market execution order
    sell_limit = MetaTrader5.ORDER_TYPE_SELL_LIMIT # sell limit order
    sell_stop = MetaTrader5.ORDER_TYPE_SELL_STOP # sell stop order

    market_execution = MetaTrader5.TRADE_ACTION_DEAL # market order
    market_limit_order = MetaTrader5.TRADE_ACTION_PENDING# limit order

    stop_loss_price_sell = trade_price + stoplosss * MT5functions.Get_Pip_Value(symbol) # stop loss price for sells
    take_profit_price_sell = trade_price - takeeprofitt * MT5functions.Get_Pip_Value(symbol) # take profit price for sells

    stop_loss_price_buy = trade_price - stoplosss * MT5functions.Get_Pip_Value(symbol) # stop loss price for sells
    take_profit_price_buy = trade_price + takeeprofitt * MT5functions.Get_Pip_Value(symbol) # take profit price for sells

    new_order_type = ordertype.lower()
    if new_order_type == "buy":
        typee = buy_market
        order_type = market_execution
        sl = stop_loss_price_buy
        tp = take_profit_price_buy

    if new_order_type == "buy limit":
        typee = buy_limit
        order_type = market_limit_order
        sl = stop_loss_price_buy
        tp = take_profit_price_buy
    if new_order_type == "buy stop":
        typee = buy_stop
        order_type = market_limit_order
        sl = stop_loss_price_buy
        tp = take_profit_price_buy
    if new_order_type == "sell":
        typee = sell_market
        order_type = market_execution
        sl = stop_loss_price_sell
        tp = take_profit_price_sell
    if new_order_type == "sell limit":
        typee = sell_limit
        order_type = market_limit_order
        sl = stop_loss_price_sell
        tp = take_profit_price_sell
    if new_order_type == "sell stop":
        typee = sell_stop
        order_type = market_limit_order
        sl = stop_loss_price_sell
        tp = take_profit_price_sell


    if re.search(r"limit|stop",new_order_type):
        request = {
            "action": order_type, # what type of order
            "symbol": symbol, # symbol
            "type": typee, # order type
            "volume": lot, #lot size
            "price": trade_price,
            "deviation": slipppage,
            "sl": sl,
            "tp": tp,
            "comment": orderrcomment, # order comment
            "magic": maggicnumberr, # magic number
            "type_time": MetaTrader5.ORDER_TIME_GTC, # order stays active until it is manually closed
            "type_filling": MetaTrader5.ORDER_FILLING_RETURN, 
        }
    if re.search(r"buy|sell",new_order_type) and not re.search(r"limit|stop",new_order_type):
        request = {
            "action": order_type, # what type of order
            "symbol": symbol, # symbol
            "type": typee, # order type
            "volume": lot, #lot size
            "price": trade_price,
            "deviation": slipppage,
            "sl": sl,
            "tp": tp,
            "comment": orderrcomment, # order comment
            "magic": maggicnumberr, # magic number
            "type_time": MetaTrader5.ORDER_TIME_GTC, # order stays active until it is manually closed
            "type_filling": MetaTrader5.ORDER_FILLING_IOC
        }

    if not MetaTrader5.order_send(request): # if it doesnt send an order
        print("Order send failed, error code =",MetaTrader5.last_error()) # send error
        quit()


def SendCustomOrder(symbol,ordertype, lot, orderprice,slipppage, stoplosssprice,takeeprofittprice,orderrcomment,maggicnumberr): 

    
    if orderprice == "ask":
        trade_price = MetaTrader5.symbol_info_tick(symbol).ask # getting the ask price
    if orderprice == "bid":
        trade_price = MetaTrader5.symbol_info_tick(symbol).bid # getting the bid price

    buy_market = MetaTrader5.ORDER_TYPE_BUY # buy market execution order
    buy_limit = MetaTrader5.ORDER_TYPE_BUY_LIMIT # buy limit order
    buy_stop = MetaTrader5.ORDER_TYPE_BUY_STOP # buy stop order

    sell_market = MetaTrader5.ORDER_TYPE_SELL # sell market execution order
    sell_limit = MetaTrader5.ORDER_TYPE_SELL_LIMIT # sell limit order
    sell_stop = MetaTrader5.ORDER_TYPE_SELL_STOP # sell stop order

    market_execution = MetaTrader5.TRADE_ACTION_DEAL # market order
    market_limit_order = MetaTrader5.TRADE_ACTION_PENDING# limit order

    new_order_type = ordertype.lower()
    if new_order_type == "buy":
        typee = buy_market
        order_type = market_execution
        sl = stoplosssprice
        tp = takeeprofittprice

    if new_order_type == "buy limit":
        typee = buy_limit
        order_type = market_limit_order
        sl = stoplosssprice
        tp = takeeprofittprice
    if new_order_type == "buy stop":
        typee = buy_stop
        order_type = market_limit_order
        sl = stoplosssprice
        tp = takeeprofittprice
    if new_order_type == "sell":
        typee = sell_market
        order_type = market_execution
        sl = stoplosssprice
        tp = takeeprofittprice
    if new_order_type == "sell limit":
        typee = sell_limit
        order_type = market_limit_order
        sl = stoplosssprice
        tp = takeeprofittprice
    if new_order_type == "sell stop":
        typee = sell_stop
        order_type = market_limit_order
        sl = stoplosssprice
        tp = takeeprofittprice


    if re.search(r"limit|stop",new_order_type):
        request = {
            "action": order_type, # what type of order
            "symbol": symbol, # symbol
            "type": typee, # order type
            "volume": lot, #lot size
            "price": trade_price,
            "deviation": slipppage,
            "sl": sl,
            "tp": tp,
            "comment": orderrcomment, # order comment
            "magic": maggicnumberr, # magic number
            "type_time": MetaTrader5.ORDER_TIME_GTC, # order stays active until it is manually closed
            "type_filling": MetaTrader5.ORDER_FILLING_RETURN, 
        }
    if re.search(r"buy|sell",new_order_type) and not re.search(r"limit|stop",new_order_type):
        request = {
            "action": order_type, # what type of order
            "symbol": symbol, # symbol
            "type": typee, # order type
            "volume": lot, #lot size
            "price": trade_price,
            "deviation": slipppage,
            "sl": sl,
            "tp": tp,
            "comment": orderrcomment, # order comment
            "magic": maggicnumberr, # magic number
            "type_time": MetaTrader5.ORDER_TIME_GTC, # order stays active until it is manually closed
            "type_filling": MetaTrader5.ORDER_FILLING_IOC
        }

    if not MetaTrader5.order_send(request): # if it doesnt send an order
        print("Order send failed, error code =",MetaTrader5.last_error()) # send error
        quit()


def SendCustomOrderSL(symbol,ordertype, lot, orderprice,slipppage, stoplosssprice,takeeprofitt,orderrcomment,maggicnumberr): 

    
    if orderprice == "ask":
        trade_price = MetaTrader5.symbol_info_tick(symbol).ask # getting the ask price
    if orderprice == "bid":
        trade_price = MetaTrader5.symbol_info_tick(symbol).bid # getting the bid price

    buy_market = MetaTrader5.ORDER_TYPE_BUY # buy market execution order
    buy_limit = MetaTrader5.ORDER_TYPE_BUY_LIMIT # buy limit order
    buy_stop = MetaTrader5.ORDER_TYPE_BUY_STOP # buy stop order

    sell_market = MetaTrader5.ORDER_TYPE_SELL # sell market execution order
    sell_limit = MetaTrader5.ORDER_TYPE_SELL_LIMIT # sell limit order
    sell_stop = MetaTrader5.ORDER_TYPE_SELL_STOP # sell stop order

    market_execution = MetaTrader5.TRADE_ACTION_DEAL # market order
    market_limit_order = MetaTrader5.TRADE_ACTION_PENDING# limit order

    take_profit_price_sell = trade_price - takeeprofitt * MT5functions.Get_Pip_Value(symbol) # take profit price for sells

    take_profit_price_buy = trade_price + takeeprofitt * MT5functions.Get_Pip_Value(symbol) # take profit price for sells
    

    new_order_type = ordertype.lower()
    if new_order_type == "buy":
        typee = buy_market
        order_type = market_execution
        sl = stoplosssprice
        tp = take_profit_price_buy

    if new_order_type == "buy limit":
        typee = buy_limit
        order_type = market_limit_order
        sl = stoplosssprice
        tp = take_profit_price_buy
    if new_order_type == "buy stop":
        typee = buy_stop
        order_type = market_limit_order
        sl = stoplosssprice
        tp = take_profit_price_buy
    if new_order_type == "sell":
        typee = sell_market
        order_type = market_execution
        sl = stoplosssprice
        tp = take_profit_price_sell
    if new_order_type == "sell limit":
        typee = sell_limit
        order_type = market_limit_order
        sl = stoplosssprice
        tp = take_profit_price_sell
    if new_order_type == "sell stop":
        typee = sell_stop
        order_type = market_limit_order
        sl = stoplosssprice
        tp = take_profit_price_sell


    if re.search(r"limit|stop",new_order_type):
        request = {
            "action": order_type, # what type of order
            "symbol": symbol, # symbol
            "type": typee, # order type
            "volume": lot, #lot size
            "price": trade_price,
            "deviation": slipppage,
            "sl": sl,
            "tp": tp,
            "comment": orderrcomment, # order comment
            "magic": maggicnumberr, # magic number
            "type_time": MetaTrader5.ORDER_TIME_GTC, # order stays active until it is manually closed
            "type_filling": MetaTrader5.ORDER_FILLING_RETURN, 
        }
    if re.search(r"buy|sell",new_order_type) and not re.search(r"limit|stop",new_order_type):
        request = {
            "action": order_type, # what type of order
            "symbol": symbol, # symbol
            "type": typee, # order type
            "volume": lot, #lot size
            "price": trade_price,
            "deviation": slipppage,
            "sl": sl,
            "tp": tp,
            "comment": orderrcomment, # order comment
            "magic": maggicnumberr, # magic number
            "type_time": MetaTrader5.ORDER_TIME_GTC, # order stays active until it is manually closed
            "type_filling": MetaTrader5.ORDER_FILLING_IOC
        }

    if not MetaTrader5.order_send(request): # if it doesnt send an order
        print("Order send failed, error code =",MetaTrader5.last_error()) # send error
        quit()


def SendCustomOrderTP(symbol,ordertype, lot, orderprice,slipppage, stoplosss,takeeprofittprice,orderrcomment,maggicnumberr): 

    
    if orderprice == "ask":
        trade_price = MetaTrader5.symbol_info_tick(symbol).ask # getting the ask price
    if orderprice == "bid":
        trade_price = MetaTrader5.symbol_info_tick(symbol).bid # getting the bid price

    buy_market = MetaTrader5.ORDER_TYPE_BUY # buy market execution order
    buy_limit = MetaTrader5.ORDER_TYPE_BUY_LIMIT # buy limit order
    buy_stop = MetaTrader5.ORDER_TYPE_BUY_STOP # buy stop order

    sell_market = MetaTrader5.ORDER_TYPE_SELL # sell market execution order
    sell_limit = MetaTrader5.ORDER_TYPE_SELL_LIMIT # sell limit order
    sell_stop = MetaTrader5.ORDER_TYPE_SELL_STOP # sell stop order

    market_execution = MetaTrader5.TRADE_ACTION_DEAL # market order
    market_limit_order = MetaTrader5.TRADE_ACTION_PENDING# limit order

    stop_loss_price_sell = trade_price + stoplosss * MT5functions.Get_Pip_Value(symbol) # stop loss price for sells

    stop_loss_price_buy = trade_price - stoplosss * MT5functions.Get_Pip_Value(symbol) # stop loss price for sells

    

    new_order_type = ordertype.lower()
    if new_order_type == "buy":
        typee = buy_market
        order_type = market_execution
        sl = stop_loss_price_buy
        tp = takeeprofittprice

    if new_order_type == "buy limit":
        typee = buy_limit
        order_type = market_limit_order
        sl = stop_loss_price_buy
        tp = takeeprofittprice
    if new_order_type == "buy stop":
        typee = buy_stop
        order_type = market_limit_order
        sl = stop_loss_price_buy
        tp = takeeprofittprice
    if new_order_type == "sell":
        typee = sell_market
        order_type = market_execution
        sl = stop_loss_price_sell
        tp = takeeprofittprice
    if new_order_type == "sell limit":
        typee = sell_limit
        order_type = market_limit_order
        sl = stop_loss_price_sell
        tp = takeeprofittprice
    if new_order_type == "sell stop":
        typee = sell_stop
        order_type = market_limit_order
        sl = stop_loss_price_sell
        tp = takeeprofittprice


    if re.search(r"limit|stop",new_order_type):
        request = {
            "action": order_type, # what type of order
            "symbol": symbol, # symbol
            "type": typee, # order type
            "volume": lot, #lot size
            "price": trade_price,
            "deviation": slipppage,
            "sl": sl,
            "tp": tp,
            "comment": orderrcomment, # order comment
            "magic": maggicnumberr, # magic number
            "type_time": MetaTrader5.ORDER_TIME_GTC, # order stays active until it is manually closed
            "type_filling": MetaTrader5.ORDER_FILLING_RETURN, 
        }
    if re.search(r"buy|sell",new_order_type) and not re.search(r"limit|stop",new_order_type):
        request = {
            "action": order_type, # what type of order
            "symbol": symbol, # symbol
            "type": typee, # order type
            "volume": lot, #lot size
            "price": trade_price,
            "deviation": slipppage,
            "sl": sl,
            "tp": tp,
            "comment": orderrcomment, # order comment
            "magic": maggicnumberr, # magic number
            "type_time": MetaTrader5.ORDER_TIME_GTC, # order stays active until it is manually closed
            "type_filling": MetaTrader5.ORDER_FILLING_IOC
        }

    if not MetaTrader5.order_send(request): # if it doesnt send an order
        print("Order send failed, error code =",MetaTrader5.last_error()) # send error
        quit()
