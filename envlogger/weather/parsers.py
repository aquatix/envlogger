import json
import requests
from .models import Observation
from .utils import unix_to_python
import forecastio
from pyowm import OWM
from pyowm.exceptions.api_call_error import APICallError as OWMAPICallError
from pytz import UTC

def get_wunderground_observation(config):
    """Weather Underground observation for current weather in location specified in config"""
    url = 'http://api.wunderground.com/api/{}/geolookup/conditions/q/{}/{}.json'.format(config.provider.apikey, config.country, config.city)
    data = requests.get(url).json()
    w = data['current_observation']

    result = Observation(weatherconfig=config)

    location = data['location']['city']
    temp_c = w['temp_c']

    # Location
    result.country_iso3166 = w['observation_location']['country_iso3166']
    result.country_name = data['location']['country_name']
    result.state = w['observation_location']['state']
    result.city = w['observation_location']['city']
    result.stationid = w['station_id']
    try:
        result.latitude = float(w['display_location']['latitude'])
    except:
        pass
    try:
        result.longitude = float(w['display_location']['longitude'])
    except:
        pass
    try:
        result.elevation = float(w['display_location']['elevation'])
    except:
        pass

    # Date and time
    result.observation_time_rfc822 = w['observation_time_rfc822']
    result.observation_epoch = unix_to_python(w['observation_epoch'])

    #result.sunrise_time
    #result.sunset_time

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

    result.pressure_trend = w['pressure_trend']
    result.dewpoint_c = w['dewpoint_c']
    result.dewpoint_f = w['dewpoint_f']

    try:
        result.rain_volume = float(w['precip_1hr_metric'])
    except:
        pass
    #result.snow_volume

    #result.cloud_coverage = w['']
    humidity = w['relative_humidity']
    result.humidity = int(humidity[:-1])
    #result.ozone
    result.uv_index = w['UV']
    if w['visibility_km'] != 'N/A':
        result.visibility_km = w['visibility_km']
    if w['visibility_mi'] != 'N/A':
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

    try:
        obs = owm.weather_at_place('{},{}'.format(config.city, config.country))
    except TypeError:
        print('Something went wrong while fetching OpenWeatherMap forecast for {}, {}'.format(config.city, config.country))
        return None
    except OWMAPICallError as e:
        print('APICallError while fetching OpenWeatherMap forecast for {}, {}'.format(config.city, config.country))
        return None
    w = obs.get_weather()

    result.country_iso3166
    result.country_name
    result.state
    result.city
    result.stationid
    result.latitude
    result.longitude
    result.elevation

    #result.observation_time_rfc822 = unix_to_python(w.get_reference_time())
    result.observation_epoch = unix_to_python(w.get_reference_time())

    result.sunrise_time = unix_to_python(w.get_sunrise_time())
    result.sunset_time = unix_to_python(w.get_sunset_time())

    result.temp_c = w.get_temperature(unit='celsius')['temp']
    result.temp_f = w.get_temperature(unit='fahrenheit')['temp']

    result.feelslike_c
    result.feelslike_f
    result.windchill_c
    result.windchill_f

    result.pressure_mb = w.get_pressure()['press']
    #result.pressure_in = w.get_pressure()['press']
    result.pressure_trend
    result.dewpoint_c
    result.dewpoint_f

    try:
        result.rain_volume = w.get_rain()['3h']
    except:
        pass
    try:
        result.snow_volume = w.get_snow()['3h']
    except:
        pass

    result.cloud_coverage = w.get_clouds()
    result.humidity = w.get_humidity()
    #result.ozone
    #result.uv_index = w.
    result.visibility_mi
    result.visibility_km = w.get_visibility_distance()

    try:
        result.wind_deg = w.get_wind()['deg']
    except:
        pass
    result.wind_direction
    result.wind_speed_mph
    result.wind_speed_kph = w.get_wind()['speed']
    result.wind_gust_mph
    result.wind_gust_kph

    result.weather_description = w.get_detailed_status()
    result.weather_short = w.get_status()

    return result

def get_darksky_observation(config):
    """DarkSky.net observation for current weather in location specified in config"""
    result = Observation(weatherconfig=config)
    forecast = forecastio.load_forecast(config.provider.apikey, config.latitude, config.longitude)

    w = forecast.currently()
    daily = forecast.daily()

    result.country_iso3166
    result.country_name
    result.state
    result.city
    result.stationid
    result.latitude
    result.longitude
    result.elevation

    result.observation_time_rfc822
    result.observation_epoch = w.time.replace(tzinfo=UTC)

    try:
        result.sunrise_time = unix_to_python(daily.sunriseTime)
        result.sunset_time = unix_to_python(daily.sunsetTime)
    except:
        pass

    result.temp_c = w.temperature
    #result.temp_f = w.get_temperature(unit='fahrenheit')['temp']

    result.feelslike_c = w.apparentTemperature
    #result.feelslike_f
    result.windchill_c
    result.windchill_f

    result.pressure_mb = w.pressure
    #result.pressure_in = w.get_pressure()['press']
    result.pressure_trend
    result.dewpoint_c = w.dewPoint
    result.dewpoint_f

    result.rain_volume
    result.snow_volume

    result.cloud_coverage = w.cloudCover * 100.0
    result.humidity = w.humidity * 100.0
    result.ozone = w.ozone
    #result.uv_index = w.
    try:
        result.visibility_mi = w.visibility
        result.visibility_km = w.visibility
    except:
        pass

    result.wind_deg = w.windBearing
    result.wind_direction
    result.wind_speed_mph
    result.wind_speed_kph = w.windSpeed
    result.wind_gust_mph
    result.wind_gust_kph

    result.weather_description = w.summary
    result.weather_short = w.icon

    return result
