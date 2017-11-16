# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from .models import *

class CategoriaAdmin(admin.ModelAdmin):
	pass	

class ProductoAdmin(admin.ModelAdmin):
	list_display = ('nombre', 'stock', 'categoria')

class ProductoLogAdmin(admin.ModelAdmin):
	list_display = ('tipo', 'producto', 'cantidad', 'fecha', 'pedido')

admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(Producto, ProductoAdmin)
admin.site.register(ProductoLog, ProductoLogAdmin)