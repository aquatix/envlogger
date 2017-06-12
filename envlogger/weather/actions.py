# encoding: utf-8

from __future__ import absolute_import

import logging
from .models import WeatherProvider, WeatherConfig, Observation
from .parsers import (
    get_openweathermap_for_location,
    get_wunderground_observation,
)


def get_observation_for_config(config):
    """Fetch current weather data for config"""
    if config.provider.source == WeatherProvider.SOURCE_OPENWEATHERMAP:
        result = get_openweathermap_for_location(config.provider.apikey, config.country, config.city)
    elif config.provider.source == WeatherProvider.SOURCE_WUNDERGROUND:
        #result = get_wunderground_for_location(config.provider.apikey, config.country, config.city)
        result = get_wunderground_observation(config)

    result.save()

def update_everything():
    configs = WeatherConfig.objects.filter(enabled=True)

    for config in configs:
        get_observation_for_config(config)
