import MetaTrader5
import sys


def MT5_login(account_number, account_password, broker_server_name):

    # this will open up meta trader 5
    if not MetaTrader5.initialize():  # if it doesnt open
        sys.exit("Couldn't start MT5, error code:",
                 MetaTrader5.last_error())  # send error and exit

    # logins to your account
    if not MetaTrader5.login(login=account_number, password=account_password, server=broker_server_name):
        # send error and exit if it doesnt login
        sys.exit("Couldn't login, error code:", MetaTrader5.last_error())
