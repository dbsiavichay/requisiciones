# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db.models import Q
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from pure_pagination.mixins import PaginationMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from .forms import *
from .models import *

class PedidoListView(PaginationMixin, ListView):
	paginate_by=10
	model = Pedido

	def get_queryset(self):
		queryset = super(PedidoListView, self).get_queryset()
		if self.request.user.perfil.gestiona_pedidos:
			queryset = queryset.exclude(Q(estado=1), ~Q(usuario=self.request.user))
		else:
			queryset = queryset.filter(usuario=self.request.user)
		return queryset

class PedidoCreateView(CreateView):
	model = Pedido
	form_class = PedidoForm
	success_url = reverse_lazy('pedidos')

	def get_context_data(self, **kwargs):
		context = super(PedidoCreateView, self).get_context_data(**kwargs)
		context['formset'] = self.get_lineapedido_formset()

		return context

	def form_valid(self, form):
		formset = self.get_lineapedido_formset()
		
		if formset.is_valid():
			self.object = form.save(commit=False)
			self.object.usuario = self.request.user
			self.object.save()
			formset.instance = self.object
			formset.save()			
			return redirect(self.get_success_url())
		else:
			return self.form_invalid(form)

	def get_lineapedido_formset(self):
		post_data = self.request.POST if self.request.method == 'POST' else None
		formset = LineaPedidoInlineFormSet(post_data)
		return formset

class PedidoUpdateView(UpdateView):
	model = Pedido
	form_class = PedidoForm
	success_url = reverse_lazy('pedidos')

	def get_context_data(self, **kwargs):
		context = super(PedidoUpdateView, self).get_context_data(**kwargs)
		context['formset'] = self.get_lineapedido_formset()

		return context

	def form_valid(self, form):
		formset = self.get_lineapedido_formset()
		
		if formset.is_valid():						
			form.save()
			formset.save()			
			return redirect(self.get_success_url())
		else:
			return self.form_invalid(form)

	def get_lineapedido_formset(self):
		self.object = self.get_object()
		post_data = self.request.POST if self.request.method == 'POST' else None
		formset = LineaPedidoInlineFormSet(post_data, instance=self.object)
		return formset

	def get(self, request, *args, **kwargs):
		self.object = self.get_object()		

		if self.object.usuario != request.user:
			if request.user.perfil.gestiona_pedidos:
				return redirect('ver_pedido', self.object.id)
			else:			
				return redirect('pedidos')
		if self.object.estado != 1:
			return redirect('ver_pedido', self.object.id)
		return super(PedidoUpdateView, self).get(request, *args, **kwargs)

class PedidoDetailView(DetailView):
	model = Pedido

	def get(self, request, *args, **kwargs):
		self.object = self.get_object()
		if self.object.usuario != request.user and not request.user.perfil.gestiona_pedidos:
			return redirect('pedidos')
		return super(PedidoDetailView, self).get(request, *args, **kwargs)

class BasePedidoUpdateView(UpdateView):
	model = Pedido
	fields = ()
	success_url = reverse_lazy('pedidos')
	estado = 1

	def post(self, request, *args, **kwargs):
		return redirect(self.get_success_url())

	def guardar(self):
		self.object.estado = self.estado
		self.object.save()
		return redirect('ver_pedido', self.object.id)

class CancelarPedidoUpdateView(BasePedidoUpdateView):
	estado = 10

	def get(self, request, *args, **kwargs):
		self.object = self.get_object()
		if self.object.usuario != request.user:
			return redirect('pedidos')
		if self.object.estado > 2:
			return redirect('ver_pedido', self.object.id)
			
		return self.guardar()

class ProcesarPedidoUpdateView(BasePedidoUpdateView):
	estado = 3

	def get(self, request, *args, **kwargs):
		self.object = self.get_object()
		if self.object.estado != 2:
			return redirect('ver_pedido', self.object.id)
			
		return self.guardar()

class NegarPedidoUpdateView(BasePedidoUpdateView):	
	estado = 4

	def get(self, request, *args, **kwargs):
		self.object = self.get_object()
		if self.object.estado != 2 and self.object.estado != 3:
			return redirect('ver_pedido', self.object.id)
			
		return self.guardar()

class EntregarPedidoUpdateView(BasePedidoUpdateView):	
	estado = 5

	def get(self, request, *args, **kwargs):
		self.object = self.get_object()
		if self.object.estado != 2 and self.object.estado != 3:
			return redirect('ver_pedido', self.object.id)
			
		return self.guardar()