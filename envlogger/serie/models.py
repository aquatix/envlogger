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

    def __unicode__(self):
        return '{} {} {}'.format(self.serie, self.date, self.value)

    def __str__(self):
        return self.__unicode__()

    class Meta:
        ordering = ['-date']
