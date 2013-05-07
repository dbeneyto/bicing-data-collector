#!/usr/bin/env python

import ConfigParser
import time
from time import sleep
import datetime
from bikplugin import *

def current_datetime(time_stamp):
        return datetime.datetime.fromtimestamp(time_stamp).strftime('%Y-%m-%d %H:%M:%S')

if __name__ == '__main__':

    config = ConfigParser.ConfigParser()
    config.read('datacollector.cfg')

    # Time between each data gathering event
#    interval = int(config.get('main', 'polling_interval'))

    # ts = timestamp
    ts = time.time()
#    print(current_datetime(ts)+" - Initiating data collection")

#    while 1:
#    Bikplugin.get_data()
#    sleep(interval)
    ts = time.time()
    print (current_datetime(ts)+" - Collecting data")
    Bikplugin.get_data()
