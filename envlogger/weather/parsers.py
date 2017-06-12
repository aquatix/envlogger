import json
import requests
from .models import Observation
from pyowm import OWM

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

    result.feelslike_c = data['current_observation']['feelslike_c']
    result.feelslike_f = data['current_observation']['feelslike_f']
    if data['current_observation']['windchill_c'] != 'NA':
        result.windchill_c = data['current_observation']['windchill_c']
    if data['current_observation']['windchill_f'] != 'NA':
        result.windchill_f = data['current_observation']['windchill_f']

    result.pressure_in = data['current_observation']['pressure_in']

    #result.cloud_coverage = data['current_observation']['']
    result.visibility_km = data['current_observation']['visibility_km']
    result.visibility_mi = data['current_observation']['visibility_mi']
    result.uv_index = data['current_observation']['UV']

    result.description_detailed = data['current_observation']['weather']
    return result

def get_openweathermap_observation(config):
    result = Observation(weatherconfig=config)
    if config.provider.pro:
        owm = OWM(config.provider.apikey, subscription_type='pro')
    else:
        owm = OWM(config.provider.apikey)

    obs = owm.weather_at_place('{},{}'.format(config.city, config.country))
    w = obs.get_weather()

    result.temp_c = w.get_temperature(unit='celsius')['temp']
    result.temp_f = w.get_temperature(unit='fahrenheit')['temp']


    #temps = w.get_temperature()


    #w.get_rain()
    #w.get_snow()

    result.sunrise_time = w.get_sunrise_time()


    result.cloud_coverage = w.get_clouds()


    result.weather_short = w.get_status()
    result.weather_description = w.get_detailed_status()

    return result
