from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^<int:user_id>/dashboard/$', views.seriesdashboard, name='seriesdashboard'),
]
