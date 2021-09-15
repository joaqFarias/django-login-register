from django.urls import path
from . import views

urlpatterns = [
    path('', views.root),
    path('index', views.index),
    path('registro', views.registro),
    path('login', views.login),
    path('exito', views.exito),
    path('salir', views.salir)
]
