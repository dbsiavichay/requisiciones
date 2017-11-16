# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible
from django.urls import reverse_lazy
from django.db import models

@python_2_unicode_compatible
class Categoria(models.Model):
	nombre = models.CharField(max_length=140)	
	padre = models.ForeignKey('self', blank=True, null=True)

	def __str__(self):		
		return '%s / %s' % (str(self.padre), self.nombre) if self.padre else self.nombre

	def get_absolute_url(self):
		return reverse_lazy('editar_categoria', args=[self.id])

@python_2_unicode_compatible
class Producto(models.Model):
	nombre = models.CharField(max_length=140)			
	categoria = models.ForeignKey(Categoria, verbose_name='categoría')
	stock = models.FloatField(blank=True, null=True)

	def __str__(self):
		return self.nombre

	def get_absolute_url(self):
		return reverse_lazy('editar_producto', args=[self.id])

@python_2_unicode_compatible
class ProductoLog(models.Model):
	TIPO_CHOICES = (
		(1, 'Entrada'),
		(2, 'Salida'),
	)

	tipo = models.PositiveSmallIntegerField(choices = TIPO_CHOICES)
	producto = models.ForeignKey(Producto)
	cantidad = models.FloatField()
	fecha = models.DateTimeField(auto_now_add=True)	
	observacion = models.TextField(blank=True, null=True)
	pedido = models.ForeignKey('requisiciones.Pedido', blank=True, null=True)

	def __str__(self):
		return '%s|%s > %s' % (
			dict(self.TIPO_CHOICES).get(self.tipo),
			self.producto, self.cantidad
		)
