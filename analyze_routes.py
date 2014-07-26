import pandas


def optimalRoute(start, finish, data, good_num, vol_limit,
                 id_type="solarSystemID"):
    """determines the optimal portfolio of goods to ship from start to
    finish"""

    # get the data subsets
    start_d = data[data[id_type] == start]
    finish_d = data[data[id_type] == finish]

    # get the samples for the market price
    b_start_samples = marketSampler(start_d)
    # b_finish_samples = marketSampler(finish_d)
    # s_start_samples = marketSampler(start_d, 0)
    s_finish_samples = marketSampler(finish_d, 0)

    # get the volume
    b_start_vol = marketVolume(start_d)
    # b_finish_vol = marketVolume(finish_d)
    # s_start_vol = marketVolume(start_d, 0)
    s_finish_vol = marketVolume(finish_d, 0)

    # get the highest earning goods above a certain volume
    return compareGoods(b_start_samples, b_start_vol,
                        s_finish_samples, s_finish_vol,
                        vol_limit, good_num)
