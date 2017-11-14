# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.generic import ListView, DetailView
from .models import *

class NotificacionListView(ListView):
	model = Notificacion

	def get_queryset(self):
		queryset = super(NotificacionListView, self).get_queryset()
		queryset = queryset.filter(receptor=self.request.user)		
		#qs = queryset.filter(status=Notificacion.UNREAD)
		#qs.update(status=Notificacion.VIEWED)
		return queryset	

class NotificationDetailView(DetailView):
	model = Notificacion

	def get(self, request, *args, **kwargs):
		self.object = self.get_object()
		if request.is_ajax():			
			res = [
				self.object.remitente.get_full_name(),
				self.object.mensaje,
				'Justo ahora',
				self.object.get_estado(),
				self.object.get_absolute_url()
			]

			return JsonResponse({'data':res})

		if self.object.receptor != request.user:
			return redirect('notificaciones')

		self.object.visto = True
		self.object.save()
		#fecha lectura		
		return redirect(self.object.get_objecto().get_absolute_url())