from datetime import datetime
import pandas
import numpy
import heapq


def getTopSSID(data, limit):
    """gets the top limited number of ids"""

    t_1 = datetime.now()

    ss_ids = data["solarSystemID"].unique()
    types = []
    ln_ss = len(ss_ids)
    for i, s in enumerate(ss_ids):
        types.append(len(data[data["solarSystemID"] == s]["typeID"].unique()))
        print (i * 100.) / ln_ss, datetime.now() - t_1, "top SS IDs"
    max_l = heapq.nlargest(limit, types)
    return [ss_ids[max_l.index(m)] for m in max_l], max_l


def getPriceEstimate(data, t, bid):
    """generates the price estimate given the data"""

    return data[data["typeID"] == t][data["bid"] == bid]["price"].mean()


def getProfits(finish, start):
    """generates the profits given the finish and start estimates"""

    return (finish - start) / start


def getVolume(finish, t, bid):
    """gets the volume for the goods being bought in finish"""

    return data[data["typeID"] == t][data["bid"] == bid]["volRemaining"].sum()


def compareGoods(start_d, finish_d, type_ids, good_num, vol_limit, ind_i,
                 ind_j, route_num, t_1):
    """gets the naive values here"""

    # output data
    output = []
    ids = []
    # bid 0 is sell, I'm comparing the sell prices
    ln = len(type_ids)
    for i, t in enumerate(type_ids):
        s_m = getPriceEstimate(start_d, t, 0)
        f_m = getPriceEstimate(finish_d, t, 0)
        if getVolume(finish_d, t, 1) > vol_limit: 
            output.append(getProfits(f_m, s_m))
            ids.append(t)
        print ((i * 100.) / ln,
               ((ind_i * ind_j + ind_j) * 100.) / (route_num * route_num),
               datetime.now() - t_1)

    max_l = heapq.nlargest(good_num, output)
    return [ids[max_l.index(m)] for m in max_l], max_l


def optimalRoute(start, finish, data, good_num, vol_limit,
                 ind_i, ind_j, route_num, t_1, id_type="solarSystemID"):
    """gets a more naive estimate"""

    # get teh data subsets
    start_d = data[data[id_type] == start]
    finish_d = data[data[id_type] == finish]

    # builds the unique type id
    t_s_s = set(start_d[start_d["bid"] == 0]["typeID"].unique())
    t_s_b = set(start_d[start_d["bid"] == 1]["typeID"].unique())
    t_f_s = set(finish_d[finish_d["bid"] == 0]["typeID"].unique())
    t_f_b = set(finish_d[finish_d["bid"] == 1]["typeID"].unique())
    type_ids = list(t_s_s.intersection(t_s_b)
                    .intersection(t_f_s)
                    .intersection(t_f_b))

    # get datasets that contain the correct ids
    start_d = start_d[start_d["typeID"].isin(type_ids)]
    finish_d = finish_d[finish_d["typeID"].isin(type_ids)]

    return compareGoods(start_d, finish_d, type_ids, good_num, vol_limit,
                        ind_i, ind_j, route_num, t_1)


def compareRoutes(data, route_num, good_num, vol_limit,
                  id_type="solarSystemID"):
    """will find the routes that are the most profitable"""

    routes = {}

    top_ssids = getTopSSID(data, route_num)

    t_1 = datetime.now()

    for i, s in enumerate(top_ssids):
        routes[s] = {}
        for j, f in enumerate(top_ssids):
            if i != j:
                goods = optimalRoute(s, f, data, good_num, vol_limit,
                                     i, j, route_num, t_1, id_type)
                routes[s][f] = goods
    return routes 
