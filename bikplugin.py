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
def get_city_data(url,bikesystem):
    try:
        response = requests.get(url)
    except Exception, e:
        print("An error occurred when collecting data")

    if response.status_code == 200:
        json_content = json.loads(response.content)
        stations_data = []
        stations_detail = []
        csv_data = ""
        csv_station_detail = ""
        now = datetime.datetime.utcnow().replace( second=0, microsecond=0)

        for value in json_content:
            # Replace API response timestamp value for suitable format to allow date searches within MongoDB
            station_data = { "s":value['id'],"f":value['free'],"b":value['bikes'],"t":now }
            station_detail = {"id":value['id'],"cleaname":value['cleaname'],"name":value['name'],"nearby_stations":value['nearby_stations'],"number":value['number'],"lat":value['lat'],"lng":value['lng'] }
            csv_data += str(value['id'])+" "+str(value['free'])+" " +str(value['bikes'])+" " +str(time.mktime(now.timetuple()))+ "\r\n"
            csv_station_detail += "#"+str(value['id'])+"#"+value['cleaname'].encode('utf-8')+"#" +str(value['nearby_stations'])+"#" +str(value['number'])+"#"+str(value['lat'])+"#"+str(value['lng'])+"\r\n"
            stations_data.append(station_data)
            stations_detail.append(station_detail)
            # TO DO - Add station details to complementary CSV - MongoDB collection

        # Call to store response in MongoDB
        ds = mongodbstore.Mongodbstore()
        ds.store_data(bikesystem, stations_data, stations_detail)

        # Call to store response in CSV
        csvds = csvstore.Csvstore()
        csvds.store_data(bikesystem, csv_data, csv_station_detail)

class Bikplugin():

#
# Get all available stations from all countries/cities from citybik.es
#
    @classmethod
    def get_data(self):
        try:
            response = requests.get('http://api.citybik.es/networks.json')
        except Exception, e:
            print("An error occurred when collecting data")

        if response.status_code == 200:
            json_content = json.loads(response.content)
            for value in json_content:
                city_url = value['url']
                if city_url == 'http://api.citybik.es/bicing.json':
                    get_city_data(city_url,value['name'])
