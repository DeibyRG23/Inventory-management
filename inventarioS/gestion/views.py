from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from gestion.models import *
from django.contrib import messages

# Create your views here.
@login_required
def novedades(request):
    return render(request,"novedades/novedades.html")


@login_required
def inventarioTotal(request):
    elementos=inventario.objects.all()
    return render(request, "inventario/inventario.html",{"elementos":elementos})

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
        return redirect("inventario")
    return render(request, "inventario/forminventario.html",{"elementos":elementos,"unidades":unidades})

@login_required
def agregarelemento(request):
    if request.method=="POST":
        tipo=request.POST.get("tipoelemento")
        elemento=tipoElemento(descripcion=tipo)
        elemento.save()
        messages.success(request,"Elemento guardado exitosamente.")
        return redirect('inventario')
    return render(request, "inventario/formelemento.html")


@login_required
def agregarunidad(request):
    if request.method == "POST":
        unidad = request.POST.get("unidad")
        unidadtipo = tipoUnidad(descripcion=unidad)
        unidadtipo.save()
        messages.success(request, "Unidad de medida guardada exitosamente.")
        return redirect("inventario")
    return render(request, "inventario/formunidad.html")


@login_required
def cantidadxrestauracion(request):
    return render(request, "cantidadxrestauracion/cantidadxrestauracion.html")


@login_required
def bitacora(request):
    return render(request, "bitacora/bitacora.html")
