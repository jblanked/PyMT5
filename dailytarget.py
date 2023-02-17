from datetime import timedelta, datetime
import MetaTrader5
import ordersettings
import trend
import MT5functions
import pytz


def ApplyDailyTarget(symbol, daily_target, daily_loss, magicnumber):

    order_type = MT5functions.order_info(symbol, "type")
    order_symbol = MT5functions.order_info(symbol, "symbol")

    starting = TodaysStartingBalance(symbol, magicnumber)

    profit = MT5functions.get_account_info("equity") - starting
    profit_gained = (MT5functions.division(profit, starting)) * 100

    if profit_gained > daily_target:
        CloseAllOrders(order_symbol, magicnumber, order_type, True)
        return False

    if profit_gained < -1 * daily_loss:
        CloseAllOrders(order_symbol, magicnumber, order_type, True)
        return False

    return True


def TodaysStartingBalance(symbol, magicnumber):
    return MT5functions.get_account_info("balance") - TodaysClosedProfit(symbol, magicnumber)


def TodaysClosedProfit(symbol, magicnumber):

    # create a timezone object for UTC
    utc_tz = pytz.utc

    # Convert the float value returned by trend.iDate() to a datetime object in UTC
    day_start_time = datetime.fromtimestamp(trend.iDate(
        symbol, MT5functions.timeframe(1440), 0), tz=utc_tz)

    # get the number of orders in history
    yesterday = day_start_time - timedelta(days=1)
    today = datetime.now(tz=utc_tz)

    total = MetaTrader5.history_orders_total(yesterday, today)
    profit = 0

    i = 0

    while i < total:

        in_deal_data = MetaTrader5.history_deals_get(yesterday, today)

        if in_deal_data is None or len(in_deal_data) == 0:
            # No more deals available
            break

        order_symbol = in_deal_data[i].symbol
        order_magic_number = in_deal_data[i].magic

        if order_symbol == symbol and order_magic_number == magicnumber:
            op_buy = MetaTrader5.ORDER_TYPE_BUY
            op_sell = MetaTrader5.ORDER_TYPE_SELL

            order_ticket = in_deal_data[i].position_id

            out_deal_data = MetaTrader5.history_deals_get(
                position=order_ticket)

            order_type = out_deal_data[1].type

            order_profit = out_deal_data[1].profit

            order_swap = out_deal_data[1].swap
            order_commission = in_deal_data[1].commission

            order_time = datetime.fromtimestamp(out_deal_data[1].time)

            if order_type in (op_buy, op_sell):
                if order_time >= day_start_time:
                    profit += order_profit + order_swap + order_commission

        i += 1

    return profit


def CloseAllOrders(symbol, magicnumber, order_type, use_magic=True):
    open_orders = MetaTrader5.positions_total()

    op_buy = MetaTrader5.ORDER_TYPE_BUY
    op_sell = MetaTrader5.ORDER_TYPE_SELL

    i = 0

    while i < open_orders:
        order_ticket = MT5functions.order_info(symbol, "ticket")
        order_symbol = MT5functions.order_info(symbol, "symbol")
        order_magic_number = MT5functions.order_info(symbol, "magic number")

        if (order_magic_number == magicnumber or not use_magic) and order_symbol == symbol:
            if order_type in (op_buy, op_sell):
                KillTicket(symbol)
        i += 1


def KillTicket(symbol):
    open_orders = MetaTrader5.positions_total()

    op_buy = MetaTrader5.ORDER_TYPE_BUY
    op_sell = MetaTrader5.ORDER_TYPE_SELL

    i = 0

    while i < open_orders:
        order_ticket = MT5functions.order_info(symbol, "ticket")
        order_type = MT5functions.order_info(symbol, "type")
        order_symbol = MT5functions.order_info(symbol, "symbol")
        order_lotsize = MT5functions.order_info(symbol, "lot size")
        ask_price = MetaTrader5.symbol_info_tick(order_symbol).ask
        bid_price = MetaTrader5.symbol_info_tick(order_symbol).bid

        if order_type in (op_sell, op_buy):
            price = 0

            if order_type == op_buy:
                price = bid_price
            elif order_type == op_sell:
                price = ask_price

            ordersettings.OrderClose(
                order_symbol, order_ticket, order_lotsize, 10)

        i += 1
