import json
import requests

def get_wunderground_for_location(apikey, country, city):
    url = 'http://api.wunderground.com/api/{}/geolookup/conditions/q/{}/{}.json'.format(apikey, country, city)
    data = requests.get(url).json()
    location = data['location']['city']
    temp_c = data['current_observation']['temp_c']
    print "Current temperature in %s is: %s C" % (location, temp_c)

def get_wunderground_for_latlon(apikey, latitude, longitude):
    pass
