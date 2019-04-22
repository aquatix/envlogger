#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Parts Copyright © 2017 Michał "czesiek" Czyżewski <me@czesiek.net>
# https://github.com/czesiekhaker/aqicn-status
#
# Distributed under terms of the MIT license.

import json
import requests

from .models import AQIObservation

def aqi_readable(aqi):
    if aqi <= 50:    return 'Good'
    elif aqi <= 100: return 'Moderate'
    elif aqi <= 150: return 'Unhealthy for Sensitive Groups'
    elif aqi <= 200: return 'Unhealthy'
    elif aqi <= 300: return 'Very Unhealthy'
    else:            return 'Hazardous'

def aqi_color(aqi):
    if aqi <= 50:    return '#009966'
    elif aqi <= 100: return '#ffdd33'
    elif aqi <= 150: return '#ff9933'
    elif aqi <= 200: return '#cc0033'
    elif aqi <= 300: return '#660099'
    else:            return '#7e0023'

def get_aqi_for_city(config):
    waqi_url = 'https://wind.waqi.info/nsearch/full/{}?n=12'.format(config.city)
    response = requests.get(waqi_url)
    try:
        result = response.json()['results'][0]['s']
    except KeyError:
        # No results found for this location
        return None

    print(result)

    newaqi = AQIObservation(aqiconfig=config)

    newaqi.aqi = int(result['a'])
    newaqi.location_name = result['n'][0]
    newaqi.location_code = result['u']
    newaqi.location_country = result['c']
    newaqi.server_update_time = result['t'][0]
    newaqi.uri = 'http://aqicn.org/city/' + result['u']

    return newaqi
