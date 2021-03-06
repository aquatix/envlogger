# encoding: utf-8

from __future__ import absolute_import

import logging
import traceback

from .models import Observation, WeatherConfig, WeatherProvider
from .parsers import (get_darksky_observation, get_openweathermap_observation,
                      get_wunderground_observation)


def get_observation_for_config(config):
    """Fetch current weather data for config"""
    if config.provider.source == WeatherProvider.SOURCE_OPENWEATHERMAP:
        result = get_openweathermap_observation(config)
    elif config.provider.source == WeatherProvider.SOURCE_WUNDERGROUND:
        result = get_wunderground_observation(config)
    elif config.provider.source == WeatherProvider.SOURCE_DARKSKY:
        result = get_darksky_observation(config)

    if result:
        #print(result.__dict__)
        try:
            result.save()
        except ValueError:
            print(result.__dict__)
            traceback.print_exc()

def update_everything():
    configs = WeatherConfig.objects.filter(enabled=True)

    for config in configs:
        get_observation_for_config(config)
