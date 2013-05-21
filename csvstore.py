#!/usr/bin/env python

#
# Disclaimer
#

import datetime
import ConfigParser
import csv

class Csvstore:
    def __init__(self):
        config = ConfigParser.ConfigParser()
        config.read('datacollector.cfg')     
        self.csvpath = str(config.get('csv', 'path'))
        self.csvfilegranularity = str(config.get('csv', 'file_rotation'))

    ## bikesystem: city bike system, i.e: bicing
    ## stations_data: data in csv space format
    ## stations_detail: data in csv format
    def store_data(self,bikesystem,stations_data,stations_detail):
        ## Compute granularity filename
        csv_file = ''
        if self.csvfilegranularity == 'HOUR':
            csv_file = datetime.datetime.now().strftime("%Y%m%d-%H%M")
        
        # Store data in csv file
        fd = open(self.csvpath+'/'+bikesystem+'_data_'+csv_file+'.csv','a+')
        fd.write(stations_data)
        fd.close()
        
        # Store stations and check for new ones
        