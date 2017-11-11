# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible
from django.db import models

@python_2_unicode_compatible
class Notificacion(models.Model):
	class Meta:
		ordering = ['fecha_creacion',]

	remitente = models.ForeignKey('auth.User', related_name='remitente')
	receptor = models.ForeignKey('auth.User', related_name='receptor')
	mensaje = models.TextField(blank=True, null=True)
	fecha_creacion = models.DateTimeField(auto_now_add=True)
	fecha_lectura = models.DateTimeField(blank=True, null=True)
	visto = models.BooleanField(default=False)
	id_objecto = models.IntegerField()
	tipo_contenido = models.ForeignKey('contenttypes.ContentType')

	def __str__(self):
		return self.mensaje