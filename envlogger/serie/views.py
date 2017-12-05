# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404


def index(request):
    return HttpResponse("Please provide a serie ID.")

def seriesdashboard(request, user_id):
    user = get_object_or_404(User, id=user_id)
