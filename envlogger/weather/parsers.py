import json
import requests
from .models import Observation
from pyowm import OWM

def get_wunderground_observation(config):
    """Weather Underground observation for current weather in location specified in config"""
    url = 'http://api.wunderground.com/api/{}/geolookup/conditions/q/{}/{}.json'.format(config.provider.apikey, config.country, config.city)
    data = requests.get(url).json()
    w = data['current_observation']

    result = Observation(weatherconfig=config)

    location = data['location']['city']
    temp_c = w['temp_c']
    print "Current temperature in %s is: %s C" % (location, temp_c)

    # Location
    result.country_iso3166 = w['observation_location']['country_iso3166']

    # Weather
    result.temp_c = w['temp_c']
    result.temp_f = w['temp_f']

    result.feelslike_c = w['feelslike_c']
    result.feelslike_f = w['feelslike_f']
    if w['windchill_c'] != 'NA':
        result.windchill_c = w['windchill_c']
    if w['windchill_f'] != 'NA':
        result.windchill_f = w['windchill_f']

    result.pressure_in = w['pressure_in']
    result.pressure_mb = w['pressure_mb']

    #result.cloud_coverage = w['']
    humidity = w['relative_humidity']
    result.humidity = int(humidity[:-1])
    result.uv_index = w['UV']
    result.visibility_km = w['visibility_km']
    result.visibility_mi = w['visibility_mi']

    result.wind_deg = w['wind_degrees']
    result.wind_direction = w['wind_dir']
    result.wind_speed_kph = w['wind_kph']
    result.wind_speed_mph = w['wind_mph']
    result.wind_gust_kph = w['wind_gust_kph']
    result.wind_gust_mph = w['wind_gust_mph']

    result.description_detailed = w['weather']
    result.description_short = w['icon']
    return result

def get_openweathermap_observation(config):
    """OpenWeatherMap observation for current weather in location specified in config"""
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


    result.pressure_mb = w.get_pressure()['press']

    result.cloud_coverage = w.get_clouds()
    result.humidity = w.get_humidity()
    #result.uv_index = w.
    result.visibility_km = w.get_visibility_distance()

    result.wind_deg = w.get_wind()['deg']
    result.wind_speed_kph = w.get_wind()['speed']

    result.weather_description = w.get_detailed_status()
    result.weather_short = w.get_status()

    return result
