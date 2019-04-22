from django.contrib.auth.models import User
from django.db import models


def aqi_readable(aqi):
    if aqi <= 50:
        return 'Good'
    if aqi <= 100:
        return 'Moderate'
    if aqi <= 150:
        return 'Unhealthy for Sensitive Groups'
    if aqi <= 200:
        return 'Unhealthy'
    if aqi <= 300:
        return 'Very Unhealthy'
    return 'Hazardous'


def aqi_color(aqi):
    if aqi <= 50:
        return '#009966'
    if aqi <= 100:
        return '#ffdd33'
    if aqi <= 150:
        return '#ff9933'
    if aqi <= 200:
        return '#cc0033'
    if aqi <= 300:
        return '#660099'
    return '#7e0023'


class BaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta():
        abstract = True


class AQIConfig(BaseModel):
    """AQI config, which city"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    city = models.CharField(max_length=200, null=True, blank=True)
    country = models.CharField(max_length=200, null=True, blank=True)

    enabled = models.BooleanField(default=True)

    def __repr__(self):
        return f'AQIConfig({self.city}, {self.country})'

    def __str__(self):
        return f'{self.city}, {self.country}'


class AQIObservation(BaseModel):
    aqiconfig = models.ForeignKey(AQIConfig, on_delete=models.CASCADE)

    aqi = models.IntegerField()
    server_update_time = models.DateTimeField()
    location_name = models.CharField(max_length=255)
    location_code = models.CharField(max_length=255)
    location_country = models.CharField(max_length=20, null=True, blank=True)
    uri = models.CharField(max_length=500, null=True, blank=True)

    def __repr__(self):
        return f'AQIObservation({self.aqi}, {self.server_update_time}, {self.location_name})'

    def __str__(self):
        return f'{self.aqi} ({self.server_update_time}, {self.location_name})'
