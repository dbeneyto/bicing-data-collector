#!/usr/bin/env python

#
# Disclaimer
#

import time
import requests
import json
import datetime
import mongodbstore
import csvstore

#
# Get all data from all stations from a URL
#
def get_city_data(bikesystem,json_content):

        stations_data = []
        stations_detail = []
        csv_data = ""
        csv_station_detail = ""
        now = datetime.datetime.utcnow().replace( second=0, microsecond=0)
        
        for value in json.loads(json_content[1]['data']):
            
            # Replace API response timestamp value for suitable format to allow date searches within MongoDB
            station_data = { "s":int(value['StationID']),"f":int(value['StationFreeSlot']),"b":int(value['StationAvailableBikes']),"t":now }
            station_detail = {"id":int(value['StationID']),"cleaname":value['AddressStreet1'],"name":value['StationName'],"nearby_stations":value['NearbyStationList'],"number":value['AddressNumber'],'location':{ 'lon':float(value['AddressGmapsLongitude']),'lat':float(value['AddressGmapsLatitude'])} }
            csv_data += str(value['StationID'])+" "+str(value['StationFreeSlot'])+" " +str(value['StationAvailableBikes'])+" " +str(time.mktime(now.timetuple()))+ "\r\n"
            csv_station_detail += "#"+str(value['StationID'])+"#"+value['AddressStreet1'].encode('utf-8')+"#" +str(value['NearbyStationList'])+"#" +str(value['AddressNumber'])+"#"+str(value['AddressGmapsLatitude'])+"#"+str(value['AddressGmapsLongitude'])+"\r\n"
            stations_data.append(station_data)
            stations_detail.append(station_detail)

        # Call to store response in MongoDB
        ds = mongodbstore.Mongodbstore()
        ds.store_data(bikesystem, stations_data, stations_detail)

        # Call to store response in CSV
        csvds = csvstore.Csvstore()
        csvds.store_data(bikesystem, csv_data, csv_station_detail)

class Datacollectorplugin():

#
# Get all available stations from all countries/cities from citybik.es
#
    @classmethod
    def get_data(self):
        try:
            response = requests.get('https://www.bicing.cat/es/formmap/getJsonObject')
        except Exception, e:
            print("ERROR: An error occurred performing HTTP request to bicing.cat API")

        if response.status_code == 200:
            json_content = json.loads(response.content)
            get_city_data("bicing",json_content)
