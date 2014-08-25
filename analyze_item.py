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


def getMaxTypeIDs(data, id_lim):
    """gets the maximum value elements"""

    t_1 = datetime.now()

    t_ids = data["typeID"].unique()
    val_l = []
    ln_t = len(t_ids)
    for i, t in enumerate(t_ids):
        t_data = data[data["typeID"] == t]
        val = t_data["volRemaining"] * t_data["price"]
        val_l.append(val.sum())
        print (i * 100.) / ln_t, datetime.now() - t_1, "top type IDs"
    max_l = heapq.nlargest(limit, val_l)
    return [t_ids[val_l.index(m)] for m in max_l], max_l


def getRoute(data, s_id, e_id):
    """gets the routes"""

    t_1 = datetime.now()
    s_data = data[(data["solarSystemID"] == s_id) | (data["solarSystemID"] == e_id)]
    t_ids = s_data["typeID"].unique()
    ln_t = len(t_ids)
    profit_l = []
    id_l = []
    vol_l = []
    for i, t in enumerate(t_ids):
        t_data = s_data[s_data["typeID"] == t]
        s_t_data = t_data[t_data["solarSystemID"] == s_id]
        e_t_data = t_data[t_data["solarSystemID"] == e_id]
        p_est_s = getPriceEstimate(s_t_data)
        p_est_e = getPriceEstimate(e_t_data)
        profit_l.append(getProfits(p_est_e, p_est_s))
        id_l.append(t)
        vol_l.append(getVolume(e_t_data))
        print datetime.now() - t_1, (i * 100.) / ln_t
    return profit_l, id_l, vol_l


def getMax(profit_l, id_l, vol_l, vol_limit, item_limit):
    """get the max elements"""
    
    o_profit_l = []
    o_vol_l = []
    o_id_l = []
    for p, i, v in zip(profit_l, id_l, vol_l):
        if v >= vol_limit:
            o_profit_l.append(p)
            o_vol_l.append(v)
            o_id_l.append(i)
    max_l = heapq.nlargest(item_limit, o_profit_l)
    return max_l, [o_vol_l[max_l.index(m)] for m in max_l], [o_id_l[max_l.index(m)] for m in max_l]


def dumpValues(profit_l, id_l, vol_l, o_file):
    """dumps the values to a csv file"""

    o_data = open(o_file, "wb")
    writer = csv.writer(o_data)
    for p, i, v in zip(profit_l, id_l, vol_l):
        writer.writerow([p, i, v])
    o_data.close()
    

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
