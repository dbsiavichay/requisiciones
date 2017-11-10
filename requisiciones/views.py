# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from .forms import *
from .models import *

class PedidoListView(ListView):
	model = Pedido

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
		if self.object.estado != 1:
			return redirect('ver_pedido', self.object.id)
		return super(PedidoUpdateView, self).get(request, *args, **kwargs)

class CancelarPedidoUpdateView(UpdateView):
	model = Pedido
	fields = ()
	success_url = reverse_lazy('pedidos')

	def post(self, request, *args, **kwargs):
		return redirect(self.get_success_url())

	def get(self, request, *args, **kwargs):
		self.object = self.get_object()
		if self.object.estado > 3:
			return redirect('ver_pedido', self.object.id)
			
		self.object.estado = 7
		self.object.save()
		return redirect('ver_pedido', self.object.id)

class PedidoDetailView(DetailView):
	model = Pedido
