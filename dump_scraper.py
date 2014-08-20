from datetime import datetime, timedelta
import requests
import StringIO
import gzip


def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)


def downloadDate(str_date):
    """downloads the file for the date object"""

    t_1 = datetime.now()
    url = "https://eve-central.com/dumps/"
    results = requests.get(url + "%s.dump.gz" % str_date).read()
    inF = gzip.GzipFile(fileobj=StringIO.StringIO(results))
    outF = open("%s.dump" % str_date, "wb")
    outF.write(inF.read())
    outF.close()
    print datetime.now() - t_1, str_date


def downloadDateRange(s_date, e_date):
    """iterates through daterange and downloads files"""
    
    # get initiale files and remove old zips
    f_names = os.listdir(".")
    for f in f_names:
        if "gz" in f:
            os.remove(f)
    # get date file names
    f_names = os.listdir(".")
    dates = [r.split(".")[0] for r in f_names]
    for d in daterange(s_date, e_date):
        str_date = d.strftime("%Y-%m-%d")
        if str_date not in dates:
            downloadDate(str_date)
    # remove new zip files
    f_names = os.listdir(".")
    for f in f_names:
        if "gz" in f:
            os.remove(f)
