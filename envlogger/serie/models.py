# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import date, datetime, timedelta

from django.contrib.auth.models import User
from django.db import models


class BaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta(object):
        abstract = True


class Serie(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    label = models.CharField(max_length=200)
    notes = models.CharField(max_length=512, null=True, blank=True)

    def __unicode__(self):
        return self.label

    def __str__(self):
        return self.__unicode__()


class Measurement(BaseModel):
    serie = models.ForeignKey(Serie, on_delete=models.CASCADE)

    date = models.DateTimeField()
    value = models.DecimalField(max_digits=9, decimal_places=2)
    notes = models.CharField(max_length=512, null=True, blank=True)

    def get_previous(self):
        previous_measurement = Measurement.objects.filter(serie=self.serie).filter(date__lt=self.date).order_by('-date')[0:1]
        if not previous_measurement:
            return None
        return previous_measurement[0]

    def diff_with_previous(self, previous):
        if not previous:
            return None
        return self.value - previous.value

    @property
    def delta(self):
        """ Delta with previous measurement """
        previous = self.get_previous()
        return self.diff_with_previous(previous)

    @property
    def delta_per_day_float(self):
        """ Delta per day with previous measurement """
        previous = self.get_previous()
        value_diff = self.delta
        dates_diff = self.date - previous.date
        day_diff = timedelta(days=1)
        day_frac = float(dates_diff.total_seconds()) / float(day_diff.total_seconds())
        return value_diff / day_frac

    @property
    def delta_per_day(self):
        result = self.delta_per_day_float
        if not result:
            return None
        return f"{result:.2f}"

    def __unicode__(self):
        return '{} {} {}'.format(self.serie, self.date, self.value)

    def __str__(self):
        return self.__unicode__()

    class Meta:
        ordering = ['-date']
