import MetaTrader5
import sys


def MT5_login(account_number, account_password, broker_server_name):
    # this will open up meta trader 5 and login
    if not MetaTrader5.initialize(
                                login=account_number, # account number (int)
                                password=account_password, # account password (string)
                                server=broker_server_name # broker(string)
                                ):
         # send error and exit if it doesnt open
        sys.exit(f"Couldn't initialize and start MT5, error code = {MetaTrader5.last_error()}")
    else: # if it does open
        print("System initialized and account logged in")

    # enable automatic trading
    if not MetaTrader5.terminal_info().trade_allowed:
        print("Enable auto-trading")