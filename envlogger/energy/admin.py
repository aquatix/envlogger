# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Location, Tariff, Measurement


class LocationAdmin(admin.ModelAdmin):
    list_display = ('label', 'electricity_this_year', )
    search_fields = ('label', 'address', )


class TariffAdmin(admin.ModelAdmin):
    list_display = ('location', 'start_date', 'end_date', 'electricity', 'gas', 'water',)


class MeasurementAdmin(admin.ModelAdmin):
    list_display = ('date', 'electricity_use_kwh', 'electricity_use_day', 'electricity_out_kwh', 'electricity_out_day', 'electricity_generated_kwh', 'gas_m3', 'gas_m3_day', 'water_m3', 'water_m3_day', 'timediff', 'notes', )
    list_filter = ('location', )

admin.site.register(Location, LocationAdmin)
admin.site.register(Tariff, TariffAdmin)
admin.site.register(Measurement, MeasurementAdmin)
