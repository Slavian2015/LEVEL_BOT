import json
from pymongo import MongoClient, ASCENDING, DESCENDING
import os
import datetime

main_path_data = os.path.expanduser('/usr/local/WB/data/statistic.json')


class Database:

    def __init__(self):
        pass

    def save_new_order(self,
                       symbol="TESTUSDT",
                       direction="LONG",
                       percent=0,
                       profit=0):

        data = {"symbol": symbol,
                "direction": direction,
                "percent": percent,
                "profit": profit}

        try:
            with open(main_path_data, "r") as f:
                rools = json.load(f)
                rools[f"{datetime.datetime.now()}"] = data

            with open(main_path_data, "w") as f:
                json.dump(rools, f, indent=4)
            return True
        except Exception as e:
            print(f"ERROR save trade to db \n {e}")
            return False

    def update_rools(self):

        connection = MongoClient(os.environ.get("DATABASE_MONGO_URL"))
        x = connection['WS']['ROOLS'].find({"sku": 1})
        return x








