import traceback

from .models import AQIConfig
from .parsers import get_aqi_for_city


def get_observation_for_config(config):
    """Fetch current air quality data for config"""
    result = get_aqi_for_city(config)

    if result:
        try:
            result.save()
        except ValueError:
            print(result.__dict__)
            traceback.print_exc()

def update_airquality():
    configs = AQIConfig.objects.filter(enabled=True)

    for config in configs:
        get_observation_for_config(config)
