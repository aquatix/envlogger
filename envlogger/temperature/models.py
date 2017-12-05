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
    """Serie of measurements, like for a certain location"""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    label = models.CharField(max_length=200)

    def __unicode__(self):
        return self.label

    def __str__(self):
        return self.__unicode__()


class Measurement(BaseModel):
    """Measurement of a certain temperature probe"""
    temperatureserie = models.ForeignKey(TemperatureSerie, on_delete=models.CASCADE)

    datetime = models.DateTimeField()
    value = models.FloatField()
    note = models.CharField(max_length=255, null=True, blank=True)
