from datetime import datetime, timedelta
from extract_data import *
from analyze_routes import *
from dump_scraper import *
import time
import csv


def dumpRoutes(routes, o_file):
    """dumps the routes in a csv"""

    o_data = open(o_file, "wb")
    writer = csv.writer(o_data)
    writer.writerow(["start", "finish", "type", "profit"])
    for s in routes:
        for f in routes[s]:
            for k in routes[s][f]:
                writer.writerow([s, f, k, routes[s][f][k]])
    o_data.close()


def fullRun(s_date, t_sleep, vol_limit, ss_limit, route_limit, good_limit, o_file):
    """does the autorun"""

    t_1 = datetime.now()
    i = 0
    while True:
        c_date = datetime.now()
        downloadDateRange(s_date, c_date)
        print "dump downloaded", datetime.now() - t_1, i
        data = dataDumpExtractor(c_date, c_date + timedelta(days=1))
        print "data loaded", datetime.now() - t_1, i
        if i % 7 == 0:
            ss_ids = getTopSSID(data, ss_limit)
            print "new ssids loaded", datetime.now() - t_1, i
        routes = compareRoutes(data, route_limit, good_limit, vol_limit, ss_ids)
        print "new routes loaded", dateime.now() - t_1, i
        dumpRoutes(routes, o_file)
        print "routes stored", datetime.now() - t_1, i
        i += 1
        time.sleep(79200)

        
