#!/usr/bin/env python

#       Disclaimer

import requests
import json


def get_city_data(url):
   try:
      response = requests.get(url)
   except Exception, e:
      print("An error occurred when collecting data")

   if response.status_code == 200:
      json_content = json.loads(response.content)
#      print response.content
      for value in json_content:
#	  print value
          print value['name']

class Bikplugin(object):

#    def __init__():

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
#		print city_url
		if city_url == 'http://api.citybik.es/bicing.json':
	           get_city_data(city_url)

                   
#       	     if type(value) == type(['']):
#            	for sub_value in value:
#                	strg = str(json.dumps(sub_value))
#                	format_main_response(strg)
#        	else:
#            	print value
#            print response.content
