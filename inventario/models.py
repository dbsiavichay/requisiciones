# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.urls import reverse_lazy
from django.db import models


class Categoria(models.Model):
	nombre = models.CharField(max_length=140)	
	padre = models.ForeignKey('self', blank=True, null=True)

	def __unicode__(self):		
		return '%s / %s' % (str(self.padre), self.nombre) if self.padre else self.nombre

	def get_absolute_url(self):
		return reverse_lazy('editar_categoria', args=[self.id])

class Producto(models.Model):
	nombre = models.CharField(max_length=140)			
	categoria = models.ForeignKey(Categoria, verbose_name='categoría')	

	def __unicode__(self):
		return self.nombre

	def get_absolute_url(self):
		return reverse_lazy('editar_producto', args=[self.id])