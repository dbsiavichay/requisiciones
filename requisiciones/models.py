# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.urls import reverse_lazy
from django.core.validators import MaxValueValidator, MinValueValidator

class Pedido(models.Model):
	ESTADO_CHOICES = (
		(1, 'Borrador'),
		(2, 'Generado'),
		(3, 'En proceso'),
		(4, 'Negado'),
		(5, 'Entregado'),
		(6, 'Finalizado'),
		(7, 'Cancelado'),
	)

	fecha = models.DateTimeField(auto_now_add=True)
	estado = models.PositiveSmallIntegerField(choices=ESTADO_CHOICES, default=1)
	observacion = models.TextField(blank=True, null=True)
	usuario = models.ForeignKey('auth.User')

	def get_absolute_url(self):
		return reverse_lazy('editar_pedido', args=[self.id])

class LineaPedido(models.Model):
	cantidad = models.FloatField(validators = [MinValueValidator(0.01),])	
	producto = models.ForeignKey('inventario.Producto')
	pedido = models.ForeignKey(Pedido)

