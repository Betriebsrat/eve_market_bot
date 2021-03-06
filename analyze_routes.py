from datetime import datetime
import cPickle
import pandas
import numpy
import heapq


def getTopSSID(data, limit):
    """gets the top limited number of ids"""

    t_1 = datetime.now()

    ss_ids = data["solarSystemID"].unique()
    val_l = []
    ln_ss = len(ss_ids)
    for i, s in enumerate(ss_ids):
        # we only want to keep solar systems that have a lot of "value" passing through them
        # value is just defined as price times quantity.  So basically I want the solar systems
        # that have the most money in them currently
        ss_data = data[data["solarSystemID"] == s]
        val = ss_data["volRemaining"] * ss_data["price"]
        val_l.append(val.sum())
        print (i * 100.) / ln_ss, datetime.now() - t_1, "top SS IDs"
    max_l = heapq.nlargest(limit, val_l)
    return [ss_ids[val_l.index(m)] for m in max_l]


def getPriceEstimate(data, t, bid):
    """generates the price estimate given the data"""

    s_data = data[data["typeID"] == t][data["bid"] == bid]
    # throw out data that is greater than two standard deviations away from the mean
    s_data = s_data[abs(s_data["price"] - s_data["price"].mean()) < (2 * s_data["price"].std())]
    return s_data["price"].mean()


def getProfits(finish, start):
    """generates the profits given the finish and start estimates"""

    return (finish - start) / start


def getVolume(data, t, bid):
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
        print (i * 100.) / ln, datetime.now() - t_1, ((ind_i * route_num + ind_j) * 100.) / (route_num * route_num)
    
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
                  top_ssids=None, id_type="solarSystemID"):
    """will find the routes that are the most profitable"""

    routes = {}

    if top_ssids is None:
        top_ssids = getTopSSID(data, route_num)

    t_1 = datetime.now()

    for i, s in enumerate(top_ssids):
        routes[s] = {}
        for j, f in enumerate(top_ssids):
            if i != j:
                goods = optimalRoute(s, f, data, good_num, vol_limit,
                                     i, j, route_num, t_1, id_type)
                routes[s][f] = {}
                for k, v in zip(goods[0], goods[1]):
                    routes[s][f][k] = v
    return routes


def getBestRoutes(routes, lower_limit):
    """gets the best routes above a certain return"""

    good_routes = []
    for s in routes:
        for f in routes[s]:
            for i in routes[s][f]:
                if routes[s][f][i] > lower_limit:
                    good_routes.append((s, f, routes[s][f][i], i))
    return good_routes


def mapNames(routes, loc_links, type_links):
    """builds a new dictionary of routes that use names in place
    of ids, this makes it easier to read"""

    n_routes = {}
    for s in routes:
        s_n = name_links[s]
        n_routes[s_n] = {}
        for f in routes[s]:
            f_n = name_links[f]
            n_routes[s_n][f_n] = {}
            for i in routes[s][f]:
                i_n = type_links[i]
                n_routes[s_n][f_n][i_n] = routes[s][f][i]
    return n_routes


def storeRoutes(routes, routes_F):
    """stores the routes in the route file"""

    cPickle.dump(routes, open(routes_f, "wb"))
