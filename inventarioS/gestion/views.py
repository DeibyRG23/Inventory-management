from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from gestion.models import *
from django.contrib import messages

# Create your views here.
@login_required
def novedades(request):
    return render(request,"novedades/novedades.html")


@login_required
def inventario(request):
    return render(request, "inventario/inventario.html")

@login_required
def agregarinventario(request):
    elementos=tipoElemento.objects.all()
    unidades=tipoUnidad.objects.all()
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
