#!/usr/bin/env python

#
# Disclaimer
#

import datetime
import ConfigParser
import shutil
import difflib
import os

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
            # We firstly check if the file X_station.csv already exists
            with open(self.csvpath+'/'+bikesystem+'_station.csv','r') as fd:
                # If the file exists, we compare files to check if there is any new station
                new_fd = open(self.csvpath+'/'+bikesystem+'_station.csv.'+datetime.datetime.now().strftime("%Y%m%d-%H"),'w')
                new_fd.write(stations_detail)
                new_fd.close()
                
                # Iterate through both  reader1 and reader2, compare common row, and append matching column data to test.txt in its matching column
                new = open(self.csvpath+'/'+bikesystem+'_station.csv.'+datetime.datetime.now().strftime("%Y%m%d-%H"),'r')
                old = open(self.csvpath+'/'+bikesystem+'_station.csv','r')
                
                diff = difflib.ndiff(new.readlines(), old.readlines())
                delta = ''.join(x[2:] for x in diff if x.startswith('- '))
                
                old.close()
                new_fd.close()

                
                if delta:
                    # If new stations are found, a new station.csv file is created and moved old one to keep historic data
                    shutil.move(self.csvpath+'/'+bikesystem+'_station.csv', self.csvpath+'/'+bikesystem+'_station.csv.'+datetime.datetime.now().strftime("%Y%m%d-%H%M"))
                    shutil.move(self.csvpath+'/'+bikesystem+'_station.csv.'+datetime.datetime.now().strftime("%Y%m%d-%H"),self.csvpath+'/'+bikesystem+'_station.csv')
                    print "New station added: \r\n"+delta
                else:
                    os.remove(self.csvpath+'/'+bikesystem+'_station.csv.'+datetime.datetime.now().strftime("%Y%m%d-%H"))

        except IOError:
            try:
                print "INFO: File station.csv created"
                # If the file doesn't exist we try to write is straight ahead
                with open(self.csvpath+'/'+bikesystem+'_station.csv','w') as fd:
                    fd.write(stations_detail)
                    fd.close()
            except IOError:
                print "ERROR: Wrong file permissions or path "+self.csvpath+" doesn't exist"
                
        