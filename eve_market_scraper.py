import requests


def downloadData(region_l, type_l, o_file, u_name):
    """downloads all the data for the regions and types and dumps them to the
    output csv

    NOTE: This does not automatically accomidate the eve marketdata 10000
    limit, you have to account for that yourself"""

    region_str = ",".join([str(r) for r in region_l])
    type_str = ",".join([str(r) for r in type_l])
    base_url = "http://api.eve-marketdata.com/api/item_history2.txt"
    res = requests.post(base_url, {"char_name": u_name, "region_ids": region_str,
                                   "type_ids": type_str})
    o_data = open(o_file, "wb")
    o_data.write(res.text)
    o_data.close()

