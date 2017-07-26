# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import decimal
from django.contrib.auth.models import User
from django.db import models

from datetime import timedelta


class BaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta(object):
        abstract = True


class Location(BaseModel):
    user = models.ForeignKey(User)
    label = models.CharField(max_length=200)
    address = models.CharField(max_length=255, null=True, blank=True)
    notes = models.CharField(max_length=512, null=True, blank=True)

    def __unicode__(self):
        return self.label


class Measurement(BaseModel):
    location = models.ForeignKey(Location)

    date = models.DateTimeField()

    electricity_use_kwh = models.IntegerField()
    electricity_out_kwh = models.IntegerField(null=True, blank=True)
    electricity_generated_kwh = models.IntegerField(null=True, blank=True)
    gas_m3 = models.DecimalField(max_digits=9, decimal_places=3)
    water_m3 = models.DecimalField(max_digits=9, decimal_places=3)

    notes = models.CharField(max_length=512, null=True, blank=True)

    def get_previous(self):
        previous_measurement = Measurement.objects.filter(date__lt=self.date).order_by('-date')[0:1]
        if not previous_measurement:
            return None
        else:
            return previous_measurement[0]

    def diff_with_previous(self, previous):
        if not previous:
            return None
        return self.date - previous.date

    @property
    def timediff(self):
        previous = self.get_previous()
        return self.diff_with_previous(previous)

    @property
    def electricity_use_day_float(self):
        previous = self.get_previous()
        if not previous:
            return None
        diff = self.diff_with_previous(previous)
        day_diff = timedelta(days=1)
        day_frac = float(diff.total_seconds()) / float(day_diff.total_seconds())
        electricity_diff = float(self.electricity_use_kwh - previous.electricity_use_kwh)
        return electricity_diff / day_frac

    @property
    def electricity_use_day(self):
        result = self.electricity_use_day_float
        if not result:
            return None
        return '{0:.2f}'.format(result)

    @property
    def electricity_out_day_float(self):
        previous = self.get_previous()
        if not previous:
            return None
        diff = self.diff_with_previous(previous)
        day_diff = timedelta(days=1)
        day_frac = float(diff.total_seconds()) / float(day_diff.total_seconds())
        if self.electricity_out_kwh and previous.electricity_out_kwh:
            electricity_diff = float(self.electricity_out_kwh - previous.electricity_out_kwh)
            return electricity_diff / day_frac
        else:
            return None

    @property
    def electricity_out_day(self):
        result = self.electricity_out_day_float
        if not result:
            return None
        return '{0:.2f}'.format(result)

    @property
    def gas_m3_day_float(self):
        previous = self.get_previous()
        if not previous:
            return None
        diff = self.diff_with_previous(previous)
        day_diff = timedelta(days=1)
        day_frac = float(diff.total_seconds()) / float(day_diff.total_seconds())
        gas_m3_diff = float(self.gas_m3 - previous.gas_m3)
        return gas_m3_diff / day_frac

    @property
    def gas_m3_day(self):
        result = self.gas_m3_day_float
        if not result:
            return None
        return '{0:.2f}'.format(result)

    @property
    def water_m3_day_float(self):
        previous = self.get_previous()
        if not previous:
            return None
        diff = self.diff_with_previous(previous)
        day_diff = timedelta(days=1)
        day_frac = float(diff.total_seconds()) / float(day_diff.total_seconds())
        water_m3_diff = float(self.water_m3 - previous.water_m3)
        return water_m3_diff / day_frac

    @property
    def water_m3_day(self):
        result = self.water_m3_day_float
        if not result:
            return None
        return '{0:.2f}'.format(result)

    class Meta:
        ordering = ['-date']
