#!/usr/bin/env python

#
# Disclaimer
#

import datetime
import ConfigParser
import csv
import difflib

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
            csv_file = datetime.datetime.now().strftime("%Y%m%d-%H")
        elif self.csvfilegranularity == 'DAY':
            csv_file = datetime.datetime.now().strftime("%Y%m%d")
        else: # MONTH
            csv_file = datetime.datetime.now().strftime("%Y%m")
        
        # Store data in csv file
        fd = open(self.csvpath+'/'+bikesystem+'_data_'+csv_file+'.csv','a+')
        fd.write(stations_data)
        fd.close()

        ## TODO - CORRECT STATION STORE ##
        try:
            with open(self.csvpath+'/'+bikesystem+'_station.csv.'+datetime.datetime.now().strftime("%Y%m%d-%H"),'w') as fd:
                # Check if there is any new station
                fd.write(stations_detail)
                fd.close()
                new_fd = open(self.csvpath+'/'+bikesystem+'_station.csv.'+datetime.datetime.now().strftime("%Y%m%d-%H"),'r')
                old_fd = open(self.csvpath+'/'+bikesystem+'_station.csv','r')
                print difflib.Differ(new_fd, old_fd)
                
                
        except IOError:
            print "Arrg"
            fd = open(self.csvpath+'/'+bikesystem+'_station.csv','w')
            fd.write(stations_detail)
            fd.close()
#        # Store stations and check for new ones
#        try:
#            with open(self.csvpath+'/'+bikesystem+'_station.csv') as fd:
#                fd.write(stations_detail)
#                fd.close
#        except IOError:
#            print 'Oh dear.'
        