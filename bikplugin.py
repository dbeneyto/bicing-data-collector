#!/usr/bin/env python

#
# Disclaimer
#

import requests
import json
import pymongo
import datetime
from pymongo import Connection

#
# Store data to its correspondent MongoDB collection
#
def store_data(bikesystem,jsondata):
   # Create a local connection
   conn = Connection()
   db = conn['bicing']
   collection = db['data']
   db.data.insert(jsondata)

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
      for value in json_content:
	  # Replace API response timestamp value for suitable format to allow date searches within MongoDB
	  value['timestamp'] = datetime.datetime.utcnow()
	  store_data(bikesystem,value)

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

