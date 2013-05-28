#!/usr/bin/env python

from bikplugin import Bikplugin
from bicing import Bicingplugin
import ConfigParser
import datetime
import time
import os

def current_datetime(time_stamp):
        return datetime.datetime.fromtimestamp(time_stamp).strftime('%Y-%m-%d %H:%M:%S')

if __name__ == '__main__':
    # Changing execution to main.py path to avid problems when reading cfg files
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)
#    config = ConfigParser.ConfigParser()
#    config.read('datacollector.cfg')

    # Time between each data gathering event
#    interval = int(config.get('main', 'polling_interval'))

    # ts = timestamp
#    ts = time.time()
#    print(current_datetime(ts)+" - Initiating data collection")

#    while 1:
#    Bikplugin.get_data()
#    sleep(interval)
    ts = time.time()
#    try:
    print (current_datetime(ts)+" - Collecting data")
#        Bikplugin.get_data()
    Bicingplugin.get_bicing_data()
#    except Exception, e:
#        print("ERROR: An error occurred when collecting data at "+current_datetime(ts))
