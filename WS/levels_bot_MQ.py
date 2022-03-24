import sys
from datetime import datetime
from zigzag import peak_valley_pivots
import pandas as pd
import pika
import time
import json
import warnings
from scipy.stats import linregress
import numpy as np
from talib import ATR
import math

warnings.filterwarnings("ignore")

#################################   SHOW ALL ROWS & COLS   ####################################
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.expand_frame_repr', False)
pd.set_option('max_colwidth', None)


def normal_round(num, ndigits=0):
    if ndigits == 0:
        return int(num + 0.5)
    else:
        digit_value = 10 ** ndigits
        return int(num * digit_value + 0.5) / digit_value


def round_decimals_down(number: float, decimals: int = 2):
    if not isinstance(decimals, int):
        raise TypeError("decimal places must be an integer")
    elif decimals < 0:
        raise ValueError("decimal places has to be 0 or more")
    elif decimals == 0:
        return math.floor(number)

    factor = 10 ** decimals
    return math.floor(number * factor) / factor


class Strategy:
    def __init__(self,
                 timer="1min",
                 my_symbols=None,
                 leverage="1",
                 min_amount="20",
                 brocker_manager=None
                 ):

        self.BrockerManager = brocker_manager
        params = pika.URLParameters('amqp://guest:guest@YOUR_IP:PORT/%2f')
        params.socket_timeout = 5
        self.connection = pika.BlockingConnection(params)
        self.channel = self.connection.channel()

        self.main_data = {}
        self.main_BD = {}
        self.symbols = [my_symbols]
        self.hadg_symbol = self.symbols[0].upper()
        self.bot_ping = True
        self.min_amount = float(min_amount)

        self.last_time = datetime.strptime('01 Nov 2020', '%d %b %Y')
        self.signal_time = datetime.strptime('01 Nov 2020', '%d %b %Y')
        self.high_trend = []
        self.low_trend = []
        self.Number1 = 0
        self.timer = timer

        self.uptrend = 1000000
        self.downtrend = 0

        self.leverage = int(float(leverage))
        self.stop_list = ["BNB", "BUSD", "USDT", "UAH", "EUR", "NFT"]
        self.atr_up = 0
        self.atr_down = 0

        self.n_rools = {}
        self.n_rools_futures = {}

        self.my_sl = 0
        self.my_tp = 0
        self.extra_price = 0

    def calc(self, dft):
        dft.reset_index(drop=True, inplace=True)
        X = dft['close'].values
        pivots = peak_valley_pivots(X, 0.002, -0.002)

        dft['sig'] = pivots
        points = []
        line_high = []
        line_low = []
        line_high_container = []
        line_low_container = []

        for ind in dft.index:
            if dft['sig'].iloc[ind] == -1 or dft['sig'].iloc[ind] == 1:
                points.append(dft['close'].iloc[ind])
                if len(points) >= 3:
                    if points[-3] < points[-1] < points[-2]:
                        dft['line_low'].iloc[ind] = points[-1]
                        line_low.append([dft['close'].iloc[ind], dft['ind_index'].iloc[ind]])

                    elif points[-1] > points[-3] > points[-2]:
                        dft['line_high'].iloc[ind] = points[-1]
                        line_high.append([dft['close'].iloc[ind], dft['ind_index'].iloc[ind]])

                    elif points[-1] < points[-2] > points[-3]:
                        dft['line_low'].iloc[ind] = points[-1]
                        line_low.append([dft['close'].iloc[ind], dft['ind_index'].iloc[ind]])

                    elif points[-3] > points[-1] > points[-2]:
                        dft['line_high'].iloc[ind] = points[-1]
                        line_high.append([dft['close'].iloc[ind], dft['ind_index'].iloc[ind]])
        if len(line_high) > 2:
            if line_high[-3][0] > line_high[-1][0]:
                line_high_container.append(line_high)
        if len(line_low) > 2:
            if line_low[-3][0] < line_low[-1][0]:
                line_low_container.append(line_low)

        return line_low_container, line_high_container

    def calc_trend(self, indexes, prices):
        slope, intercept, r_value, p_value, std_err = linregress(x=indexes, y=prices)
        return slope, intercept

    def run_main(self, df):

        df['line_low'] = None
        df['line_high'] = None
        df['Uptrend'] = None
        df['Downtrend'] = None

        df.reset_index(inplace=True)
        df['Number1'] = np.arange(len(df)) - 1
        df['ind_index'] = df.index

        if len(df) >= 51:
            trend_line_down, trend_line_up = self.calc(df)

            if trend_line_down and trend_line_up:
                self.Number1 = df['Number1'].iloc[-1]

                for i in trend_line_down:
                    cut_ind = int((i[-3][1] + i[-1][1]) / 2)
                    df_new_start2 = df[int(i[-3][1]):cut_ind]
                    df_new_start = df_new_start2[df_new_start2["close"] == df_new_start2["close"].min()].index.values
                    df_new_finish2 = df[cut_ind + 1:int(i[-1][1])]
                    df_new_finish = df_new_finish2[
                        df_new_finish2["close"] == df_new_finish2["close"].min()].index.values

                    if df_new_start.any():
                        if df['close'].iloc[df_new_start[0]] < df['close'].iloc[df_new_finish[-1]]:
                            r1, r2 = self.calc_trend([df_new_start[0], df_new_finish[-1]],
                                                     [df['close'].iloc[df_new_start[0]],
                                                      df['close'].iloc[df_new_finish[-1]]])
                            self.low_trend = [r1, r2]
                        else:
                            r1, r2 = self.calc_trend([i[-3][1], i[-1][1]],
                                                     [df['close'].iloc[int(i[-3][1])], df['close'].iloc[int(i[-1][1])]])
                            self.low_trend = [r1, r2]
                    else:
                        r1, r2 = self.calc_trend([i[-3][1], i[-1][1]],
                                                 [df['close'].iloc[int(i[-3][1])], df['close'].iloc[int(i[-1][1])]])
                        self.low_trend = [r1, r2]

                for i in trend_line_up:
                    cut_ind = int((i[-3][1] + i[-1][1]) / 2)
                    df_new_start2 = df[int(i[-3][1]):cut_ind]
                    df_new_start = df_new_start2[df_new_start2["close"] == df_new_start2["close"].max()].index.values

                    df_new_finish2 = df[cut_ind + 1:int(i[-1][1])]
                    df_new_finish = df_new_finish2[
                        df_new_finish2["close"] == df_new_finish2["close"].max()].index.values
                    if df_new_start.any():
                        if df['close'].iloc[df_new_start[0]] > df['close'].iloc[df_new_finish[-1]]:
                            r1, r2 = self.calc_trend([df_new_start[0], df_new_finish[-1]],
                                                     [df['close'].iloc[df_new_start[0]],
                                                      df['close'].iloc[df_new_finish[-1]]])
                            self.high_trend = [r1, r2]
                        else:
                            r1, r2 = self.calc_trend([i[-3][1], i[-1][1]],
                                                     [df['close'].iloc[int(i[-3][1])], df['close'].iloc[int(i[-1][1])]])
                            self.high_trend = [r1, r2]
                    else:
                        r1, r2 = self.calc_trend([i[-3][1], i[-1][1]],
                                                 [df['close'].iloc[int(i[-3][1])], df['close'].iloc[int(i[-1][1])]])
                        self.high_trend = [r1, r2]

    def open_hadg_buy(self, my_price):
        new_amount_future = normal_round(
            self.min_amount / float(my_price),
            self.n_rools_futures[self.hadg_symbol]["decimals"])

        if self.n_rools_futures[self.hadg_symbol]["decimals"] == 0:
            new_amount_future = int(float(new_amount_future))

        # if not self.BrockerManager.place_buy_market_future_order(symbol=self.hadg_symbol, amount=new_amount_future):
        #     self.close_symbol()
        #     return

        current_price = normal_round(float(my_price), self.n_rools[self.hadg_symbol]['price'])
        my_message = f"\n(TRIANGLE) BUY {self.hadg_symbol}\ncurrent price: {current_price} | new amount: {new_amount_future}"
        self.BrockerManager.telega_msg(my_message)
        print(my_message)

        self.main_BD[self.hadg_symbol]["hadg_fond"] = new_amount_future
        self.main_BD[self.hadg_symbol]["direct"] = 1

        self.main_BD[self.hadg_symbol]["hadg_fond_start_price"] = current_price

        self.main_BD[self.hadg_symbol]["hadg_fond_take_profit"] = current_price + ((current_price - self.atr_down) * 2)
        self.main_BD[self.hadg_symbol]["hadg_fond_stop_loss"] = self.atr_down

    def open_hadg_sell(self, my_price):
        new_amount_future = normal_round(
            self.min_amount / float(my_price),
            self.n_rools_futures[self.hadg_symbol]["decimals"])

        if self.n_rools_futures[self.hadg_symbol]["decimals"] == 0:
            new_amount_future = int(float(new_amount_future))

        # if not self.BrockerManager.place_sell_market_future_order(symbol=self.hadg_symbol, amount=new_amount_future):
        #     self.close_symbol()
        #     return

        current_price = normal_round(float(my_price), self.n_rools[self.hadg_symbol]['price'])
        my_message = f"\n(TRIANGLE) SELL {self.hadg_symbol}\ncurrent price: {current_price} | new amount: {new_amount_future}"
        self.BrockerManager.telega_msg(my_message)
        print(my_message)

        self.main_BD[self.hadg_symbol]["hadg_fond"] = new_amount_future
        self.main_BD[self.hadg_symbol]["direct"] = 2
        self.main_BD[self.hadg_symbol]["hadg_fond_start_price"] = current_price

        self.main_BD[self.hadg_symbol]["hadg_fond_take_profit"] = current_price - ((self.atr_up - current_price) * 2)
        self.main_BD[self.hadg_symbol]["hadg_fond_stop_loss"] = self.atr_up

    def exit_from_buy_hadg(self, my_price, status):
        # if not self.BrockerManager.close_sell_market_future_order(symbol=self.hadg_symbol,
        #                                                           amount=self.main_BD[sym]["hadg_fond"]):
        #     self.close_symbol()
        #     return

        percent = (float(my_price) - float(self.main_BD[self.hadg_symbol]["hadg_fond_start_price"])) / float(
            my_price) * 100
        profit = self.min_amount * percent / 100

        my_message = f"(TRIANGLE) exit_from_buy {self.hadg_symbol}\ncurrent price: {float(my_price)} \n {status} \n profit: {profit} USD / {round(percent, 2)} %"
        self.BrockerManager.telega_msg(my_message)
        print(my_message)

        self.BrockerManager.save_new_order(
            symbol=self.hadg_symbol,
            direction="LONG",
            percent=percent,
            profit=profit)

        self.main_BD[self.hadg_symbol]["hadg_fond_sum"].append(profit)

        self.main_BD[self.hadg_symbol]["hadg_fond"] = 0
        self.main_BD[self.hadg_symbol]["direct"] = 0
        self.main_BD[self.hadg_symbol]["hadg_fond_start_price"] = 0
        self.main_BD[self.hadg_symbol]["hadg_fond_start_usdt"] = 0
        self.main_BD[self.hadg_symbol]["hadg_fond_take_profit"] = 0
        self.main_BD[self.hadg_symbol]["hadg_fond_stop_loss"] = 0

    def exit_from_sell_hadg(self, my_price, status):
        # if not self.BrockerManager.close_buy_market_future_order(symbol=self.hadg_symbol,
        #                                                          amount=self.main_BD[sym]["hadg_fond"]):
        #     self.close_symbol()
        #     return

        percent = (self.main_BD[self.hadg_symbol]["hadg_fond_start_price"] - float(my_price)) / \
                  self.main_BD[self.hadg_symbol][
                      "hadg_fond_start_price"] * 100
        profit = self.min_amount * percent / 100
        self.main_BD[self.hadg_symbol]["hadg_fond_sum"].append(profit)
        my_message = f"(TRIANGLE) exit_from_sell {self.hadg_symbol}\ncurrent price: {float(my_price)} \n {status} \n profit: {profit} USD / {round(percent, 2)}%"
        print(my_message)

        self.BrockerManager.telega_msg(my_message)
        self.BrockerManager.save_new_order(
            symbol=self.hadg_symbol,
            direction="SHORT",
            percent=percent,
            profit=profit)

        self.main_BD[self.hadg_symbol]["hadg_fond"] = 0
        self.main_BD[self.hadg_symbol]["direct"] = 0
        self.main_BD[self.hadg_symbol]["hadg_fond_start_price"] = 0
        self.main_BD[self.hadg_symbol]["hadg_fond_start_usdt"] = 0
        self.main_BD[self.hadg_symbol]["hadg_fond_take_profit"] = 0
        self.main_BD[self.hadg_symbol]["hadg_fond_stop_loss"] = 0

    def algorithm(self):
        df = pd.DataFrame(self.main_data[self.symbols[0]],
                          columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time',
                                   'quote_av', 'trades', 'tb_base_av', 'tb_quote_av', 'ignore'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')

        df['close'] = pd.to_numeric(df['close'])
        df["high"] = pd.to_numeric(df["high"])
        df["low"] = pd.to_numeric(df["low"])
        df.reset_index(inplace=True)

        if self.timer != "1min":
            # df.to_csv(f'/usr/local/WB/WS/LEVELS/{self.symbols[0]}.csv')
            df_new = df.head(-1).groupby(pd.Grouper(key='timestamp', freq=f"{self.timer}")).agg({
                "open": "first",
                "high": "max",
                "low": "min",
                "close": "last",
                "volume": "sum",

            })
            df_new = df_new.dropna()
            df_new.reset_index(inplace=True)
        else:
            df_new = df

        df_new['atr'] = ATR(df_new["high"], df_new["low"], df_new["close"], timeperiod=20)
        df_new['atr_up'] = df_new['close'] + df_new['atr'] * 3
        df_new['atr_down'] = df_new['close'] - df_new['atr'] * 3

        self.atr_up = df_new['atr_up'].iloc[-1]
        self.atr_down = df_new['atr_down'].iloc[-1]

        if df_new['timestamp'].iloc[-2] != self.last_time:
            self.last_time = df_new['timestamp'].iloc[-2]

            df2 = df_new[df_new['timestamp'] >= self.signal_time]
            if len(df2) >= 51:
                self.run_main(df_new.tail(51))

            if self.high_trend and self.low_trend:
                self.Number1 += 1
                self.uptrend = self.high_trend[0] * self.Number1 + self.high_trend[-1]
                self.downtrend = self.low_trend[0] * self.Number1 + self.low_trend[-1]

                # print(f"uptrend: {self.uptrend}  /  downtrend: {self.downtrend}")

                if self.uptrend < self.downtrend:
                    point_line_middle = (self.uptrend + self.downtrend) / 2
                    self.uptrend = point_line_middle
                    self.downtrend = point_line_middle

                    # msg = f"LEVELS -> {self.symbols[0]}\n Price: {round(point_line_middle, 3)}"
                    # self.telega_msg(msg)
                    self.high_trend = []
                    self.low_trend = []
                    self.signal_time = df_new['timestamp'].iloc[-2]

            if self.main_BD[self.hadg_symbol.upper()]["hadg_fond"] == 0:
                if df_new['close'].iloc[-2] <= self.uptrend <= df_new['high'].iloc[-1]:
                    self.open_hadg_buy(df_new['close'].iloc[-1])
                elif df_new['close'].iloc[-2] >= self.downtrend >= df_new['low'].iloc[-1]:
                    self.open_hadg_sell(df_new['close'].iloc[-1])

    def on_change_price(self, ch, method, properties, body):
        data = json.loads(body.decode('utf8'))

        sym = data["symbol"].upper()
        if data['status'] != 'running':
            msg = f"(LEVELS) Server not running (Symbol: {sym})"
            self.BrockerManager.telega_msg(msg)
            time.sleep(2)
        else:
            if data['channel'] == "depth5f":
                my_ask = float(data["data"]['data']['a'][0][0])
                my_bid = float(data["data"]['data']['b'][0][0])
                self.extra_price = my_bid

                if self.main_BD[sym]["hadg_fond"] > 0:
                    if self.main_BD[sym]["direct"] == 1:
                        if my_ask < self.main_BD[sym]['hadg_fond_stop_loss']:
                            self.exit_from_buy_hadg(my_ask, "STOP LOSS")
                        elif my_bid >= self.main_BD[sym]['hadg_fond_take_profit']:
                            self.exit_from_buy_hadg(my_bid, "TAKE PROFIT")
                    else:
                        if my_ask < self.main_BD[sym]['hadg_fond_take_profit']:
                            self.exit_from_sell_hadg(my_ask, "TAKE PROFIT")
                        elif my_bid >= self.main_BD[sym]['hadg_fond_stop_loss']:
                            self.exit_from_sell_hadg(my_bid, "STOP LOSS")
            else:
                new_row = [data["data"]['data']['k']['t'],
                           data["data"]['data']['k']['o'],
                           data["data"]['data']['k']['h'],
                           data["data"]['data']['k']['l'],
                           data["data"]['data']['k']['c'],
                           data["data"]['data']['k']['v'],
                           data["data"]['data']['k']['T'],
                           None, None, None, None, None]
                if int(float(data["data"]['data']['k']['T'])) == int(float(self.main_data[sym][-1][6])):
                    self.main_data[sym][-1] = new_row
                elif int(float(data["data"]['data']['k']['T'])) > int(float(self.main_data[sym][-1][6])):
                    self.main_data[sym].append(new_row)
                    del self.main_data[sym][0]
                    self.algorithm()

    def prepare_k_lines(self):
        for i in self.symbols:
            print(f"New TRIANGLE data k_line START: \n {i}")
            para2 = self.BrockerManager.new_data(i.upper(), "1m", 2)
            self.main_data[i.upper()] = para2
            self.algorithm()
            time.sleep(0.5)

    def on_change_rools(self, ch, method, properties, body):
        data = json.loads(body.decode('utf8'))
        self.n_rools = data['spot']
        self.n_rools_futures = data['futures']

    def on_start(self):

        msg = f"(TRIANGLE) ON START {self.symbols[0]}"
        if self.BrockerManager.telega_msg(msg):
            print("\n", msg)

        if self.bot_ping:
            x = self.BrockerManager.new_rools()

            if x:
                self.n_rools_futures = x[0]['futures']
                self.n_rools = x[0]['spot']
            else:
                self.close_symbol()
                return

        for i in self.symbols:
            self.main_data[i.upper()] = []
            self.main_BD[i.upper()] = {"start_balance": self.min_amount,
                                       "START_USDT": self.min_amount,
                                       "START_COIN": self.min_amount,
                                       "start_price": 0,
                                       "hadg_fond": 0,
                                       "direct": 0,
                                       "hadg_fond_take_profit": 0,
                                       "hadg_fond_start_price": 0,
                                       "hadg_fond_start_usdt": 0,
                                       "hadg_fond_stop_loss": 0,
                                       "hadg_fond_sum": []}

            try:
                self.BrockerManager.futures_change_leverage(self.leverage, self.hadg_symbol.lower())
            except:
                pass

        self.prepare_k_lines()

        return

    def stop_comm(self, ch, method, properties, body):

        data = json.loads(body.decode('utf8'))

        print(f"STOP COMM (INSIDE): \n {data}")
        if method.routing_key == "STOP" and data["status"] == "STOP":
            self.bot_ping = False
            self.close_symbol()

    def close_symbol(self):
        try:
            self.channel.stop_consuming()
            self.channel.close()
            self.connection.close()
        except SystemExit:
            sys.exit(0)

    def run(self):
        msg = f"(TRIANGLE) start RUNNING"
        if self.BrockerManager.telega_msg(msg):
            print("\n", msg)

        """ ROOLS UPDATE """
        self.channel.exchange_declare(exchange='rools', exchange_type='fanout')
        result = self.channel.queue_declare(queue='', exclusive=True)
        queue_name = result.method.queue

        self.channel.queue_bind(exchange='rools', queue=queue_name)
        self.channel.basic_consume(queue=queue_name, on_message_callback=self.on_change_rools, auto_ack=True)

        """ STOP BOT ONLY """
        self.channel.exchange_declare(exchange=f'close_TRIANGLE_{self.hadg_symbol}', exchange_type='direct')
        result = self.channel.queue_declare(queue='', exclusive=True)
        queue_name = result.method.queue

        self.channel.queue_bind(exchange=f'close_TRIANGLE_{self.hadg_symbol}', queue=queue_name, routing_key="STOP")
        self.channel.basic_consume(queue=queue_name, on_message_callback=self.stop_comm, auto_ack=True)

        for i in self.symbols:
            my_exchange = f'{i.lower()}@depth5f'
            self.channel.exchange_declare(exchange=my_exchange, exchange_type='fanout')
            result = self.channel.queue_declare(queue='', exclusive=True)
            queue_name = result.method.queue
            self.channel.queue_bind(exchange=my_exchange, queue=queue_name)
            self.channel.basic_consume(queue=queue_name, on_message_callback=self.on_change_price, auto_ack=True)

        for i in self.symbols:
            my_exchange = f'{i.lower()}@kline_1mf'
            self.channel.exchange_declare(exchange=my_exchange, exchange_type='fanout')
            result = self.channel.queue_declare(queue='', exclusive=True)
            queue_name = result.method.queue
            self.channel.queue_bind(exchange=my_exchange, queue=queue_name)
            self.channel.basic_consume(queue=queue_name, on_message_callback=self.on_change_price, auto_ack=True)

        self.channel.start_consuming()
