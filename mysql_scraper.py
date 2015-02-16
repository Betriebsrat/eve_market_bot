import zlib
import zmq
import simplejson
import time
from datetime import datetime
import MySQLdb
import mysql_fn
import ConfigParser

def main():
    context = zmq.Context()
    subscriber = context.socket(zmq.SUB)

    # Connect to the first publicly available relay.
    subscriber.connect('tcp://relay-us-central-1.eve-emdr.com:8050')
    # Disable filtering.
    subscriber.setsockopt(zmq.SUBSCRIBE, "")

    # open db
    rdb = MySQLdb.connect(host=host, user=user, passwd=passwd, db=db, user_unicode=True, charset="utf8")
    cursor = self.rdb.cursor()
    cursor.execute('SET NAMES utf8mb4')
    cursor.execute("SET CHARACTER SET utf8mb4")
    cursor.execute("SET character_set_connection=utf8mb4")
    cursor.execute("SET character_set_server=utf8mb4"

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
                for r in market_data["rowsets"]:
                    mysql_fn.insertOrder(cursor, r, table)
            print ind, datetime.now() - t_1
        except Exception as e:
            print e
            time.sleep(30)
        ind += 1

if __name__ == '__main__':
    main()
