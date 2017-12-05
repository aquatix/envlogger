# -*- coding: utf-8 -*-
from __future__ import unicode_literals

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

    def __unicode__(self):
        return '{} {} {}'.format(self.serie, self.date, self.value)

    def __str__(self):
        return self.__unicode__()

    class Meta:
        ordering = ['-date']
