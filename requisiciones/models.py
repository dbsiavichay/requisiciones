# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible
from django.db import models
from django.urls import reverse_lazy
from django.utils.html import format_html		
from django.core.validators import MaxValueValidator, MinValueValidator

class Pedido(models.Model):
	class Meta:
		ordering = ['-fecha']
	ESTADO_CHOICES = (
		(1, 'Borrador'),(2, 'Generado'),(3, 'En proceso'),
		(4, 'Negado'),(5, 'Entregado'),(6, 'Finalizado'),
		(7, 'Cancelado'),
	)

	ESTADO_LABELS = (
		(1, 'default'),(2, 'primary'),(3, 'success'),
		(4, 'danger'),(5, 'info'),(6, 'warning'),
		(7, 'danger'),
	)

	fecha = models.DateTimeField(auto_now_add=True)
	estado = models.PositiveSmallIntegerField(choices=ESTADO_CHOICES, default=1)
	observacion = models.TextField(blank=True, null=True)
	usuario = models.ForeignKey('auth.User')

	def get_estado(self):
		return format_html(
            '<span class="label label-{}">{}</span>',
            dict(self.ESTADO_LABELS).get(self.estado),
            dict(self.ESTADO_CHOICES).get(self.estado),            
        )		

	def get_absolute_url(self):
		return reverse_lazy('ver_pedido', args=[self.id])

class LineaPedido(models.Model):
	cantidad = models.FloatField(validators = [MinValueValidator(0.01),])	
	producto = models.ForeignKey('inventario.Producto')
	pedido = models.ForeignKey(Pedido)

