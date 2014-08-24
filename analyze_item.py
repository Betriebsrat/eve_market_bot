from datetime import datetime
import cPickle
import pandas
import numpy
import heapq
import csv


def loadIds(csv_f):
    """load ids"""

    reader = csv.reader(open(csv_f, "rb"))
    return [r for r in reader][1:]


def getPriceEstimate(data):
    """gets the price estimate for the data subset"""

    data = data[abs(data["price"] - data["price"].mean()) < (2 * data["price"].std())]
    return data["price"].mean()


def getVolume(data):
    """gets the volume for a data subset"""

    return data["volRemaining"].sum()


def getProfits(finish, start):
    """generates the profits for moving between the two points"""

    return (finish - start) / start


def tradeMat(data, th_ids, type_id, bid=0):
    """generates a matrix of returns for each pair of trade hubs"""

    t_1 = datetime.now()
    s_data = data[data["typeID"] == type_id][data["bid"] == bid]
    ln = len(th_ids)
    res = numpy.zeros(shape=(ln, ln))
    for i, r_i in enumerate(th_ids):
        for j, r_j in enumerate(th_ids):
            ss_data_i = s_data[s_data["solarSystemID"] == int(r_i[1])]
            ss_data_j = s_data[s_data["solarSystemID"] == int(r_j[1])]
            p_est_i = getPriceEstimate(ss_data_i)
            p_est_j = getPriceEstimate(ss_data_j)
            res[i, j] = getProfits(p_est_j, p_est_i)
            print datetime.now() - t_1, ((i * ln + j) * 100.) / (ln * ln)
    return res


def optimalSS(data, type_id, vol_limit, station_limit, bid=0, mxmn=0):
    """gets the optimal solar system ids and the mean price for the
    specified inputs"""

    t_1 = datetime.now()
    s_data = data[data["typeID"] == type_id][data["bid"] == bid]
    ss_ids = data["solarSystemID"].unique()
    price_l = []
    ss_l = []
    ln_ss = len(ss_ids)
    for i, s in enumerate(ss_ids):
        ss_data = s_data[s_data["solarSystemID"] == s]
        if getVolume(ss_data) > vol_limit:
            price_l.append(getPriceEstimate(ss_data))
            ss_l.append(s)
        print datetime.now() - t_1, (i * 100.) / ln_ss
    # now get max/min elements
    if mxmn == 0:
        mxmn_l = heapq.nlargest(station_limit, price_l)
    if mxmn == 1:
        mxmn_l = heapq.nsmallest(station_limit, price_l)
    return [ss_l[price_l.index(m)] for m in mxmn_l], mxmn_l
