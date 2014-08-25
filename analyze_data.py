from datetime import datetime
import pandas
import numpy


def genProfits(s_data, e_data):
    """generates profits from moving from one to the other"""

    num = (s_data["avgPrice"].mean() - e_data["avgPrice"].mean())
    den = (s_data["avgPrice"].mean())
    return num / den


def buildReturnsMatrix(data, region_l, type_l, date_limit):
    """gets the returns from moving from one region to another
    with each item"""

    t_1 = datetime.now()

    # lengths
    ln_region = len(region_l)
    ln_type = len(type_l)

    res_l = []
    for k, t in enumerate(type_l):
        t_data = data[data["typeID"] == t]
        ret_mat = numpy.zeros(shape=(ln_region, ln_region))
        for i, r_i in enumerate(region_l):
            for j, r_j in enumerate(region_l):
                s_data = t_data[t_data["regionID"] == r_i]
                e_data = t_data[t_data["regionID"] == r_j]
                sd_data = s_data[s_data["date"] >= date_limit]
                ed_data = e_data[e_data["date"] >= date_limit]
                ret_mat[i, j] = genProfits(sd_data, ed_data)
        res_l.append(ret_mat)
        print datetime.now() - t_1, (k * 100.) / ln_type
    return res_l


def bestRoutes(data, ret_l, region_l, type_l, val_limit, ret_limit, date_limit):
    """gets the best routes given some limits"""

    ln_type = len(type_l)
    t_1 = datetime.now()

    data = data[data["date"] >= date_limit]

    res_l = []
    k = 0
    for ret, t in zip(ret_l, type_l):
        t_data = data[data["typeID"] == t]
        for i, r_i in enumerate(region_l):
            for j, r_j in enumerate(region_l):
                ret_v = ret[i, j]
                s_data = t_data[t_data["regionID"] == r_i]
                e_data = t_data[t_data["regionID"] == r_j]
                s_val = s_data["avgPrice"] * s_data["volume"]
                s_val = s_val.sum()
                e_val = e_data["avgPrice"] * e_data["volume"]
                e_val = e_val.sum()
                if s_val > val_limit and e_val > val_limit and ret_v > ret_limit:
                    res_l.append([t, r_i, r_j, ret_v])
        print datetime.now() - t_1, (k * 100.) / ln_type
        k += 1
    return res_l
