import pandas
import numpy
import heapq


def getTopSSID(data, limit):
    """gets the top limited number of ids"""

    ss_ids = data["solarSystemID"].unique()
    types = []
    ln_ss = len(ss_ids)
    for i, s in enumerate(ss_ids):
        types.append(len(data[data["solarSystemID"] == s]["typeID"].unique()))
        print (i * 100.) / ln_ss, i, ln_ss
    max_l = heapq.nlargest(limit, types)
    return [ss_ids[max_l.index(m)] for m in max_l], max_l


def marketVolume(data, type_ids, buy=1):
    """gets the volume for the data"""

    vol_l = []
    order_data = data[data["bid"] == buy]
    for g in type_ids:
        vol_l.append(order_data[order_data["typeID"] == g]["volRemaining"].sum())
    return vol_l


def genMeanSamp(data):
    """generates normal samples for the mean of the data subset"""

    return numpy.random.normal(data["price"].mean(), 10, 1000)


def marketSampler(data, type_ids, buy=1):
    """does a sample for the mean"""

    samp_l = []
    order_data = data[data["bid"] == buy]
    for g in type_ids:
        samp_l.append(genMeanSamp(order_data[order_data["typeID"] == g]))
    return samp_l


def compareGoods(b_start_samples, b_start_vol, s_start_samples,
                 s_start_vol, b_finish_samples, b_finish_vol,
                 s_finish_samples, s_finish_vol, vol_limit, good_num,
                 type_ids):
    """returns the maximum return goods
    
    NOTE: This currently only takes into account the mean I would
    like to add something to account for variance as well later
    
    The way this currently works is that it gets the gains from buying
    in start and selling in start, along with the gains from buying in
    start and selling in finish.  It then takes N goods that maximize
    the gains from selling in finish over start

    """

    mu = []
    r_type_ids = []

    for i in range(len(s_start_samples)):
        
        # NOTE: these are not necessary for the way I'm doing it
        # if however you wanted to compare the s_diff with f_diff
        # in some way this would be necessary

        # s_diff = s_start_samples[i] - b_start_samples[i]
        # f_diff = s_finish_samples[i] - b_finish_samples[i]
        # fs_diff = s_finish_samples[i] - b_start_samples[i]
        # Right now this works by taking the difference between the amount
        # you could see in one station vs the other over the sell price
        # in the original station, this is just the "returns"
        if b_finish_vol[i] > vol_limit:
            mu.append(((s_finish_samples[i] - s_start_samples[i]) / s_start_samples[i]).mean())
            r_type_ids.append(type_ids[i])

    max_l = heapq.nlargest(good_num, mu)
    return [r_type_ids[max_l.index(m)] for m in max_l], max_l


def naiveCompare(start_d, finish_d, type_ids, good_num):
    """gets the naive values here"""

    output = []
    o_start_d = start_d[start_d["bid"] == 0]
    o_finish_d = finish_d[finish_d["bid"] == 0]
    ln = len(type_ids)
    for i, g in enumerate(type_ids):
        s_m = o_start_d[o_start_d["typeID"] == g]["price"].mean()
        f_m = o_finish_d[o_finish_d["typeID"] == g]["price"].mean()
        output.append((f_m - s_m) / s_m)
        print (i * 100.) / ln

    max_l = heapq.nlargest(good_num, output)
    return [type_ids[max_l.index(m)] for m in max_l], max_l


def naiveOptimalRoute(start, finish, data, good_num, vol_limit,
                      id_type="solarSystemID"):
    """gets a more naive estimate"""

    # get teh data subsets
    start_d = data[data[id_type] == start]
    finish_d = data[data[id_type] == finish]

    # builds the unique type id
    t_s_s = set(start_d[start_d["bid"] == 0]["typeID"].unique())
    t_s_b = set(start_d[start_d["bid"] == 1]["typeID"].unique())
    t_f_s = set(finish_d[finish_d["bid"] == 0]["typeID"].unique())
    t_f_b = set(finish_d[finish_d["bid"] == 1]["typeID"].unique())
    type_ids = list(t_s_s.intersection(t_s_b).intersection(t_f_s).intersection(t_f_b))

    # get datasets that contain the correct ids
    start_d = start_d[start_d["typeID"].isin(type_ids)]
    finish_d = finish_d[finish_d["typeID"].isin(type_ids)]

    return naiveCompare(start_d, finish_d, type_ids, good_num)



def optimalRoute(start, finish, data, good_num, vol_limit,
                 id_type="solarSystemID"):
    """determines the optimal portfolio of goods to ship from start to
    finish"""

    # get the data subsets
    start_d = data[data[id_type] == start]
    finish_d = data[data[id_type] == finish]

    # builds the unique type id
    t_s_s = set(start_d[start_d["bid"] == 0]["typeID"].unique())
    t_s_b = set(start_d[start_d["bid"] == 1]["typeID"].unique())
    t_f_s = set(finish_d[finish_d["bid"] == 0]["typeID"].unique())
    t_f_b = set(finish_d[finish_d["bid"] == 1]["typeID"].unique())
    type_ids = list(t_s_s.intersection(t_s_b).intersection(t_f_s).intersection(t_f_b))

    # get datasets that contain the correct ids
    start_d = start_d[start_d["typeID"].isin(type_ids)]
    finish_d = finish_d[finish_d["typeID"].isin(type_ids)]

    # get the samples for the market price
    b_start_samples = marketSampler(start_d, type_ids)
    b_finish_samples = marketSampler(finish_d, type_ids)
    s_start_samples = marketSampler(start_d, type_ids, 0)
    s_finish_samples = marketSampler(finish_d, type_ids, 0)

    # get the volume
    b_start_vol = marketVolume(start_d, type_ids)
    b_finish_vol = marketVolume(finish_d, type_ids)
    s_start_vol = marketVolume(start_d, type_ids, 0)
    s_finish_vol = marketVolume(finish_d, type_ids, 0)

    # get the highest earning goods above a certain volume
    return compareGoods(b_start_samples, b_start_vol,
                        s_start_samples, s_start_vol,
                        b_finish_samples, b_finish_vol,
                        s_finish_samples, s_finish_vol,
                        vol_limit, good_num, type_ids)


def compareRoutes(data, route_num, good_num, vol_limit,
                  id_type="solarSystemID"):
    """will find the routes that are the most profitable"""

    routes = []
    for s in data[id_type].unique():
        for f in data[id_type].unique():
            routes.append(optimalRoute(s, f, data, good_num, vol_limit,
                                       id_type))
            print s, f

    routes = [sum(r) for r in routes]
    return heapq.nlargest(route_num, routes)
