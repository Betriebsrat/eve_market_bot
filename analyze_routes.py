import pandas
import heapq

def marketVolume(data, buy=1)
    """gets the volume for the data"""

    vol_l = []
    order_data = data[data["bid"] == buy]
    for g in order_data["type_id"].unique():
        vol_l.append(order_data[order_data["type_id"] == g]["volRemaining"].sum())
    return vol_l


def compareGoods(b_start_samples, b_start_vol, s_start_samples,
                 s_start_vol, b_finish_samples, b_finish_vol,
                 s_finish_samples, s_finish_vol, vol_limit, good_num):
    """returns the maximum return goods
    
    NOTE: This currently only takes into account the mean I would
    like to add something to account for variance as well later
    
    The way this currently works is that it gets the gains from buying
    in start and selling in start, along with the gains from buying in
    start and selling in finish.  It then takes N goods that maximize
    the gains from selling in finish over start

    """

    mu = []

    for i in range(len(b_start_samples)):
        
        # NOTE: these are not necessary for the way I'm doing it
        # if however you wanted to compare the s_diff with f_diff
        # in some way this would be necessary

        # s_diff = s_start_samples[i] - b_start_samples[i]
        # f_diff = s_finish_samples[i] - b_finish_samples[i]
        # fs_diff = s_finish_samples[i] - b_start_samples[i]
        if b_finish_vol[i] > vol_limit:
            mu.append((s_finish_samples[i] - s_start_samples[i]).mean())

    return heapq.nlargest(good_num, mu)


def optimalRoute(start, finish, data, good_num, vol_limit,
                 id_type="solarSystemID"):
    """determines the optimal portfolio of goods to ship from start to
    finish"""

    # get the data subsets
    start_d = data[data[id_type] == start]
    finish_d = data[data[id_type] == finish]

    # get the samples for the market price
    b_start_samples = marketSampler(start_d)
    b_finish_samples = marketSampler(finish_d)
    s_start_samples = marketSampler(start_d, 0)
    s_finish_samples = marketSampler(finish_d, 0)

    # get the volume
    b_start_vol = marketVolume(start_d)
    b_finish_vol = marketVolume(finish_d)
    s_start_vol = marketVolume(start_d, 0)
    s_finish_vol = marketVolume(finish_d, 0)

    # get the highest earning goods above a certain volume
    return compareGoods(b_start_samples, b_start_vol,
                        s_start_samples, s_start_vol,
                        b_finish_samples, b_finish_vol,
                        s_finish_samples, s_finish_vol,
                        vol_limit, good_num)


def compareRoutes(data, route_num, good_num, vol_limit,
                  id_type="solarSystemID"):
    """will find the routes that are the most profitable"""

    routes = []
    for s in data[id_type].unique():
        for f in data[id_type].unique():
            routes.append(optimalRoute(s, f, data, good_num, vol_limit,
                                       id_type))

    routes = [sum(r) for r in routes]
    return heapq.nlargest(route_num, routes)
