# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.views.generic import UpdateView, DetailView
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

	def get_object(self, queryset=None):
		username = self.request.GET.get('username') or self.kwargs.get('username') or None
		try:			
			perfil = self.model.objects.get(usuario__username=username)
		except self.model.DoesNotExist:
			perfil = self.request.user.perfil		

		return perfil

class PerfilUpdateView(UpdateView):
	model = Perfil
	fields = ('imagen',)	
	
	def post(self, request, *args, **kwargs):		
		self.object = self.get_object()
		if self.object.usuario != request.user:
			return redirect('perfil', self.object.usuario.username)
		self.success_url = reverse_lazy('perfil', args=[self.object.usuario.username,])
		return super(PerfilUpdateView, self).post(request, *args, **kwargs)

	def get(self, request, *args, **kwargs):
		self.object = self.get_object()		
		return redirect('perfil', self.object.usuario.username)