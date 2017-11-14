# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from .models import *

class NotificacionAdmin(admin.ModelAdmin):
	list_display = ('get_remitente', 'get_receptor', 'mensaje', 'get_estado' )	

	def get_remitente(self, obj):
		return obj.remitente.get_full_name()

	def get_receptor(self, obj):
		return obj.receptor.get_full_name()

admin.site.register(Notificacion, NotificacionAdmin)

