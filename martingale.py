import MT5functions
import MetaTrader5
import ordersettings


def ModifyTP(takeprofit, symbol, magicnumber, op_type):
    i = 0
    total_limit_orders = MetaTrader5.orders_total()
    total_market_orders = MetaTrader5.positions_total()
    order_symbol = MT5functions.order_info(symbol, "symbol")
    order_magic_number = MT5functions.order_info(symbol, "magic number")
    order_type = MT5functions.order_info(symbol, "type")
    order_tp = MT5functions.order_info(symbol, "take profit")
    order_ticket = MT5functions.order_info(symbol, "ticket")
    order_open_price = MT5functions.order_info(symbol, "open price")
    order_sl = MT5functions.order_info(symbol, "stop loss")

    total_orders = total_limit_orders + total_market_orders

    while i < total_orders:
        if order_symbol == symbol and order_magic_number == magicnumber and order_type == op_type:
            if round((takeprofit - order_tp), 5) != 0:
                ordersettings.OrderModify(
                    symbol, order_ticket, order_open_price, order_sl, takeprofit)
        i += 1


def OpenedOrdersCount(symbol, magicnumber, op_type):
    total = 0
    i = 0
    total_limit_orders = MetaTrader5.orders_total()
    total_market_orders = MetaTrader5.positions_total()
    total_orders = total_limit_orders + total_market_orders
    order_symbol = MT5functions.order_info(symbol, "symbol")
    order_magic_number = MT5functions.order_info(symbol, "magic number")
    order_type = MT5functions.order_info(symbol, "type")

    while i < total_orders:
        if order_symbol == symbol and order_magic_number == magicnumber and order_type == op_type:
            total += 1
        i += 1
    return total


def SelectLastOrder(symbol, magicnumber, op_type):
    result = False

    total_limit_orders = MetaTrader5.orders_total()
    total_market_orders = MetaTrader5.positions_total()
    total_orders = total_limit_orders + total_market_orders

    order_symbol = MT5functions.order_info(symbol, "symbol")
    order_magic_number = MT5functions.order_info(symbol, "magic number")
    order_type = MT5functions.order_info(symbol, "type")
    i = total_orders - 1

    while i >= 0:
        if order_symbol == symbol and order_magic_number == magicnumber and order_type == op_type:
            result = True
            break
        i -= 1
    return result


def CheckMartingale(symbol, magicnumber, op_type, pipsTP):
    order_profit = MT5functions.order_info(symbol, "profit")
    ask_price = MetaTrader5.symbol_info_tick(
        symbol).ask
    bid_price = MetaTrader5.symbol_info_tick(
        symbol).bid
    open_order_price = MT5functions.order_info(symbol, "open price")
    order_type = MT5functions.order_info(symbol, "type")

    op_buy = MetaTrader5.ORDER_TYPE_BUY
    op_sell = MetaTrader5.ORDER_TYPE_SELL

    if SelectLastOrder(symbol, magicnumber, op_type) and order_profit < 0:
        if order_type == op_buy and abs((open_order_price - ask_price) / MT5functions.Get_Pip_Value(symbol)) >= pipsTP:
            return True
        if order_type == op_sell and abs((open_order_price - bid_price) / MT5functions.Get_Pip_Value(symbol)) >= pipsTP:
            return True
    return False


def use_martingale(symbol, magic_number, stop_loss_price, multiplier, pips_activation, pips_tp, trades, order_comment):
    order_type = MT5functions.order_info(symbol, "type")

    op_buy = MetaTrader5.ORDER_TYPE_BUY
    op_sell = MetaTrader5.ORDER_TYPE_SELL
    if order_type == op_buy:
        martin = CheckMartingale(symbol, magic_number, op_buy, pips_activation)

        if martin:
            martingale(symbol, magic_number, op_buy, stop_loss_price,
                       10, multiplier, pips_tp, trades, order_comment)
    if order_type == op_sell:
        martin = CheckMartingale(symbol, magic_number,
                                 op_sell, pips_activation)

        if martin:
            martingale(symbol, magic_number, op_sell, stop_loss_price,
                       10, multiplier, pips_tp, trades, order_comment)


def martingale(symbol, magic_number, op_type, stoploss, max_slippage, lot_multiplier, pips_tp, trades, order_comment):
    order_type = MT5functions.order_info(symbol, "type")
    order_profit = MT5functions.order_info(symbol, "profit")
    order_lotsize = MT5functions.order_info(symbol, "lot size")

    op_buy = MetaTrader5.ORDER_TYPE_BUY
    op_sell = MetaTrader5.ORDER_TYPE_SELL

    order_lots = 0
    total = OpenedOrdersCount(symbol, magic_number, op_type)

    if trades > total > 0:

        if order_type == op_buy:

            if SelectLastOrder(symbol, magic_number, op_buy) and order_profit <= 0:
                order_lots = round((order_lotsize * lot_multiplier), 2)
            else:
                order_lots = order_lotsize

            MetaTrader5.symbol_info_tick(symbol)  # refreshing rates

            ordersettings.OrderSend(symbol, "buy", order_lots, "ask", max_slippage,
                                    True, stoploss, False, pips_tp, order_comment, magic_number)

            order_take_profit = MT5functions.order_info(symbol, "take profit")
            ModifyTP(order_take_profit, symbol, magic_number, op_type)

        if order_type == op_sell:

            if SelectLastOrder(symbol, magic_number, op_sell) and order_profit <= 0:
                order_lots = round((order_lotsize * lot_multiplier), 2)
            else:
                order_lots = order_lotsize

            MetaTrader5.symbol_info_tick(symbol)  # refreshing rates

            ordersettings.OrderSend(symbol, "sell", order_lots, "bid", max_slippage,
                                    True, stoploss, False, pips_tp, order_comment, magic_number)

            order_take_profit = MT5functions.order_info(symbol, "take profit")
            ModifyTP(order_take_profit, symbol, magic_number, op_type)
