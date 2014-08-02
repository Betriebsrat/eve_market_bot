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
