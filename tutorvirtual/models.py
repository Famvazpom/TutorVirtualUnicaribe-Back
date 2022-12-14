from django.db import models

class Contenido(models.Model):
    titulo = models.CharField(max_length=50)
    contenido = models.TextField()
    relacionados = models.ManyToManyField('self')
    autor = models.CharField(max_length=50)

    class Meta:
        verbose_name = ("Contenido")
        verbose_name_plural = ("Contenidos")

    def __str__(self):
        return self.titulo
