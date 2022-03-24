from abc import ABC


class IStock(ABC):

    def new_data(self, sym, timeframe, days_ago):
        raise

    def update_main_data(self):
        raise

    def prepare_future_account(self):
        raise

    def place_buy_market_order(self):
        raise

    def place_sell_market_order(self):
        raise

    def check_balance(self):
        raise

    def run(self):
        raise

    def on_change_price(self):
        raise
