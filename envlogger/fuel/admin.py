# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Car, FuelStation, Refuelling, Default


class CarAdmin(admin.ModelAdmin):
    list_display = ('label', )

class FuelStationAdmin(admin.ModelAdmin):
    list_display = ('label', )

class RefuellingAdmin(admin.ModelAdmin):
    list_display = ('date', 'litres', 'km_per_litre', 'price', 'station', 'car', )

class DefaultsAdmin(admin.ModelAdmin):
    list_display = ('user', 'car', 'station', )

admin.site.register(Car, CarAdmin)
admin.site.register(FuelStation, FuelStationAdmin)
admin.site.register(Refuelling, RefuellingAdmin)
admin.site.register(Default, DefaultsAdmin)
