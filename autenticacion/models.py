# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible
from django.db import models

@python_2_unicode_compatible
class Perfil(models.Model):
	class Meta:
		verbose_name_plural = 'perfiles'

	fecha_nacimiento = models.DateField(blank=True, null=True, verbose_name='fecha de nacimiento')
	fecha_creacion = models.DateTimeField(auto_now_add=True)
	gestiona_pedidos = models.BooleanField(default=False, verbose_name='gestión de pedidos')
	imagen = models.ImageField(upload_to='perfiles/imagenes/', blank=True, null=True, verbose_name='imagen de perfil')
	usuario = models.OneToOneField('auth.User', on_delete=models.CASCADE)

	def __str__(self):
		return self.usuario.get_full_name()
