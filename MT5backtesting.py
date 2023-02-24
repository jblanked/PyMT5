import charts
import trend
import pandas as pd
import pytz
import talib_functions as TA

class Run_Test:

    def __init__(self, pair, time_frame,year, month, day, starting_bar, max_bars,account_balance, testing_type):
        self.pair = pair
        self.timeframe = time_frame
        self.start = starting_bar
        self.amount = max_bars
        self.balance = account_balance
        self.testing = testing_type
        self.year = year
        self.month = month
        self.day = day


    def get_data(self,data_type):

        # Get the historical data for the symbol and timeframe as a pandas DataFrame
        symbol_data = charts.historical_data(self.pair, self.timeframe, self.start, self.amount)
        tick_data = charts.tick_data(self.pair,self.year,self.month,self.day)


        prices = symbol_data.drop(columns=["real_volume", "tick_volume", "spread"])

        edited = data_type.lower()

        if edited in ["close", "price_close"]:
            return prices['close']

        if edited in ["open", "price_open"]:
            return prices['open']

        if edited in ["high", "price_high"]:
            return prices['high']

        if edited in ["low", "price_low"]:
            return prices['low']
        
        if edited in ['ask', "current"]:
            return tick_data['ask']

        if edited == "order time":
            data_time = prices['time']
            data_time_seconds = pd.to_datetime(data_time, unit='s')

            # localize the pandas datetime objects to the UTC timezone
            localized_time = data_time_seconds.dt.tz_localize('UTC')

            # convert the localized pandas datetime objects to datetime objects with timezone information
            candle_times = localized_time.dt.tz_convert(pytz.utc)

            return candle_times

        if edited == "tick time":
            data_time =tick_data['time']
            data_time_seconds = pd.to_datetime(data_time, unit='s')

            # localize the pandas datetime objects to the UTC timezone
            localized_time = data_time_seconds.dt.tz_localize('UTC')

            # convert the localized pandas datetime objects to datetime objects with timezone information
            candle_times = localized_time.dt.tz_convert(pytz.utc)

            return candle_times



    def RSI(self,rsi_period, applied_price, buy_level, sell_level, take_profit, stop_loss, lotsize):

        total_entries = []
        total_stoplosses = []
        total_takeprofits = []
        total_times = []
        total_profit_loss = []
        balance = []
        dollar_value = trend.MT5functions.profit_in_dollars(self.pair,lotsize)
        


        # this function returns the RSI price
        rsi_price = TA.iRSI(self.pair, self.timeframe,rsi_period, applied_price, self.start, self.amount,self.year,self.month,self.day,self.testing)

        prices =self.get_data(applied_price)

        total_amount = len(prices)
        i = rsi_period

        initial_balance = self.balance
        account_balance = initial_balance
        max_drawdown = initial_balance
        initial_balance_loss = 0
        initial_balance_gain = 0

        positions = 0



        # iterate through the price data
        for i in range(rsi_period, total_amount):
            
            # calculate the RSI value for the current bar
            rsi_value = rsi_price[i]

            if self.testing == "control points":
                # get the current close price
                close_price = self.get_data("close")[i]
                #get the current order and RSI date
                order_date = self.get_data('order time')[i]

            if self.testing == "every tick":
                # get the ask for every tick
                close_price = self.get_data("ask")[i]
                order_date = self.get_data('tick time')[i]


            
            # check if the price is above the RSI 
            if rsi_value < buy_level and positions == 0:
                # buy at the current price
                entry_price = close_price
                total_entries.append(entry_price)

                stop_loss_price = entry_price - stop_loss
                total_stoplosses.append(stop_loss_price)

                take_profit_price = entry_price + take_profit
                total_takeprofits.append(take_profit_price)

                total_times.append(order_date)
                
                calc_take_profit_buy = trend.MetaTrader5.order_calc_profit(trend.MetaTrader5.ORDER_TYPE_BUY,self.pair,lotsize,entry_price,take_profit_price)
                calc_stop_loss_buy = trend.MetaTrader5.order_calc_profit(trend.MetaTrader5.ORDER_TYPE_BUY,self.pair,lotsize,entry_price,stop_loss_price)

                order_type = "Buy"
                positions += 1
                
            # check if the price is below the RSI 
            if rsi_value > sell_level and positions == 0:
                # sell at the current price
                entry_price = close_price
                total_entries.append(entry_price)

                stop_loss_price = entry_price + stop_loss
                total_stoplosses.append(stop_loss_price)

                take_profit_price = entry_price - take_profit
                total_takeprofits.append(take_profit_price)

                calc_take_profit_sell = trend.MetaTrader5.order_calc_profit(trend.MetaTrader5.ORDER_TYPE_SELL,self.pair,lotsize,entry_price,take_profit_price)
                calc_stop_loss_sell = trend.MetaTrader5.order_calc_profit(trend.MetaTrader5.ORDER_TYPE_SELL,self.pair,lotsize,entry_price,stop_loss_price)

                total_times.append(order_date)
                

                order_type = "Sell"
                positions += 1
                
                        
            # check if there is an open position
            if positions > 0:
                
                # check if the current price is above the take profit price

                if order_type == "Buy" and close_price >= take_profit_price:

                    
                    account_balance += calc_take_profit_buy
                    total_profit_loss.append("profit")
                    balance.append(account_balance)
                    initial_balance_gain += calc_take_profit_buy
                    positions = 0
                    
                # check if the current price is below the stop loss price
                elif order_type == "Buy" and close_price <= stop_loss_price:
                    
                    account_balance += calc_stop_loss_buy
                    total_profit_loss.append("loss")
                    balance.append(account_balance)
                    initial_balance_loss += calc_stop_loss_buy
                    positions = 0
                    
                # check if the current price is below the take profit price
                elif order_type == "Sell" and close_price <= take_profit_price:
                    
                    account_balance += calc_take_profit_sell
                    total_profit_loss.append("profit")
                    balance.append(account_balance)
                    initial_balance_gain += calc_take_profit_sell
                    positions = 0
                    
                # check if the current price is above the stop loss price
                elif order_type == "Sell" and close_price >= stop_loss_price:
                    
                    account_balance += calc_stop_loss_sell
                    total_profit_loss.append("loss")
                    balance.append(account_balance)
                    initial_balance_loss += calc_stop_loss_sell
                    positions = 0
                
                # max drawdown
                elif account_balance < max_drawdown:
                    max_drawdown = account_balance

        total_profit_loss.append('')
        balance.append('')

        profit_loss = round(account_balance-initial_balance,2)
        percent_profit_loss = round(((profit_loss/initial_balance) * 100),2)
        end_profit = round(initial_balance_gain,2)
        end_loss = round(initial_balance_loss,2)
        
        max_dd = round((((initial_balance - max_drawdown) / initial_balance) * 100),2)

        df = pd.DataFrame({"Entry": total_entries, "Result": total_profit_loss, "Balance": balance, "Take profit": total_takeprofits, "Stop loss": total_stoplosses, "Order time": total_times})

        df['Order time'] = pd.to_datetime(df['Order time']).dt.strftime('%Y-%m-%d %H:%M:%S')


        # display all rows and columns
        pd.set_option('display.max_rows', None)
        pd.set_option('display.max_columns', None)

        print(f"\n{df}")

        account_currency = trend.MT5functions.get_account_info("currency")

        print( f"\nTotal loss: {end_loss}")
        print( f"Total profit: {end_profit}")
        print( f"Final profit/loss: {profit_loss} {account_currency}")
        print(f'Max Drawdown: {max_dd}%')
        print( f"Percent Growth: {percent_profit_loss}%\nFinal Account Balance: {account_balance}\n")
