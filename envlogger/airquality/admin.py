from django.contrib import admin

from .models import AQIConfig, AQIObservation


class AQIConfigAdmin(admin.ModelAdmin):
    list_display = ('city', 'country', 'enabled', )
    list_filter = ('city', )


class AQIObservationAdmin(admin.ModelAdmin):
    list_display = ('server_update_time', 'aqi', 'readable_value', 'location_name', )
    list_filter = ('location_name', 'location_code', )


admin.site.register(AQIConfig, AQIConfigAdmin)
admin.site.register(AQIObservation, AQIObservationAdmin)
