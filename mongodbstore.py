#!/usr/bin/env python

#
# Disclaimer
#

import ConfigParser
from pymongo import Connection

class Mongodbstore:
    def __init__(self):
        config = ConfigParser.ConfigParser()
        config.read('datacollector.cfg')     
        self.mongodbip = str(config.get('mongodb', 'ip'))
        self.mongodbport = int(config.get('mongodb', 'port'))
        self.mongodbuser = str(config.get('mongodb', 'user'))
        self.mongodbpass = str(config.get('mongodb', 'pass'))

    ## bikesystem: city bike system, i.e: bicing
    ## stations_data: data in json format
    ## stations_detail: data in json format
    def store_data(self,bikesystem,stations_data,stations_detail):
        connection = Connection(self.mongodbip,self.mongodbport)
        db = connection[bikesystem]
        # Collection to store crawled data is "data"
        db['data']
        db.data.insert(stations_data)
        
        # Collection to store station information is "station"
        collection = db['station']

        # Check if there is any new station
        for value in stations_detail:
            # Search in the collection for the station id, if no entries are returned we add the station to db
            cursor = collection.find({"id" : value['id']})
            if cursor.count() == 0:
                collection.insert(value)
                print ("NEW Station found, added to stations collection\n\r"+str(value))
