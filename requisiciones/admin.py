# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from .models import *

class LugarAdmin(admin.ModelAdmin):
	model = Lugar

class LineaPedidoInline(admin.TabularInline):
    model = LineaPedido    

class PedidoAdmin(admin.ModelAdmin):
	list_display = ('id','get_usuario', 'fecha', 'lugar', 'estado', 'nota' )
	inlines = [
		LineaPedidoInline
	]

	def get_usuario(self, obj):
		return obj.usuario.get_full_name()

admin.site.register(Lugar, LugarAdmin)
admin.site.register(Pedido, PedidoAdmin)
