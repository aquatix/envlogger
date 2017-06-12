# encoding: utf-8

from __future__ import absolute_import

import logging
from .models import WeatherProvider, WeatherConfig, Observation
from .parsers import (
    get_openweathermap_observation,
    get_wunderground_observation,
)


def get_observation_for_config(config):
    """Fetch current weather data for config"""
    if config.provider.source == WeatherProvider.SOURCE_OPENWEATHERMAP:
        result = get_openweathermap_observation(config)
    elif config.provider.source == WeatherProvider.SOURCE_WUNDERGROUND:
        result = get_wunderground_observation(config)

    print(result.__dict__)
    result.save()

def update_everything():
    configs = WeatherConfig.objects.filter(enabled=True)

    for config in configs:
        get_observation_for_config(config)
