from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(tipoElemento)
admin.site.register(tipoUnidad)
admin.site.register(inventario)
admin.site.register(cantidad_x_restauracion)
admin.site.register(bitacora_inventario)
admin.site.register(elementos_x_bitacora)
admin.site.register(responsable_alamacen)

