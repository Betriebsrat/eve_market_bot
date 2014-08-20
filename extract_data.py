from pymongo import MongoClient
import pandas
from datetime import datetime, timedelta

def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)


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


def dataDumpExtractor(s_date, e_date):
    """loads the data for all of the dates and joins into one dataframe"""

    data = pandas.DataFrame(columns=["regionID", "typeID", "price",
                                     "volRemaining", "range", "orderID",
                                     "volEntered", "minVolumne", "bid",
                                     "issueDate", "duration",
                                     "stationID", "solarSystemID",
                                     "reportedBy", "reportedTime"])
    for d in daterange(s_date, e_date):
        t_data = pandas.read_csv(d.strftime("%Y-%m-%d.dump"))
        t_data = t_data.rename(columns={"orderid": "orderID",
                                        "regionid": "regionID",
                                        "systemid": "solarSystemID",
                                        "stationid": "stationID",
                                        "typeid": "typeID",
                                        "minvolume": "minVolume", 
                                        "volremain": "volRemaining",
                                        "volenter": "volEntered",
                                        "issued": "issueDate",
                                        "reportedby": "reportedBy",
                                        "reportedtime": "reportedTime"})
        t_data["issueDate"] = pandas.to_datetime(t_data["issueDate"])
        t_data["reportedTime"] = pandas.to_datetime(t_data["reportedTime"])
        data = pandas.concat([data, t_data])
    return data
        
