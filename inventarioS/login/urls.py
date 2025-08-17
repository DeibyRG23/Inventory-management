from django.urls import path
from .views import *

urlpatterns=[
    path('',inicio_sesion,name="home"),
    path('logout',cerrar_sesion,name="cerrar_sesion"),
]