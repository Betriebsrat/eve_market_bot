from datetime import datetime, timedelta
from eve_market_scraper import *
from analyze_data import *
import pandas


def fullRun(region_ids, type_ids, base_f):
    """keeps updated records of profitable opportunities"""

    while True:
        c_date = datetime.now()
        c_str_date = c_date.strftime("%Y-%m-%d")
        downloadData(region_ids, type_ids, "%s.csv" % c_str_date, "Slutsky Danneskjold", 6, 2)
        c_data = joinNewData(base_f, "%s.csv" % c_str_date)
        # get prev dates
        m_date = c_date + timedelta(-30)
        w_date = c_date + timedelta(-7)
        d_date = c_date + timedelta(-1)
        # get return matrices
        m_ret_mat_l = buildReturnsMatrix(c_data, region_ids, type_ids, m_date)
        w_ret_mat_l = buildReturnsMatrix(c_data, region_ids, type_ids, w_date)
        d_ret_mat_l = buildReturnsMatrix(c_data, region_ids, type_ids, d_date)
        for ret in [0.5, 0.75, 0.9]:
            m_routes = bestRoutes(c_data, m_ret_mat_l, region_ids, type_ids,
                                  1000000000, ret, m_date)
            w_routes = bestRoutes(c_data, w_ret_mat_l, region_ids, type_ids,
                                  100000000, ret, w_date)
            d_routes = bestRoutes(c_data, d_ret_mat_l, region_ids, type_ids,
                                  10000000, ret, d_date)
            # write monthly routes
            m_output = open("%d_%s_m_routes.csv" % (ret, c_str_date), "wb")
            writer = csv.writer(m_output)
            for route in m_routes:
                writer.writerow(route)
            m_output.close()
            # write monthly routes
            w_output = open("%d_%s_w_routes.csv" % (ret, c_str_date), "wb")
            writer = csv.writer(w_output)
            for route in w_routes:
                writer.writerow(route)
            w_output.close()
            # write monthly routes
            d_output = open("%d_%s_d_routes.csv" % (ret, c_str_date), "wb")
            writer = csv.writer(d_output)
            for route in d_routes:
                writer.writerow(route)
            d_output.close()
