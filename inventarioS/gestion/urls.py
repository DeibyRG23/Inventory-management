from django.urls import path
from .views import *

urlpatterns = [
    path("novedades", novedades, name="novedades"),
    path("inventario", inventarioTotal, name="inventario"),
    path("inventario/agregar_elemento", agregarelemento, name="agregar_elemento"),
    path("inventario/agregar_unidad", agregarunidad, name="agregar_unidad"),
    path("inventario/agregar_inventario", agregarinventario, name="agregar_inventario"),
    path("bitacora", bitacora, name="bitacora"),
    path("cantidadxrestauracion", cantidadxrestauracion, name="cantidadxrestauracion"),
    path("cantidadxrestauracion/agregar", agregar_cantxrest, name="agregar_cantidadxrestauracion"),
]
