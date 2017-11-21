# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible
from django.db import models
from django.urls import reverse_lazy
from django.utils.html import format_html		
from django.core.validators import MaxValueValidator, MinValueValidator

@python_2_unicode_compatible
class Pedido(models.Model):
	class Meta:
		ordering = ['-fecha']
	ESTADO_CHOICES = (
		(1, 'Borrador'),(2, 'Generado'),(3, 'En proceso'),
		(4, 'Negado'),(5, 'Enviado'),(6, 'Recibido'),
		(10, 'Cancelado'),
	)

	ESTADO_LABELS = (
		(1, 'default'),(2, 'primary'),(3, 'success'),
		(4, 'danger'),(5, 'info'), (6, 'warning'),
		(10, 'danger'),
	)

	fecha = models.DateTimeField(auto_now_add=True)
	estado = models.PositiveSmallIntegerField(choices=ESTADO_CHOICES, default=1)
	nota = models.TextField(blank=True, null=True, verbose_name='nota general')
	usuario = models.ForeignKey('auth.User')

	def __str__(self):
		return '%s | %s' % (self.id, self.usuario.get_full_name())

	def get_estado(self):
		return format_html(
            '<span class="label label-{}">{}</span>',
            dict(self.ESTADO_LABELS).get(self.estado),
            dict(self.ESTADO_CHOICES).get(self.estado),            
        )		

	def get_absolute_url(self):
		return reverse_lazy('ver_pedido', args=[self.id])

class LineaPedido(models.Model):	
	cantidad_pedida = models.FloatField(validators = [MinValueValidator(0.01),])
	cantidad_recibida = models.FloatField(blank=True, null=True)
	fecha_recepcion = models.DateTimeField(auto_now=True)	
	producto = models.ForeignKey('inventario.Producto')
	pedido = models.ForeignKey(Pedido)

