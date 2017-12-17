# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User, Group
from .forms import CustomUserCreationForm
from .models import *

class PerfilInline(admin.StackedInline):
    model = Perfil
    can_delete = False
    verbose_name_plural = 'Perfil'    

class CustomUserAdmin(UserAdmin):
	add_form = CustomUserCreationForm
	fieldsets = (        
		(None, {
			'fields': ('username','password')
		}),
        ('Información personal', {            
            'fields': ('first_name','last_name', 'email')
        }),
        ('Permisos', {
        	'fields': ('is_active', 'is_staff', 'is_superuser')
        }),
        ('Fechas importantes', {
        	'fields': ('date_joined', 'last_login')
        })
    )	

	inlines =[
    	PerfilInline, 
    ]

	def get_inline_instances(self, request, obj=None):
		if not obj:
			return list()
		return super(CustomUserAdmin, self).get_inline_instances(request, obj)

admin.site.unregister(Group)
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
