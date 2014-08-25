from datetime import datetime
import pandas
import numpy
import csv


def loadData(csv_f):
    """reads data from a tab delimited csv file"""

    reader = csv.reader(open(csv_f, "rb"), delimiter="\t")
    reader_l = [r for r in reader]
    data = pandas.DataFrame(reader_l, columns=["typeID",
                                               "regionID",
                                               "date",
                                               "lowPrice",
                                               "highPrice",
                                               "avgPrice",
                                               "volume",
                                               "orders"])
    data["date"] = pandas.to_datetime(data["date"])
    data["typeID"] = data["typeID"].astype("int")
    data["regionID"] = data["regionID"].astype("int")
    data["lowPrice"] = data["lowPrice"].astype("float")
    data["highPrice"] = data["highPrice"].astype("float")
    data["avgPrice"] = data["avgPrice"].astype("float")
    data["volume"] = data["volume"].astype("float")
    data["orders"] = data["orders"].astype("float")
    return data


def genProfits(s_data, e_data):
    """generates profits from moving from one to the other"""

    num = (s_data["avgPrice"].mean() - e_data["avgPrice"].mean())
    den = (s_data["avgPrice"].mean())
    return num / den


def buildReturnsMatrix(data, region_l, type_l, date_limit):
    """gets the returns from moving from one region to another
    with each item"""

    # lengths
    ln_region = len(region_l)
    ln_type = len(type_l)

    res_l = []
    for t in type_l:
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
    return res_l
