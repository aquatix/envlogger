# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect

from .models import WeatherConfig, WeatherProvider


def index(request):
    return HttpResponse("Please provide a weather ID.")

def weatherdashboard(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if not request.user.is_authenticated:
        return redirect('login')
    elif request.user != user:
        return HttpResponse("Not authorised!")

    weatherproviders = WeatherProvider.objects.filter(user=user)
    weatherconfigs = []
    for provider in weatherproviders:
        weatherconfigs.extend(WeatherConfig.objects.filter(provider=provider))

    colours = ['rgba(153,255,51,0.4)', 'rgba(255,255,0,0.4)', 'rgba(255,153,0,0.4)']
    graphs = []
    for config in weatherconfigs:
        graphs.append([config, config.slug, config.get_dataseries(['temp_c', 'wind_speed_kph', 'humidity'])])

    context = {
        'weatherconfigs': weatherconfigs,
        'colours': colours,
        'graphs': graphs,
    }

    print(context)

    return render(request, 'dashboard.html', context)
