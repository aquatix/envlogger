# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import decimal

from django.contrib.auth.models import User
from django.db import models


class BaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta(object):
        abstract = True


class Car(BaseModel):
    """Car"""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    label = models.CharField(max_length=200)
    number_plate = models.CharField(max_length=20)
    make = models.CharField(max_length=30, null=True, blank=True)
    model = models.CharField(max_length=30, null=True, blank=True)
    year = models.IntegerField(null=True, blank=True)
    notes = models.CharField(max_length=512, null=True, blank=True)


    def __unicode__(self):
        return self.label

    def __str__(self):
        return self.__unicode__()


class FuelStation(BaseModel):
    """Fuel station"""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    label = models.CharField(max_length=200)
    address = models.CharField(max_length=512, null=True, blank=True)
    notes = models.CharField(max_length=512, null=True, blank=True)

    def __unicode__(self):
        return self.label

    def __str__(self):
        return self.__unicode__()


class Refuelling(BaseModel):
    """Refuelling event"""

    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    station = models.ForeignKey(FuelStation, on_delete=models.CASCADE)
    date = models.DateTimeField()
    litres = models.DecimalField(max_digits=9, decimal_places=3)
    litre_price = models.DecimalField(max_digits=6, decimal_places=3)
    price = models.DecimalField(max_digits=9, decimal_places=2)

    daycounterkm = models.DecimalField(max_digits=9, decimal_places=1)
    totalcounterkm = models.IntegerField()

    notes = models.CharField(max_length=512, null=True, blank=True)

    @property
    def km_per_litre_float(self):
        return self.daycounterkm / self.litres

    @property
    def km_per_litre(self):
        return '{0:.2f}'.format(self.km_per_litre_float)

    @property
    def litre_per_100km_float(self):
        return self.litres / (self.daycounterkm / decimal.Decimal(100.0))

    @property
    def litre_per_100km(self):
        return '{0:.2f}'.format(self.litre_per_100km_float)

    @property
    def price_per_km_float(self):
        return self.price / decimal.Decimal(self.daycounterkm)

    @property
    def price_per_km(self):
        return '{0:.2f}'.format(self.price_per_km_float)


    class Meta:
        ordering = ['-date']


class Default(BaseModel):
    """Default Car and FuelStation for User"""

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    station = models.ForeignKey(FuelStation, on_delete=models.CASCADE)
