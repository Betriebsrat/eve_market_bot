import zlib
import zmq
import simplejson
import time
from datetime import datetime
from pymongo import MongoClient
from datetime import datetime

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

    t_1 = datetime.now()
    ind = 0

    while True:
        try:
            # Receive raw market JSON strings.
            market_json = zlib.decompress(subscriber.recv())
            # Un-serialize the JSON data to a Python dict.
            market_data = simplejson.loads(market_json)
            market_data["currentTime"] = datetime.strptime(market_data["currentTime"].split("+")[0],
                                                           "%Y-%m-%dT%H:%M:%S")
            if market_data["resultType"] == "orders":
                o_col.insert(market_data)
            print ind, datetime.now() - t_1
        except Exception as e:
            print e
            time.sleep(30)
        ind += 1

if __name__ == '__main__':
    main()
