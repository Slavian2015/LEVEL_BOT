import requests
from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceOrderException
import time
from main_abs import IStock
from DBprovider import Database


class LiveBrockerManager(IStock, Database):
    def __init__(self, api_key, api_secret, telega_api_key, telega_api_secret):
        Database.__init__(self)
        self.telega_api_key = telega_api_key
        self.telega_api_secret = telega_api_secret
        self.dbase = Database()
        self.bclient = Client(api_key=api_key, api_secret=api_secret)

    def new_data(self, sym, timeframe, days_ago):
        try:
            data = self.bclient.get_historical_klines(sym, timeframe.lower(), f"{days_ago} day ago UTC")
            return data
        except Exception as e:
            print(e)
            return False

    def new_rools(self):
        try:
            x = self.dbase.update_rools()
            return x
        except Exception as e:
            print(e)
            return False

    def futures_change_leverage(self, new_leverage, new_symbol):
        self.bclient.futures_change_leverage(leverage=int(new_leverage), symbol=new_symbol.lower())
        return

    def futures_change_margin_type(self, new_margin, new_symbol):
        self.bclient.futures_change_margin_type(marginType=new_margin, symbol=new_symbol)
        return

    def place_buy_market_future_order(self, symbol=None, amount=0):
        n = 0
        while True:
            try:
                order = self.bclient.futures_create_order(
                    symbol=symbol,
                    side='BUY',
                    type='MARKET',
                    quantity=amount)

                return order
            except BinanceOrderException as order:
                if n < 2:
                    if '1021' in order:
                        time.sleep(1)
                        n += 1
                    else:
                        print(f"Future BUY Order Error: \n {order}")
                        return order
                else:
                    print(f"Future BUY Order Error: \n {order}")
                    return order
            except BinanceAPIException as order:
                if n < 2:
                    if '1021' in order:
                        time.sleep(1)
                        n += 1
                    else:
                        print(f"Future BUY Order Error: \n {order}")
                        return order
                else:
                    print(f"Future BUY Order Error: \n {order}")
                    return order

    def place_sell_market_future_order(self, symbol=None, amount=0):
        n = 0
        while True:
            try:
                order = self.bclient.futures_create_order(
                    symbol=symbol,
                    side='SELL',
                    type='MARKET',
                    quantity=amount)

                return order
            except BinanceOrderException as order:
                if n < 2:
                    if '1021' in order:
                        time.sleep(1)
                        n += 1
                    else:
                        print(f"Future SELL Order Error: \n {order}")
                        return order
                else:
                    print(f"Future SELL Order Error: \n {order}")
                    return order
            except BinanceAPIException as order:
                if n < 2:
                    if '1021' in order:
                        time.sleep(1)
                        n += 1
                    else:
                        print(f"Future BUY Order Error: \n {order}")
                        return order
                else:
                    print(f"Future BUY Order Error: \n {order}")
                    return order

    def close_buy_market_future_order(self, symbol=None, amount=0):
        n = 0
        while True:
            try:
                order = self.bclient.futures_create_order(
                    symbol=symbol,
                    side='BUY',
                    type='MARKET',
                    reduceOnly='true',
                    quantity=amount)

                return order
            except BinanceOrderException as order:
                if n < 2:
                    if '1021' in order:
                        time.sleep(1)
                        n += 1
                    else:
                        print(f"Future BUY Order Error: \n {order}")
                        return order
                else:
                    print(f"Future BUY Order Error: \n {order}")
                    return order
            except BinanceAPIException as order:
                if n < 2:
                    if '1021' in order:
                        time.sleep(1)
                        n += 1
                    else:
                        print(f"Future BUY Order Error: \n {order}")
                        return order
                else:
                    print(f"Future BUY Order Error: \n {order}")
                    return order

    def close_sell_market_future_order(self, symbol=None, amount=0):
        n = 0
        while True:
            try:
                order = self.bclient.futures_create_order(
                    symbol=symbol,
                    side='SELL',
                    type='MARKET',
                    reduceOnly='true',
                    quantity=amount)

                return order
            except BinanceOrderException as order:
                if n < 2:
                    if '1021' in order:
                        time.sleep(1)
                        n += 1
                    else:
                        print(f"Future SELL Order Error: \n {order}")
                        return order
                else:
                    print(f"Future SELL Order Error: \n {order}")
                    return order
            except BinanceAPIException as order:
                if n < 2:
                    if '1021' in order:
                        time.sleep(1)
                        n += 1
                    else:
                        print(f"Future BUY Order Error: \n {order}")
                        return order
                else:
                    print(f"Future BUY Order Error: \n {order}")
                    return order

    def check_balance(self):
        # pass
        # pid2 = subprocess.Popen(["python", "/usr/local/WB/dashboard/BINANCE/combo_new_balance.py"]).pid
        return

    def order_buy_market(self, symbol=None, amount=0):
        try:
            self.bclient.order_market_buy(symbol=symbol, quantity=str(amount))
            return True
        except BinanceOrderException as e:
            print(f"BinanceOrderException: \n {e} \n symbol={symbol}, quantity={str(amount)}")
            return False

        except BinanceAPIException as e:
            print(f"BinanceAPIException: \n {e} \n symbol={symbol}, quantity={str(amount)}")
            return False

    def order_sell_market(self, symbol, amount):
        try:
            self.bclient.order_market_sell(symbol=symbol, quantity=str(amount))
            return True
        except BinanceOrderException as e:
            print(f"BinanceOrderException: \n {e} \n symbol={symbol}, quantity={str(amount)}")
            return False

        except BinanceAPIException as e:
            print(f"BinanceAPIException: \n {e} \n symbol={symbol}, quantity={str(amount)}")
            return False

    def order_buy_limit(self, symbol, amount, price):
        try:
            self.bclient.order_limit_buy(symbol=symbol,
                                         quantity=str(amount),
                                         price=str(price))
            return True
        except BinanceOrderException as e:
            print(f"BinanceOrderException: \n {e} \n symbol={symbol}, quantity={str(amount)}")
            return False

        except BinanceAPIException as e:
            print(f"BinanceAPIException: \n {e} \n symbol={symbol}, quantity={str(amount)}")
            return False

    def order_sell_limit(self, symbol, amount, price):
        try:
            self.bclient.order_limit_sell(symbol=symbol,
                                          quantity=str(amount),
                                          price=str(price))
            return True
        except BinanceOrderException as e:
            print(f"BinanceOrderException: \n {e} \n symbol={symbol}, quantity={str(amount)}")
            return False

        except BinanceAPIException as e:
            print(f"BinanceAPIException: \n {e} \n symbol={symbol}, quantity={str(amount)}")
            return False

    def my_spot_open_orders(self):
        try:
            orders = self.bclient.get_open_orders()
            return orders
        except Exception as e:
            print(e)
            return []

    def my_spot_account_info(self):
        try:
            my_bal = self.bclient.get_account()
            return my_bal
        except Exception as e:
            print(e)
            return []

    def my_futures_account_info(self):
        try:
            my_bal = self.bclient.futures_account()
            return my_bal
        except Exception as e:
            print(e)
            return []

    def cancel_spot_order(self, symbol=None, order_id=None):
        my_reponse = {"error": False, "result": None}
        try:
            order = self.bclient.cancel_order(symbol=symbol, orderId=order_id)
            my_reponse["result"] = order
        except BinanceOrderException as e:
            my_reponse["result"] = str(e)
            my_reponse["error"] = True
        except BinanceAPIException as e:
            my_reponse["result"] = str(e)
            my_reponse["error"] = True
        return my_reponse

    def telega_msg(self, msg):
        try:
            send_text = f'https://api.telegram.org/bot{self.telega_api_key}' \
                        f'/sendMessage?chat_id={self.telega_api_secret}' \
                        f'&parse_mode=Markdown&text={msg}'
            requests.get(send_text)
            return True
        except Exception as e:
            print(e)
            return False

    def get_all_tickers(self):
        try:
            data = self.bclient.get_all_tickers()
            return data
        except Exception as e:
            print(e)
            return False

    def get_my_avg_price(self, symbol=None):
        try:
            data = self.bclient.bclient.get_avg_price(symbol=symbol)
            return data
        except Exception as e:
            print(e)
            return False