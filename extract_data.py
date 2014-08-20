from pymongo import MongoClient
import pandas
from datetime import datetime, timedelta


def extractor(t_delta):
    """gets all the orders out of the db for the current dt"""

    client = MongoClient()
    db = client["EveMarketDb"]
    col = db["OrderCollection"]

    output = []

    var = ["regionID", "typeID", "price", "volRemaining", "range", "orderID",
           "volEntered", "minVolumne", "bid", "issueDate", "duration",
           "stationID", "solarSystemID"]

    # prep to check status
    # ln = col.count()
    ln = 60000
    i = 0
    t_1 = datetime.now()

    order_ids = []

    for c in col.find({"currentTime": {"$gt": datetime.now() + t_delta}}):
        for rs in c["rowsets"]:
            r_id = rs["regionID"]
            t_id = rs["typeID"]
            for r in rs["rows"]:
                # don't include orders that we already have in the data
                if r[3] not in order_ids:
                    output.append([r_id, t_id] + r)
                    order_ids.append(r[3])
        print (i * 100.) / ln, datetime.now() - t_1
        i += 1

    return pandas.DataFrame(output, columns=var) 
