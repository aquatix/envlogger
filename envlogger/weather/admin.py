# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import WeatherProvider, WeatherConfig, Observation


class WeatherProviderAdmin(admin.ModelAdmin):
    list_display = ('source', )

class WeatherConfigAdmin(admin.ModelAdmin):
    list_display = ('provider', 'city', 'country', 'latitude', 'longitude', 'enabled', )

class ObservationAdmin(admin.ModelAdmin):
    list_display = ('weatherconfig', 'created', 'city', 'temp_c', )
    search_list = ('weatherconfig', 'country_iso3166', 'country_name', 'state', 'city', 'description_detailed', 'description_short', )
    list_filter = ('weatherconfig', 'city', )

admin.site.register(WeatherProvider, WeatherProviderAdmin)
admin.site.register(WeatherConfig, WeatherConfigAdmin)
admin.site.register(Observation, ObservationAdmin)
