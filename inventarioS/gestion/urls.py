from django.urls import path
from .views import *

urlpatterns = [
    path("novedades", novedades, name="novedades"),
    path("novedades/agregar_responsable", responsable, name="agregarResponsable"),
    path("inventario", inventarioTotal, name="inventario"),
    path("inventario/excel", excel_inventario, name="exportar_inventario"),
    path("inventario/agregar_elemento", agregarelemento, name="agregar_elemento"),
    path("inventario/agregar_unidad", agregarunidad, name="agregar_unidad"),
    path("inventario/agregar_inventario", agregarinventario, name="agregar_inventario"),
    path("inventario/editaritem/<int:id>/", editarinventario, name="editar_inventario"),
    path(
        "inventario/eliminaritem/<int:id>/",
        eliminarinventario,
        name="eliminar_inventario",
    ),
    path("filtrar_elemento/", tipo_elemento, name="dato"),
    path("filtrar_elemento/<int:id>", filtrar_elemento, name="filtrar_inventario"),
    path("bitacora", bitacora, name="bitacora"),
    path("bitacora/excel", excel_bitacora, name="exportar_bitacora"),
    path("bitacora/eliminar/<int:id>", eliminar_bitacora, name="eliminarbitacora"),
    path("bitacora/reporteingresos", reporte_ingresos, name="ingresos"),
    path("bitacora/reporteingresos/agregar", agregar_ingreso, name="guardar_ingreso"),
    path("bitacora/reportesalidas", reporte_salidas, name="salidas"),
    path("bitacora/reportesalidas/agregar", agregar_salida, name="guardar_salida"),
    path("bitacora/reportepaz_y_salvo/", reporte_paz_y_salvo, name="pazysalvo"),
    path(
        "bitacora/reportepaz_y_salvo/agregar",
        agregar_pazysalvo,
        name="guardar_pazysalvo",
    ),
    path("bitacora/reportefallas/", reporte_falla, name="falla"),
    path("bitacora/reportefallas/agregar", agregar_falla, name="guardar_falla"),
    path("cantidadxrestauracion", cantidadxrestauracion, name="cantidadxrestauracion"),
    path(
        "cantidadxrestauracion/agregar",
        agregar_cantxrest,
        name="agregar_cantidadxrestauracion",
    ),
    path("filtrar_disponible/", dato, name="dato_disponible"),
    path("filtrar_disponible/<int:id>", filtrar_disponible, name="filtrar_utilidad"),
    path(
        "cantidadxrestauracion/editar/<int:id>", editar_cantidad, name="editar_cantidad"
    ),
    path(
        "cantidadxrestauracion/eliminar/<int:id>",
        eliminar_cantidad,
        name="eliminar_cantidad",
    ),
]
