from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages


# Create your views here.
def inicio_sesion(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("novedades")
        else:
            messages.error(request, "Usuario o contraseña incorrectos")

    return render(request, "login/login.html")


def cerrar_sesion(request):
    logout(request)
    return redirect("home")

