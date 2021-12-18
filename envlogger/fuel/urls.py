from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:user_id>/dashboard/', views.fueldashboard, name='fueldashboard'),
]
