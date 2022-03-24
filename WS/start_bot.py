import json
import sys
import argparse
import warnings

warnings.filterwarnings("ignore")

parser = argparse.ArgumentParser()
parser.add_argument('--symbol', help='BNBUSDT", "LUNAUSDT')
parser.add_argument('--leverage', help='1 or 2')
parser.add_argument('--timeframe', help='1m or 1h')
parser.add_argument('--amount', help='Amount')

args = parser.parse_args()

from levels_bot_bin import Strategy

main_path_settings = '/usr/local/WB/data/settings.json'

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
my_bot.on_start()

print(f"Bot TRIANGLE on_start: ok \n")
try:
    my_bot.run()
    print("TRIANGLE STOP")
except Exception as e:

    print(f"TRIANGLE EXTRA STOP\n {e} ")
    my_bot.close_symbol()
