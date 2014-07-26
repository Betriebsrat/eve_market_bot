import zlib
import zmq
import simplejson
import time
from pymongo import MongoClient

def main():
    context = zmq.Context()
    subscriber = context.socket(zmq.SUB)

    # Connect to the first publicly available relay.
    subscriber.connect('tcp://relay-us-central-1.eve-emdr.com:8050')
    # Disable filtering.
    subscriber.setsockopt(zmq.SUBSCRIBE, "")

    # open db
    client = MongoClient()
    db = client["EveMarketDb"]
    o_col = db["OrderCollection"]
    h_col = db["HistoryCollection"]

    while True:
        try:
            # Receive raw market JSON strings.
            market_json = zlib.decompress(subscriber.recv())
            # Un-serialize the JSON data to a Python dict.
            market_data = simplejson.loads(market_json)
            if market_data["resultType"] == "order":
                o_col.insert(market_data)
            if market_data["resultType"] == "history":
                h_col.insert(market_data)
            print market_data["resultType"]
        except:
            time.sleep(30)

if __name__ == '__main__':
    main()
