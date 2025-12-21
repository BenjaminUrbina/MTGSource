from django.db import models


# Modelo inicial de cartas
# Investigar las propiedades mas comunes y posibles del modelado

class bd_Cartas(models.Model):
    title = models.CharField(max_length=200)
    descripcion = models.CharField(blank=True)
    done = models.BooleanField(default=False) 
