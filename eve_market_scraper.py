from datetime import datetime
import requests
import time
import csv
import pandas


def downloadData(region_l, type_l, o_file, u_name, t_sleep, day_limit=30):
    """downloads all the data for the regions and types and dumps them to the
    output csv"""

    t_1 = datetime.now()
    data_str = ""
    ln_r = len(region_l)
    ln_t = len(type_l)
    chk = (ln_t * day_limit) / 10000
    stp = ln_t / chk
    base_url = "http://api.eve-marketdata.com/api/item_history2.txt"
    for j, r in enumerate(region_l):
        for i in range(chk):
            s_t_l = type_l[(i * stp):((i + 1) * stp)]
            t_str = ",".join([str(t) for t in s_t_l])
            res = requests.post(base_url, {"char_name": u_name,
                                           "region_ids": r,
                                           "type_ids": t_str})
            data_str += res.text
            print datetime.now() - t_1, ((j * chk + i) * 100.) / (ln_r * chk)
            time.sleep(t_sleep)
        s_t_l = type_l[(chk * stp):]
        t_str = ",".join([str(t) for t in s_t_l])
        res = requests.post(base_url, {"char_name": u_name,
                                       "region_ids": r,
                                       "type_ids": t_str,
                                       "days": day_limit})
        data_str += res.text
    o_data = open(o_file, "wb")
    o_data.write(data_str)
    o_data.close()


def loadRawData(csv_f):
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


def joinNewData(m_csv_f, n_csv_f):
    """loads the new data and adds it to the old"""

    n_data = loadRawData(n_csv_f)
    m_data = pandas.read_csv(m_csv_f)
    m_data = m_data.drop("Unnamed: 0", 1)
    m_data["date"] = pandas.to_datetime(m_data["date"])
    m_data = pandas.concat([m_data, n_data])
    m_data = m_data.drop_duplicates()
    m_data.to_csv(m_csv_f)
    return m_data
