# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class BaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta(object):
        abstract = True


class WeatherProvider(BaseModel):
    """Weather provider, like OpenWeatherMap, Darksky.net"""

    SOURCE_OPENWEATHERMAP = 'openweathermap'
    SOURCE_DARKSKY = 'darksky'
    SOURCE_WUNDERGROUND = 'wunderground'
    SOURCE_OPTIONS = (
        (SOURCE_OPENWEATHERMAP, 'OpenWeatherMap'),
        (SOURCE_DARKSKY, 'Dark Sky'),
        (SOURCE_WUNDERGROUND, 'Weather Underground'),
    )

    source = models.CharField(max_length=10, choices=SOURCE_OPTIONS, default=SOURCE_OPENWEATHERMAP)
    apikey = models.CharField(max_length=200)


class WeatherConfig(BaseModel):
    """Configuration for a specific WeatherProvider, with location and such"""
    provider = models.ForeignKey(WeatherProvider)

    city = models.CharField(max_length=200, null=True, blank=True)
    country = models.CharField(max_length=200, null=True, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
