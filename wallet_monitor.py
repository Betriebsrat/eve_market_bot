from datetime import datetime
import csv
import time
import eveapi


def loadTransactionIDs(csv_f):
    """loads the transaction ids"""

    t_ids = []
    reader = csv.reader(open(csv_f, "rb"))
    for r in reader:
        t_ids.append(r[0])
    return t_ids


def dumpData(t, t_ids, csv_f):
    """dumps the data if it isn't already in the file"""

    if t.transactionID not in t_ids:
        writer = csv.writer(open(csv_f, "ab"))
        writer.writerow([t.transactionID,
                         datetime.fromtimestamp(t.transactionDateTime),
                         t.quantity,
                         t.typeName,
                         t.typeID,
                         t.price,
                         t.clientID,
                         t.clientName,
                         t.stationID,
                         t.stationName,
                         t.transactionType,
                         t.transactionFor,
                         t.journalTransactionID])


def dataScraper(keyID, vCode, csv_f, t_sleep):
    """scrapes the wallet transactions and updates the csv"""

    # start time
    t_1 = datetime.now()

    # load the data, this is to check if the transactions are there or not
    t_ids = loadTransactionIDs(csv_f)

    # get the API connection
    api = eveapi.EVEAPIConnection()
    auth = api.auth(keyID=keyID, vCode=vCode)

    while True:
        try:
            transactions = auth.char.WalletTransactions()
            for t in transactions:
                dumpData(t, t_ids, csv_f)
            time.sleep(t_sleep)
            print datetime.now() - t_1
        except:
            time.sleep(30)


def genReturns(data_csv, ret_csv):
    """generates the returns for the items bought and sold"""

    data_dict = {}
    reader = csv.reader(open(data_csv, "rb"))
    
    # load the data
    for r in reader:
        if r[4] not in data_dict:
            # initalize data dict if not initalized
            data_dict[r[4]] = {}
            data_dict[r[4]]["buy"] = {}
            data_dict[r[4]]["sell"] = {}
            data_dict[r[4]]["buy"]["totValue"] = 0
            data_dict[r[4]]["buy"]["totQuantity"] = 0
            data_dict[r[4]]["sell"]["totValue"] = 0
            data_dict[r[4]]["sell"]["totQuantity"] = 0
        # store row value
        data_dict[r[4]][r[10]]["totValue"] += r[2] * r[5]
        data_dict[r[4]][r[10]]["totQuantity"] += r[2]

    # store results
    writer = csv.writer(open(ret_csv, "wb"))

    # now generate the returns
    for t in data_dict:
        if (data_dict[t]["buy"]["totValue"] != 0 and
                data_dict[t]["sell"]["totValue"] != 0):
            bval = data_dict[t]["buy"]["totValue"]
            sval = data_dict[t]["sell"]["totValue"]
            bqnt = data_dict[t]["buy"]["totQuantity"]
            sqnt = data_dict[t]["sell"]["totQuantity"]
            writer.writerow([t, sval - bval,
                             ((sval / sqnt) - (bval / bqnt)) / (bval / bqnt)])
