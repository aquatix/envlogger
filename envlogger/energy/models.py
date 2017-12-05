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


class Location(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    label = models.CharField(max_length=200)
    address = models.CharField(max_length=255, null=True, blank=True)
    notes = models.CharField(max_length=512, null=True, blank=True)

    @staticmethod
    def get_first_and_latest_measurements_of_this_year():
        today = datetime.now()
        start_of_year = date(date.today().year, 1, 1)
        latest = Measurement.objects.filter(date__lte=today).order_by('-date')[0:1][0]
        first_of_the_year = Measurement.objects.filter(date__gte=start_of_year).order_by('date')[0:1][0]
        return first_of_the_year, latest

    @property
    def electricity_this_year(self):
        first_of_the_year, latest = self.get_first_and_latest_measurements_of_this_year()
        return latest.electricity_use_kwh - first_of_the_year.electricity_use_kwh

    def __unicode__(self):
        return self.label

    def __str__(self):
        return self.__unicode__()


class Measurement(BaseModel):
    location = models.ForeignKey(Location, on_delete=models.CASCADE)

    date = models.DateTimeField()

    electricity_use_kwh = models.IntegerField()
    electricity_out_kwh = models.IntegerField(null=True, blank=True)
    electricity_generated_kwh = models.DecimalField(max_digits=9, decimal_places=1, null=True, blank=True)
    gas_m3 = models.DecimalField(max_digits=9, decimal_places=3)
    water_m3 = models.DecimalField(max_digits=9, decimal_places=3)

    notes = models.CharField(max_length=512, null=True, blank=True)

    def get_previous(self):
        previous_measurement = Measurement.objects.filter(date__lt=self.date).order_by('-date')[0:1]
        if not previous_measurement:
            return None
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

    def __unicode__(self):
        return '{} {}'.format(self.location, self.date)

    def __str__(self):
        return self.__unicode__()

    class Meta:
        ordering = ['-date']


class Tariff(BaseModel):
    """Prices for energy, for a given period of time"""
    location = models.ForeignKey(Location, on_delete=models.CASCADE)

    start_date = models.DateField()
    end_date = models.DateField()

    electricity = models.DecimalField(max_digits=9, decimal_places=4)
    gas = models.DecimalField(max_digits=9, decimal_places=4)
    water = models.DecimalField(max_digits=9, decimal_places=4)
