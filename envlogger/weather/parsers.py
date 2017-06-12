import json
import requests
from .models import Observation

def _process_wunderground_request(url):
    data = requests.get(url).json()
    result = Observation()

    location = data['location']['city']
    temp_c = data['current_observation']['temp_c']
    print "Current temperature in %s is: %s C" % (location, temp_c)

    # Location
    result.country_iso3166 = data['current_observation']['observation_location']['country_iso3166']

    # Weather
    result.temp_c = data['current_observation']['temp_c']
    result.temp_f = data['current_observation']['temp_f']
    return result

def get_wunderground_for_location(apikey, country, city):
    url = 'http://api.wunderground.com/api/{}/geolookup/conditions/q/{}/{}.json'.format(apikey, country, city)
    return _process_wunderground_request(url)

def get_wunderground_for_latlon(apikey, latitude, longitude):
    pass

def get_wunderground_observation(config):
    url = 'http://api.wunderground.com/api/{}/geolookup/conditions/q/{}/{}.json'.format(config.provider.apikey, config.country, config.city)
    data = requests.get(url).json()
    result = Observation(weatherconfig=config)

    location = data['location']['city']
    temp_c = data['current_observation']['temp_c']
    print "Current temperature in %s is: %s C" % (location, temp_c)

    # Location
    result.country_iso3166 = data['current_observation']['observation_location']['country_iso3166']

    # Weather
    result.temp_c = data['current_observation']['temp_c']
    result.temp_f = data['current_observation']['temp_f']
    return result

def get_openweathermap_for_location(apikey, country, city):
    result = Observation()
    return result
