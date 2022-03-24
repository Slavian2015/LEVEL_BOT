import json
import os
import sys
import argparse
import warnings
import signal
from levels_bot_bin import Strategy

main_path_data = os.path.expanduser('/usr/local/WB/data/running.json')
main_path_settings = '/usr/local/WB/data/settings.json'
warnings.filterwarnings("ignore")

parser = argparse.ArgumentParser()
parser.add_argument('--symbol', help='BNBUSDT", "LUNAUSDT')
parser.add_argument('--leverage', help='1 or 2')
parser.add_argument('--timeframe', help='1m or 1h')
parser.add_argument('--amount', help='Amount')

args = parser.parse_args()

with open(main_path_data, "r") as f:
    rools2 = json.load(f)

if rools2[args.symbol] != 0:
    pidid = rools2[args.symbol]
    rools2[args.symbol] = 0
    f = open(main_path_data, "w")
    json.dump(rools2, f)
    f.close()
    try:
        os.kill(int(pidid), signal.SIGKILL)
    except:
        pass

with open(main_path_settings, "r") as f:
    rools = json.load(f)

telega_api_key = rools["api_key_t"]
telega_api_secret = rools["api_secret_t"]

api_key = rools["api_key"]
api_secret = rools["api_secret"]


sys.path.insert(0, '/usr/local/WB/BACKEND')
from bin import LiveBrockerManager

brocker_manager = LiveBrockerManager(api_key,
                                     api_secret,
                                     telega_api_key,
                                     telega_api_secret)

my_bot = Strategy(
    timer=args.timeframe,
    my_symbols=args.symbol,
    leverage=args.leverage,
    min_amount=args.amount,
    brocker_manager=brocker_manager
)

my_bot.close_symbol()
