from django.urls import path

from . import views

urlpatterns = [
    path(r'^$', views.index, name='index'),
    path(r'^<int:user_id>/dashboard/$', views.fueldashboard, name='fueldashboard'),
]
