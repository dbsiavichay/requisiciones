# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .forms import CustomUserCreationForm
from .models import *

class PerfilInline(admin.StackedInline):
    model = Perfil
    can_delete = False
    verbose_name_plural = 'Perfil'    

class CustomUserAdmin(UserAdmin):
	add_form = CustomUserCreationForm
	inlines =[
    	PerfilInline, 
    ]

	def get_inline_instances(self, request, obj=None):
		if not obj:
			return list()
		return super(CustomUserAdmin, self).get_inline_instances(request, obj)

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
