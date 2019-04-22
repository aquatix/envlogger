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

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    source = models.CharField(max_length=20, choices=SOURCE_OPTIONS, default=SOURCE_OPENWEATHERMAP)
    apikey = models.CharField(max_length=200)
    pro = models.BooleanField(default=False)

    def __unicode__(self):
        #return self.SOURCE_OPTIONS[self.source]
        return self.source

    def __str__(self):
        return self.__unicode__()


class WeatherConfig(BaseModel):
    """Configuration for a specific WeatherProvider, with location and such"""
    provider = models.ForeignKey(WeatherProvider, on_delete=models.CASCADE)
    enabled = models.BooleanField(default=True)

    city = models.CharField(max_length=200, null=True, blank=True)
    country = models.CharField(max_length=200, null=True, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    def get_dataseries(self, fields):
        observations = Observation.objects.filter(weatherconfig=self).order_by('observation_epoch')
        result = []
        for obs in observations:
            data = []
            for field in fields:
                data.append((field, obs.__dict__[field]))
            result.append((obs.observation_epoch, data),)
        return result

    @property
    def slug(self):
        return '{}_{}'.format(self.provider, self.id)

    def __unicode__(self):
        return '{} ({}, {})'.format(self.provider, self.city, self.country)

    def __repr__(self):
        return f'WeatherConfig({self.provider}, {self.city}, {self.country})'

    def __str__(self):
        return self.__unicode__()


class Observation(BaseModel):
    """Observation for a certain location"""
    weatherconfig = models.ForeignKey(WeatherConfig, on_delete=models.CASCADE)

    # Location
    country_iso3166 = models.CharField(max_length=3, null=True, blank=True)
    country_name = models.CharField(max_length=200, null=True, blank=True)
    state = models.CharField(max_length=200, null=True, blank=True)
    city = models.CharField(max_length=200, null=True, blank=True)
    stationid = models.CharField(max_length=200, null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    elevation = models.FloatField(null=True, blank=True)

    # Date and time
    observation_time_rfc822 = models.CharField(max_length=50, null=True, blank=True)
    #observation_epoch = models.BigIntegerField(null=True, blank=True)
    observation_epoch = models.DateTimeField(null=True, blank=True)

    sunrise_time = models.DateTimeField(null=True, blank=True)
    sunset_time = models.DateTimeField(null=True, blank=True)

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

    snow_volume = models.FloatField(null=True, blank=True)
    rain_volume = models.FloatField(null=True, blank=True)

    cloud_coverage = models.IntegerField(null=True, blank=True)
    humidity = models.IntegerField(null=True, blank=True)
    ozone = models.FloatField(null=True, blank=True)  # Dobson units
    uv_index = models.FloatField(null=True, blank=True)
    visibility_mi = models.FloatField(null=True, blank=True)
    visibility_km = models.FloatField(null=True, blank=True)

    wind_deg = models.IntegerField(null=True, blank=True)
    wind_direction = models.CharField(max_length=10, null=True, blank=True)
    wind_speed_mph = models.FloatField(null=True, blank=True)
    wind_speed_kph = models.FloatField(null=True, blank=True)
    wind_gust_mph = models.FloatField(null=True, blank=True)
    wind_gust_kph = models.FloatField(null=True, blank=True)

    description_detailed = models.CharField(max_length=255, null=True, blank=True)
    description_short = models.CharField(max_length=50, null=True, blank=True)
