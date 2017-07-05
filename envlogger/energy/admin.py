# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Location, Measurement


class LocationAdmin(admin.ModelAdmin):
    list_display = ('label', )
    search_fields = ('label', 'address', )

class MeasurementAdmin(admin.ModelAdmin):
    list_display = ('date', 'electricity_use_kwh', 'electricity_out_kwh', 'gas_m3', 'water_m3', 'gas_m3_day', 'timediff', 'notes', )
    list_filter = ('location', )

admin.site.register(Location, LocationAdmin)
admin.site.register(Measurement, MeasurementAdmin)
