# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse

from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404

from .models import WeatherProvider, WeatherConfig

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

    graphs = {}
    for config in weatherconfigs:
        graphs[config.slug] = config.get_dataseries(['temp_c', 'wind_speed_kph', 'humidity'])

    context = {
        'weatherconfigs': weatherconfigs,
        'graphs': graphs,
    }

    print context

    return render(request, 'dashboard.html', context)
