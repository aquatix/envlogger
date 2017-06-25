# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models

class BaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta(object):
        abstract = True


class FuelStation(BaseModel):
    """Fuel station"""

    user = models.ForeignKey(User)
    label = models.CharField(max_length=200)
    notes = models.CharField(max_length=512)

    def __unicode__(self):
        return self.label


class Refuelling(BaseModel):
    """Refuelling event"""

    station = models.ForeignKey(FuelStation)
    date = models.DateTimeField()
    litres = models.DecimalField(max_digits=9, decimal_places=3)
    litre_price = models.DecimalField(max_digits=6, decimal_places=3)
    price = models.DecimalField(max_digits=9, decimal_places=3)

    daycounterkm = models.DecimalField(max_digits=9, decimal_places=1)
    totalcounterkm = models.IntegerField()

    notes = models.CharField(max_length=512, null=True, blank=True)

    @property
    def km_per_litre(self):
        return self.daycounterkm / self.litres

    @property
    def litre_per_100km(self):
        return self.litres / (self.daycounterkm / 100.0)

    @property
    def price_per_km(self):
        return self.price / self.daycounterkm
