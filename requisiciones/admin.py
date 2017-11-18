# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from .models import *

class LineaPedidoInline(admin.TabularInline):
    model = LineaPedido    

class PedidoAdmin(admin.ModelAdmin):
	list_display = ('id','get_usuario', 'fecha', 'estado', 'nota' )
	inlines = [
		LineaPedidoInline
	]

	def get_usuario(self, obj):
		return obj.usuario.get_full_name()

admin.site.register(Pedido, PedidoAdmin)
