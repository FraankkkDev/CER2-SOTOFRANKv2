from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator

Usuario = get_user_model()

class Evento(models.Model):
    titulo = models.CharField(max_length=200, verbose_name="Título")
    tiempo = models.DateTimeField(verbose_name="Fecha y hora")
    lugar = models.CharField(max_length=200, verbose_name="Lugar")
    imagen = models.ImageField(upload_to='event_images/', null=True, blank=True, verbose_name="Imagen")
    valor = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Valor")
    plazas_totales = models.IntegerField(validators=[MinValueValidator(0)], default=0, verbose_name="Número de plazas")
    plazas_disponibles = models.IntegerField(validators=[MinValueValidator(0)], default=0, verbose_name="Plazas disponibles")

    asistentes = models.ManyToManyField(Usuario, through='Registro', related_name='eventos_asistidos')

    def get_valor_clp(self):
        if self.valor == 0:
            return "Gratuito"
        valor_int = int(self.valor)
        formato_us = f'{valor_int:,}'
        formato_clp = formato_us.replace(',', '.')
        return f'CLP ${formato_clp}'

    class Meta:
        verbose_name = "Evento"
        verbose_name_plural = "Eventos"
        ordering = ['tiempo']

    def __str__(self):
        return self.titulo
    
class Registro(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, verbose_name="Usuario")
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE, verbose_name="Evento")
    fecha_registro = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de registro")

    class Meta:
        verbose_name = "Registro"
        verbose_name_plural = "Registros"
        unique_together = ('usuario', 'evento')

    def __str__(self):
        return f"{self.usuario.username} inscrito en {self.evento.titulo}"