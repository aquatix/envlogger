# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
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

    user = models.ForeignKey(User)
    source = models.CharField(max_length=20, choices=SOURCE_OPTIONS, default=SOURCE_OPENWEATHERMAP)
    apikey = models.CharField(max_length=200)
    pro = models.BooleanField(default=False)

    def __unicode__(self):
        #return self.SOURCE_OPTIONS[self.source]
        return self.source


class WeatherConfig(BaseModel):
    """Configuration for a specific WeatherProvider, with location and such"""
    provider = models.ForeignKey(WeatherProvider)
    enabled = models.BooleanField(default=True)

    city = models.CharField(max_length=200, null=True, blank=True)
    country = models.CharField(max_length=200, null=True, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    def __unicode__(self):
        return '{} ({}, {})'.format(self.provider, self.city, self.country)


class Observation(BaseModel):
    """Observation for a certain location"""
    weatherconfig = models.ForeignKey(WeatherConfig)

    # Location
    country_iso3166 = models.CharField(max_length=3, null=True, blank=True)
    country_name = models.CharField(max_length=200, null=True, blank=True)
    state = models.CharField(max_length=200, null=True, blank=True)
    city = models.CharField(max_length=200, null=True, blank=True)

    # Date and time
    observation_time_rfc822 = models.CharField(max_length=50, null=True, blank=True)
    observation_epoch = models.BigIntegerField(null=True, blank=True)

    sunrise_time = models.BigIntegerField(null=True, blank=True)
    sunset_time = models.BigIntegerField(null=True, blank=True)

    # Weather
    temp_c = models.FloatField(default=0.0, null=True, blank=True)
    temp_f = models.FloatField(default=0.0, null=True, blank=True)
    feelslike_c = models.FloatField(default=0.0, null=True, blank=True)
    feelslike_f = models.FloatField(default=0.0, null=True, blank=True)
    windchill_c = models.FloatField(default=0.0, null=True, blank=True)
    windchill_f = models.FloatField(default=0.0, null=True, blank=True)

    pressure_mb = models.FloatField(null=True, blank=True)
    pressure_in = models.FloatField(null=True, blank=True)
    pressure_trend = models.CharField(max_length=1, null=True, blank=True)  # + or -
    dewpoint_c = models.FloatField(null=True, blank=True)
    dewpoint_f = models.FloatField(null=True, blank=True)

    cloud_coverage = models.IntegerField(null=True, blank=True)
    humidity = models.IntegerField(null=True, blank=True)
    uv_index = models.IntegerField(null=True, blank=True)
    visibility_mi = models.FloatField(null=True, blank=True)
    visibility_km = models.FloatField(null=True, blank=True)

    wind_deg = models.IntegerField(null=True, blank=True)
    wind_speed_mph = models.FloatField(null=True, blank=True)
    wind_speed_kph = models.FloatField(null=True, blank=True)
    wind_gust_mph = models.FloatField(null=True, blank=True)
    wind_gust_kph = models.FloatField(null=True, blank=True)

    description_detailed = models.CharField(max_length=255, null=True, blank=True)
    description_short = models.CharField(max_length=50, null=True, blank=True)