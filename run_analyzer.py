from analyze_routes import *
from extract_data import *
import sys
import os


dr = sys.argv[1]
routes_f = sys.argv[2]
route_num = int(sys.argv[3])
good_num = int(sys.argv[4])
vol_limit = int(sys.argv[5])
t_delta = -int(sys.argv[6])


os.chdir(dr)
data = extractor(t_delta)
routes = compareRoute(data, route_num, good_num, vol_limit)
storeRoutes(routes, routes_f)
