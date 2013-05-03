#!/usr/bin/env python

#       Disclaimer

import requests

class Bikplugin(object):

#    def __init__():

    @classmethod
    def get_data(self):
        try:
            response = requests.get('http://api.citybik.es/networks.json')
        except Exception, e:
            print("An error occurred when collecting data")

        if response.status_code == 200:
            print response.content
