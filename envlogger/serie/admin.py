# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Serie, Measurement


class SerieAdmin(admin.ModelAdmin):
    list_display = ('label', )
    search_fields = ('label', 'notes', )


class MeasurementAdmin(admin.ModelAdmin):
    list_display = ('serie', 'date', 'value', 'delta', 'delta_per_day', )
    search_fields = ('value', 'notes', )
    list_filter = ('serie', )


admin.site.register(Serie, SerieAdmin)
admin.site.register(Measurement, MeasurementAdmin)
