# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import FuelStation, Refuelling


class FuelStationAdmin(admin.ModelAdmin):
    list_display = ('label', )

class RefuellingAdmin(admin.ModelAdmin):
    list_display = ('date', 'litres', 'km_per_litre', 'price', 'station', )

admin.site.register(FuelStation, FuelStationAdmin)
admin.site.register(Refuelling, RefuellingAdmin)
