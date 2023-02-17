import MetaTrader5
import MT5functions
import ordersettings

def Take_Partials(symbol, magicnumber, break_start, close_percentage, break_stop, break_start_2, break_start_3, break_start_4):

    ask_price = MetaTrader5.symbol_info_tick(symbol).ask
    bid_price = MetaTrader5.symbol_info_tick(symbol).bid

    op_buy =MetaTrader5.ORDER_TYPE_BUY
    op_sell = MetaTrader5.ORDER_TYPE_SELL

    orders_total = MetaTrader5.positions_total()
    
    i = 0


    while i < orders_total:# loops through each order
        order_type = MT5functions.order_info(symbol,"type")
        order_magic_number = MT5functions.order_info(symbol,"magic number")
        order_symbol = MT5functions.order_info(symbol,"symbol")
        order_ticket = MT5functions.order_info(symbol,"ticket")
        order_stop_loss = MT5functions.order_info(symbol,"stop loss")
        order_take_profit = MT5functions.order_info(symbol,"take profit")
        order_open_price = MT5functions.order_info(symbol,"open price")

        order_current_price = MT5functions.order_info(symbol,"current price")

        order_lot_size = MT5functions.order_info(symbol,"lot size")
        pip_value = MT5functions.Get_Pip_Value(symbol)
        symbol_digits = MT5functions.symbol_info(symbol, "digits")

        # check if symbol and magic number match
        if order_magic_number == magicnumber and order_symbol == symbol:

        # to move stop loss the first time

            # buys
            if order_type == op_buy and (order_stop_loss < order_open_price or order_stop_loss == 0) and ask_price - order_open_price > break_start * pip_value:

                stop_loss_new = order_open_price # define new stop loss as the open order price

                if break_stop != 0: # if break stop is 0, then the stop loss just the open order price
                    stop_loss_new = order_open_price + break_stop * pip_value # otherwise add the break stop pips to it

                if round(stop_loss_new,symbol_digits) > round(order_stop_loss,symbol_digits): # if new stop loss > current stop loss
                    
                    # move stop loss
                    ordersettings.OrderModify(symbol,order_ticket,order_open_price,stop_loss_new,order_take_profit)

                    # close a pecentage of our current lot size
                    close_lot = round(((order_lot_size/100) * close_percentage),2)

                    # take partials
                    ordersettings.OrderClose(symbol,order_ticket,close_lot,100)

            # sells
            if order_type == op_sell and (order_stop_loss > order_open_price or order_stop_loss == 0) and order_open_price - bid_price > break_start * pip_value:

                stop_loss_new = order_open_price # define new stop loss as the open order price

                if break_stop != 0: # if break stop is 0, then the stop loss just the open order price
                    stop_loss_new = order_open_price - break_stop * pip_value # otherwise add the break stop pips to it

                 # if new stop loss < current stop loss, or there is no order stop loss
                if round(stop_loss_new,symbol_digits) < round(order_stop_loss,symbol_digits) or order_stop_loss == 0:

                    # move stop loss
                    ordersettings.OrderModify(symbol,order_ticket,order_open_price,stop_loss_new,order_take_profit)

                    # close a pecentage of our current lot size
                    close_lot = round(((order_lot_size/100) * close_percentage),2)


                    # take partials
                    ordersettings.OrderClose(symbol,order_ticket,close_lot,100)


        # to move stop loss the second time

            # buys
            if order_type == op_buy and (order_stop_loss >= order_open_price or order_stop_loss == 0) and ask_price - order_stop_loss > break_start_2 * pip_value:

                stop_loss_new = order_stop_loss # define new stop loss as the current stop loss price

                if break_start_2 != 0: # if break start is 0, then the stop loss just the current stop loss price
                    stop_loss_new = order_stop_loss + break_start_2 * pip_value # otherwise add the 2nd break start pips to it

                if round(stop_loss_new,symbol_digits) > round(order_stop_loss,symbol_digits): # if new stop loss > current stop loss
                    
                    # move stop loss
                    ordersettings.OrderModify(symbol,order_ticket,order_open_price,stop_loss_new,order_take_profit)

                    # close a pecentage of our current lot size
                    close_lot = ((order_lot_size/100) * close_percentage)

                    # take partials
                    ordersettings.OrderClose(symbol,order_ticket,close_lot,100)

            # sells
            if order_type == op_sell and (order_stop_loss <= order_open_price or order_stop_loss == 0) and order_stop_loss - bid_price > break_start_2 * pip_value:

                stop_loss_new = order_stop_loss # define new stop loss as the open order price

                if break_start_2 != 0: # if break stop is 0, then the stop loss just the open order price
                    stop_loss_new = order_stop_loss - break_start_2 * pip_value # otherwise add the break stop pips to it

                 # if new stop loss < current stop loss, or there is no order stop loss
                if round(stop_loss_new,symbol_digits) < round(order_stop_loss,symbol_digits) or order_stop_loss == 0:

                    # move stop loss
                    ordersettings.OrderModify(symbol,order_ticket,order_open_price,stop_loss_new,order_take_profit)

                    # close a pecentage of our current lot size
                    close_lot = ((order_lot_size/100) * close_percentage)

                    # take partials
                    ordersettings.OrderClose(symbol,order_ticket,close_lot,100)

        # to move stop loss the third time

            # buys
            if order_type == op_buy and (order_stop_loss >= order_open_price or order_stop_loss == 0) and ask_price - order_stop_loss > break_start_3 * pip_value:

                stop_loss_new = order_stop_loss # define new stop loss as the current stop loss price

                if break_start_3 != 0: # if break start is 0, then the stop loss just the current stop loss price
                    stop_loss_new = order_stop_loss + break_start_3 * pip_value # otherwise add the 2nd break start pips to it

                if round(stop_loss_new,symbol_digits) > round(order_stop_loss,symbol_digits): # if new stop loss > current stop loss
                    
                    # move stop loss
                    ordersettings.OrderModify(symbol,order_ticket,order_open_price,stop_loss_new,order_take_profit)

                    # close a pecentage of our current lot size
                    close_lot = ((order_lot_size/100) * close_percentage)

                    # take partials
                    ordersettings.OrderClose(symbol,order_ticket,close_lot,100)

            # sells
            if order_type == op_sell and (order_stop_loss <= order_open_price or order_stop_loss == 0) and order_stop_loss - bid_price > break_start_3 * pip_value:

                stop_loss_new = order_stop_loss # define new stop loss as the open order price

                if break_start_3 != 0: # if break stop is 0, then the stop loss just the open order price
                    stop_loss_new = order_stop_loss - break_start_3 * pip_value # otherwise add the break stop pips to it

                 # if new stop loss < current stop loss, or there is no order stop loss
                if round(stop_loss_new,symbol_digits) < round(order_stop_loss,symbol_digits) or order_stop_loss == 0:

                    # move stop loss
                    ordersettings.OrderModify(symbol,order_ticket,order_open_price,stop_loss_new,order_take_profit)

                    # close a pecentage of our current lot size
                    close_lot = ((order_lot_size/100) * close_percentage)

                    # take partials
                    ordersettings.OrderClose(symbol,order_ticket,close_lot,100)

        # to move stop loss the fourth time

            # buys
            if order_type == op_buy and (order_stop_loss >= order_open_price or order_stop_loss == 0) and ask_price - order_stop_loss > break_start_4 * pip_value:

                stop_loss_new = order_stop_loss # define new stop loss as the current stop loss price

                if break_start_4 != 0: # if break start is 0, then the stop loss just the current stop loss price
                    stop_loss_new = order_stop_loss + break_start_4 * pip_value # otherwise add the 2nd break start pips to it

                if round(stop_loss_new,symbol_digits) > round(order_stop_loss,symbol_digits): # if new stop loss > current stop loss
                    
                    # move stop loss
                    ordersettings.OrderModify(symbol,order_ticket,order_open_price,stop_loss_new,order_take_profit)

                    # close a pecentage of our current lot size
                    close_lot = ((order_lot_size/100) * close_percentage)

                    # take partials
                    ordersettings.OrderClose(symbol,order_ticket,close_lot,100)

            # sells
            if order_type == op_sell and (order_stop_loss <= order_open_price or order_stop_loss == 0) and order_stop_loss - bid_price > break_start_4 * pip_value:

                stop_loss_new = order_stop_loss # define new stop loss as the open order price

                if break_start_4 != 0: # if break stop is 0, then the stop loss just the open order price
                    stop_loss_new = order_stop_loss - break_start_4 * pip_value # otherwise add the break stop pips to it

                 # if new stop loss < current stop loss, or there is no order stop loss
                if round(stop_loss_new,symbol_digits) < round(order_stop_loss,symbol_digits) or order_stop_loss == 0:

                    # move stop loss
                    ordersettings.OrderModify(symbol,order_ticket,order_open_price,stop_loss_new,order_take_profit)

                    # close a pecentage of our current lot size
                    close_lot = ((order_lot_size/100) * close_percentage)

                    # take partials
                    ordersettings.OrderClose(symbol,order_ticket,close_lot,100)
        i +=1
