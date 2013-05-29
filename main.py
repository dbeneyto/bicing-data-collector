#!/usr/bin/env python

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
    config = ConfigParser.ConfigParser()
    config.read('datacollector.cfg')

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
    try:
        load_plugins = config.get('plugins', 'plugin_list').split(',')
    except Exception, e:
        print ("ERROR: An error occurred when reading datacollector.cfg configuration file")
    for plugin in load_plugins:
        print "Collecting data from "+plugin+" plugin"
        try:
            module = __import__(plugin)
            module_class = getattr(module, 'Datacollectorplugin')
            instance = module_class()
        except Exception, e:
            print ("ERROR: An error occurred when loading dynamic datacollector plugins")
        try:
            instance.get_data()        
        except Exception, e:
            print("ERROR: An error occurred when collecting data at "+current_datetime(ts))
