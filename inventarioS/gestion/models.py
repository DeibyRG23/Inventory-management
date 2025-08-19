from django.db import models

# Create your models here.
class tipoElemento(models.Model):
    descripcion=models.CharField(max_length=20)

class tipoUnidad(models.Model):
    descripcion=models.CharField(max_length=20)

class inventario(models.Model):
    tipo=models.ForeignKey(tipoElemento,on_delete=models.CASCADE)
    elemento=models.CharField(max_length=100)
    cantidad=models.IntegerField()
    unidad=models.ForeignKey(tipoUnidad,on_delete=models.CASCADE)
    marca=models.CharField(blank=True,max_length=50)
    observaciones=models.CharField(blank=True,max_length=500)
