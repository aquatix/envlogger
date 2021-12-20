# Parts Copyright © 2017 Michał "czesiek" Czyżewski <me@czesiek.net>
# https://github.com/czesiekhaker/aqicn-status
#
# Distributed under terms of the MIT license.
from datetime import datetime, timezone

import requests

from .models import AQIObservation


def get_aqi_for_city(config):
    waqi_url = 'https://wind.waqi.info/nsearch/full/{}?n=12'.format(config.city)
    response = requests.get(waqi_url)
    try:
        result = response.json()['results'][0]['s']
    except KeyError:
        # No results found for this location
        return None

    newaqi = AQIObservation(aqiconfig=config)

    newaqi.aqi = int(result['a'])
    newaqi.location_name = result['n'][0]
    newaqi.location_code = result['u']
    try:
        newaqi.location_country = result['c']
    except KeyError:
        pass
    newaqi.server_update_time = datetime.strptime(f"{result['t'][0]}{result['t'][1]}", '%Y-%m-%d %H:%M:%S%z').replace(tzinfo=timezone.utc)
    newaqi.uri = 'https://aqicn.org/city/' + result['u']

    return newaqi
