#!/usr/bin/env python

#
# Disclaimer
#

import time
import requests
import json
import pymongo
import datetime
import struct
import binascii
#
# Store data to its correspondent MongoDB collection
#
def store_data(bikesystem,jsondata,csvdata):
   # Create a local connection
   conn = pymongo.MongoClient()
   db = conn['bicing']
   collection = db['data']
   db.data.insert(jsondata)

   #  TO DO - Add station details to complementary CSV - MongoDB collection
   #  TO DO - Create complementary CSV to relationate ID - TIMESTAMP - CSV_DATA


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
      json_data = []
      csv_data = []
      now = datetime.datetime.utcnow().replace( second=0, microsecond=0)  

      fd = open('document.csv','ab+')    
      for value in json_content:
	  # Replace API response timestamp value for suitable format to allow date searches within MongoDB
          station_data = { "s":value['id'],"f":value['free'],"b":value['bikes'],"t":now }
          fd.write(struct.pack("<I",value['id']))
          fd.write(struct.pack("<I",value['free']))
          fd.write(struct.pack("<I",value['bikes']))
          fd.write(struct.pack("<L",18000))
#          fd.write(m)
          json_data.append(station_data)
# f.write(struct.pack('H', 0xffff))
#+"," +str(time.mktime(now.timetuple()))+ "\r\n"
          # TO DO - Add station details to complementary CSV - MongoDB collection

      # Call to store response in MongoDB
      fd.close()
      store_data(bikesystem,json_data,csv_data)

class Bikplugin(object):

#    def __init__():

#
# Get all available stations from all countires/cities from citybik.es
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

