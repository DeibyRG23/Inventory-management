from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.decorators import login_required
from gestion.models import *
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from openpyxl import Workbook

# Create your views here.
@login_required
def novedades(request):
    necesario=cantidad_x_restauracion.objects.filter(disponible=False)
    personal={}
    if responsable_alamacen.objects.exists():
        personal=responsable_alamacen.objects.last()
    return render(request,"novedades/novedades.html",{"personal":personal,"necesario":necesario})


@login_required
def responsable(request):
    if request.method == "POST":
        nombre = request.POST.get("nombre")
        cargo = request.POST.get("cargo")
        contacto = request.POST.get("contacto")

        personal_responsable = responsable_alamacen(
            nombre_responsable=nombre,
            cargo=cargo,
            contacto=contacto,
        )

        personal_responsable.save()
        messages.success(request, "Responsable guardado correctamente")
    return render(request, "novedades/responsable.html")


@login_required
def inventarioTotal(request):
    elementos=inventario.objects.all()
    ids_tipos_elemento = inventario.objects.exclude(tipo__isnull=True).values_list('tipo', flat=True).distinct()
    items = tipoElemento.objects.filter(id__in=ids_tipos_elemento)
    return render(request, "inventario/inventario.html",{"elementos":elementos,"items":items})

@login_required
def agregarinventario(request):
    elementos=tipoElemento.objects.all()
    unidades=tipoUnidad.objects.all()
    if request.method=="POST":
        elementotipo=request.POST.get("elementotipo")
        elemento=request.POST.get("elemento")
        cantidad=request.POST.get("cantidad")
        tipo=request.POST.get("tipo")
        marca=request.POST.get("marca")
        observacion=request.POST.get("observacion")

        elementoInventario=inventario(
            tipo=tipoElemento.objects.get(id=elementotipo),
            elemento=elemento,
            cantidad=cantidad,
            unidad=tipoUnidad.objects.get(id=tipo),
            marca=marca,
            observaciones=observacion
        )

        elementoInventario.save()
        messages.success(request,"Elemento agregado correctamente al inventario")
    return render(request, "inventario/forminventario.html",{"elementos":elementos,"unidades":unidades})

@login_required
def editarinventario(request,id):
    elemento=inventario.objects.get(id=id)
    if request.method == "POST":
        nombre_nuevo=request.POST.get("elemento")
        cantidad_nueva=request.POST.get("cantidad")
        marca_nueva=request.POST.get("marca")
        observacion_nueva=request.POST.get("observacion")

        elemento.elemento=nombre_nuevo
        elemento.cantidad=cantidad_nueva
        elemento.marca=marca_nueva
        elemento.observaciones=observacion_nueva

        elemento.save()
        messages.success(request, "Elemento editado satisfactoriamente.")

    return render(request,"edit/editelemento.html",{"elemento":elemento})

@login_required
def eliminarinventario(request,id):
    elemento=inventario.objects.filter(id=id)
    elemento.delete()
    messages.success(request,"Elemento eliminado satisfactoriamente.")
    return redirect("inventario")

@login_required
def agregarelemento(request):
    if request.method=="POST":
        tipo=request.POST.get("tipoelemento")
        elemento=tipoElemento(descripcion=tipo)
        elemento.save()
        messages.success(request,"Elemento guardado exitosamente.")
    return render(request, "inventario/formelemento.html")


@login_required
def agregarunidad(request):
    if request.method == "POST":
        unidad = request.POST.get("unidad")
        unidadtipo = tipoUnidad(descripcion=unidad)
        unidadtipo.save()
        messages.success(request, "Unidad de medida guardada exitosamente.")
    return render(request, "inventario/formunidad.html")

@login_required
def tipo_elemento(request):
    if request.method == "POST":
        id=request.POST.get("id")
        return redirect("filtrar_inventario",id)

@login_required
def filtrar_elemento(request,id):
    elementos=inventario.objects.filter(tipo=id)
    ids_tipos_elemento = inventario.objects.exclude(tipo__isnull=True).values_list('tipo', flat=True).distinct()
    items = tipoElemento.objects.filter(id__in=ids_tipos_elemento)
    return render(request,"inventario/inventario.html",{"elementos":elementos,'items':items})

@login_required
def cantidadxrestauracion(request):
    cantidad=cantidad_x_restauracion.objects.all()
    for elemento in cantidad:
        bandera=elemento.material.cantidad/elemento.necesario
        if bandera>=1:
            elemento.disponible=True
        else:
            elemento.disponible=False
        elemento.restauraciones=int(bandera)
        elemento.save()
    return render(request, "cantidadxrestauracion/cantidadxrestauracion.html",{"cantidad":cantidad})

def agregar_cantxrest(request):
    cantidad=cantidad_x_restauracion.objects.all()
    total = inventario.objects.exclude(id__in=cantidad.values_list('id', flat=True))
    if request.method == "POST":
        elemento = request.POST.get("elemento")
        unidad = request.POST.get("cantidad")
        pieza=inventario.objects.get(id=elemento)
        restauracion=pieza.cantidad/int(unidad)
        if restauracion >= 1:
            disponible=True
        else: 
            disponible=False
        mantenimiento=cantidad_x_restauracion(
            material=inventario.objects.get(id=elemento),
            necesario=unidad,
            restauraciones=restauracion,
            disponible=disponible
        )
        mantenimiento.save()
        messages.success(request, "Elemento guardado exitosamente.")
    return render(request, "cantidadxrestauracion/formcantxrest.html",{"total":total,"cantidad":cantidad})

@login_required
def dato(request):
    if request.method=="POST":
        disponible=request.POST.get("disponible")
        return redirect("filtrar_utilidad",disponible)

@login_required
def filtrar_disponible(request,id):
    if id==0:
        cantidad=cantidad_x_restauracion.objects.filter(disponible=False)
    elif id==1:
        cantidad = cantidad_x_restauracion.objects.filter(disponible=True)
    return render(request, "cantidadxrestauracion/cantidadxrestauracion.html",{"cantidad":cantidad})

@login_required
def editar_cantidad(request,id):
    cantidad_id=cantidad_x_restauracion.objects.get(id=id)
    if request.method == "POST":
        cantidad_nueva=request.POST.get("cantidad")

        cantidad_id.necesario=cantidad_nueva

        cantidad_id.save()

        messages.success(request, "Elemento guardado exitosamente.")

    
    return render(request,"edit/editcantidad.html",{"cantidad_id":cantidad_id})

@login_required
def eliminar_cantidad(request,id):
    cantidad=cantidad_x_restauracion.objects.filter(id=id)
    cantidad.delete()
    messages.success(request, "Elemento eliminado satisfactoriamente.")
    return redirect("cantidadxrestauracion")

@login_required
def bitacora(request):
    lista=elementos_x_bitacora.objects.all()
    nombre = request.GET.get("nombre")
    fecha = request.GET.get("fecha")
    tipo = request.GET.get("tipo")

    registros = bitacora_inventario.objects.all()
    # Aplicar filtros uno por uno
    if nombre:
        registros = registros.filter(responsable__icontains=nombre)
    if fecha:
        registros = registros.filter(fecha=fecha)

    if tipo:
        registros = registros.filter(
            tipo_ingreso__iexact=tipo
        )  # iexact = ignora mayúsculas

    lista=elementos_x_bitacora.objects.filter(lista__in=registros)

    return render(request, "bitacora/bitacora.html",{"lista":lista})

@login_required
def reporte_ingresos(request):
    elementos=inventario.objects.all()
    unidades=tipoUnidad.objects.all()
    tipo=tipoElemento.objects.all()
    return render(request,"bitacora/reporteingresos.html",{"elementos":elementos,"unidades":unidades,"tipo":tipo})

@login_required
@csrf_exempt  # permite POST desde fetch (recuerda csrf_token si no usas esto)
def agregar_ingreso(request):
    if request.method == "POST":
        data = json.loads(request.body)

        responsable = data.get("responsable")
        fecha = data.get("fecha")
        observaciones = data.get("observaciones")
        items = data.get("items", [])

        # Crear cabecera
        lista = bitacora_inventario.objects.create(
            responsable=responsable, fecha=fecha, observaciones=observaciones, tipo_ingreso="ingreso",
        )

        # Guardar items
        for item in items:
            if item.get("nuevo"):  # si viene como producto nuevo
                producto = inventario.objects.create(elemento=item["nombre"],cantidad=int(item["cantidad"]),unidad=tipoUnidad.objects.get(id=int(item["unidad_id"])),tipo=tipoElemento.objects.get(id=int(item["tipo"])))
            else:
                producto = inventario.objects.get(id=item["producto_id"])
                producto.cantidad = producto.cantidad + int(item["cantidad"])
                print(producto.cantidad)

            elementos_x_bitacora.objects.create(
                lista=lista,
                elemento=producto,
                cantidad=item["cantidad"],
            )

            producto.save()

        return JsonResponse({"status": "ok", "mensaje": "Lista guardada con éxito"})

    return JsonResponse({"status": "error", "mensaje": "Método no permitido"})


@login_required
def reporte_salidas(request):
    elementos = inventario.objects.all()
    return render(
        request,
        "bitacora/reportesalidas.html",
        {"elementos": elementos},
    )


@login_required
@csrf_exempt  # permite POST desde fetch (recuerda csrf_token si no usas esto)
def agregar_salida(request):
    if request.method == "POST":
        data = json.loads(request.body)

        responsable = data.get("responsable")
        fecha = data.get("fecha")
        observaciones = data.get("observaciones")
        items = data.get("items", [])

        # Crear cabecera
        lista = bitacora_inventario.objects.create(
            responsable=responsable,
            fecha=fecha,
            observaciones=observaciones,
            tipo_ingreso="salida",
        )

        # Guardar items
        for item in items:
            producto = inventario.objects.get(id=item["producto_id"])
            producto.cantidad = producto.cantidad - int(item["cantidad"])

            elementos_x_bitacora.objects.create(
                lista=lista,
                elemento=producto,
                cantidad=item["cantidad"],
            )

            producto.save()

        return JsonResponse({"status": "ok", "mensaje": "Lista guardada con éxito"})

    return JsonResponse({"status": "error", "mensaje": "Método no permitido"})


@login_required
def reporte_paz_y_salvo(request):
    elementos = inventario.objects.all()
    return render(
        request,
        "bitacora/reportepazysalvo.html",
        {"elementos": elementos},
    )


@login_required
@csrf_exempt  # permite POST desde fetch (recuerda csrf_token si no usas esto)
def agregar_pazysalvo(request):
    if request.method == "POST":
        data = json.loads(request.body)

        responsable = data.get("responsable")
        fecha = data.get("fecha")
        observaciones = data.get("observaciones")
        items = data.get("items", [])

        # Crear cabecera
        lista = bitacora_inventario.objects.create(
            responsable=responsable,
            fecha=fecha,
            observaciones=observaciones,
            tipo_ingreso="paz y salvo",
        )

        # Guardar items
        for item in items:
            producto = inventario.objects.get(id=item["producto_id"])
            producto.cantidad = producto.cantidad + int(item["cantidad"])

            elementos_x_bitacora.objects.create(
                lista=lista,
                elemento=producto,
                cantidad=item["cantidad"],
            )

            producto.save()

        return JsonResponse({"status": "ok", "mensaje": "Lista guardada con éxito"})

    return JsonResponse({"status": "error", "mensaje": "Método no permitido"})


@login_required
def reporte_falla(request):
    tipo=tipoElemento.objects.get(descripcion="Herramienta")
    elementos = inventario.objects.filter(tipo=tipo)
    return render(
        request,
        "bitacora/reportefalla.html",
        {"elementos": elementos},
    )


@login_required
@csrf_exempt  # permite POST desde fetch (recuerda csrf_token si no usas esto)
def agregar_falla(request):
    if request.method == "POST":
        data = json.loads(request.body)

        responsable = data.get("responsable")
        fecha = data.get("fecha")
        observaciones = data.get("observaciones")
        items = data.get("items", [])

        # Crear cabecera
        lista = bitacora_inventario.objects.create(
            responsable=responsable,
            fecha=fecha,
            observaciones=observaciones,
            tipo_ingreso="falla",
        )

        # Guardar items
        for item in items:
            producto = inventario.objects.get(id=item["producto_id"])
            producto.cantidad = producto.cantidad - int(item["cantidad"])

            elementos_x_bitacora.objects.create(
                lista=lista,
                elemento=producto,
                cantidad=item["cantidad"],
            )

            producto.save()

        return JsonResponse({"status": "ok", "mensaje": "Lista guardada con éxito"})

    return JsonResponse({"status": "error", "mensaje": "Método no permitido"})

@login_required
def eliminar_bitacora(request,id):
    elemento=elementos_x_bitacora.objects.get(id=id)
    if elemento.lista.tipo_ingreso == "ingreso" or elemento.lista.tipo_ingreso == "paz y salvo":
        item=inventario.objects.get(id=elemento.elemento.id)
        item.cantidad = item.cantidad - elemento.cantidad
        item.save()
    elif elemento.lista.tipo_ingreso == "salida" or elemento.lista.tipo_ingreso == "falla":
        item = inventario.objects.get(id=elemento.elemento.id)
        item.cantidad = item.cantidad + elemento.cantidad
        item.save()
    elemento.delete()
    return redirect("bitacora")

@login_required
def excel_inventario(request):
    # Crear un nuevo libro y hoja
    wb = Workbook()
    ws = wb.active
    ws.title = "Inventario"

    # Escribir encabezados
    ws.append(["Tipo", "Elemento", "Cantidad", "Unidad","Marca","Observaciones"])

    # Obtener los registros de la base de datos (puedes aplicar filtros aquí)
    registros = inventario.objects.all()

    # Escribir datos fila por fila
    for registro in registros:
        ws.append(
            [
                registro.tipo.descripcion,
                registro.elemento,
                registro.cantidad,
                registro.unidad.descripcion,
                registro.marca,
                registro.observaciones,
            ]
        )

    # Preparar la respuesta HTTP
    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = 'attachment; filename="inventario.xlsx"'

    # Guardar el archivo en la respuesta
    wb.save(response)
    return response


@login_required
def excel_bitacora(request):
    # Crear un nuevo libro y hoja
    wb = Workbook()
    ws = wb.active
    ws.title = "Bitacora"

    # Escribir encabezados
    ws.append(["Fecha", "Acción", "Elemento", "Cantidad","Tipo unidad", "Observaciones", "Responsable"])

    # Obtener los registros de la base de datos (puedes aplicar filtros aquí)
    registros = elementos_x_bitacora.objects.all()

    # Escribir datos fila por fila
    for registro in registros:
        ws.append(
            [
                registro.lista.fecha,
                registro.lista.tipo_ingreso,
                registro.elemento.elemento,
                registro.cantidad,
                registro.elemento.unidad.descripcion,
                registro.lista.observaciones,
                registro.lista.responsable,
            ]
        )

    # Preparar la respuesta HTTP
    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = 'attachment; filename="bitacora.xlsx"'

    # Guardar el archivo en la respuesta
    wb.save(response)
    return response
