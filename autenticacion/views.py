# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.generic import DetailView
from .models import Perfil

class PerfilDetailView(DetailView):
	model = Perfil

	def get(self, request, *args, **kwargs):
		if request.is_ajax():
			self.object = self.get_object()
			res = {
				'cedula': self.object.usuario.username,
				'user_id': self.object.usuario.id,
				'nombre': self.object.usuario.get_full_name(),
				'gestiona_pedidos': self.object.gestiona_pedidos
			}
			return JsonResponse(res)
		else:
			return super(PerfilDetailView, self).get(request, *args, **kwargs)

	def get_object(self):
		return self.request.user.perfil