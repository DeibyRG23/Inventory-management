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

class cantidad_x_restauracion(models.Model):
    material=models.ForeignKey(inventario,on_delete=models.CASCADE)
    necesario=models.IntegerField()
    restauraciones=models.IntegerField()
    disponible=models.BooleanField()

class bitacora_inventario(models.Model):
    responsable=models.CharField(max_length=80)
    fecha=models.DateField()
    observaciones=models.CharField(max_length=500)
    tipo_ingreso=models.CharField(max_length=80,blank=True)

class elementos_x_bitacora(models.Model):
    lista=models.ForeignKey(bitacora_inventario,on_delete=models.CASCADE)
    elemento=models.ForeignKey(inventario,on_delete=models.CASCADE)
    cantidad=models.IntegerField()

class responsable_alamacen(models.Model):
    nombre_responsable=models.CharField(max_length=100)
    cargo=models.CharField(max_length=50)
    contacto=models.CharField(max_length=50)
    fecha=models.DateField(auto_now_add=True,null=True)
