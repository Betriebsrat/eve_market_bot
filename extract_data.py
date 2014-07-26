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
           "statinoID", "solarSystemID"]

    for c in col.find({"currentTime": {"$gt": datetime.now() + t_delta}}):
        for rs in c["rowsets"]:
            r_id = rs["regionID"]
            t_id = rs["typeID"]
            for r in rs["rows"]:
                output.append([r_id, t_id] + r)

    return pandas.DataFrame(output, columns=var) 