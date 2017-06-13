# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models

class BaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta(object):
        abstract = True


class TemperatureSerie(BaseModel):
    """Weather provider, like OpenWeatherMap, Darksky.net"""

    user = models.ForeignKey(User)
    label = models.CharField(max_length=200)

    def __unicode__(self):
        return self.label


class Measurement(BaseModel):
    """Measurement of a certain temperature probe"""
    temperatureserie = models.ForeignKey(TemperatureSerie)

    datetime = models.DateTimeField()
    value = models.FloatField()
    note = models.CharField(max_length=255, null=True, blank=True)
