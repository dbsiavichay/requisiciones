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
	fields = '__all__'
	success_url = reverse_lazy('pedidos')

	def get_context_data(self, **kwargs):
		context = super(PedidoUpdateView, self).get_context_data(**kwargs)
		context['formset'] = self.get_lineapedido_formset()

		return context

	def form_valid(self, form):
		formset = self.get_lineapedido_formset()
		
		if formset.is_valid():
			self.object = self.get_object()
			formset.instance = self.object
			formset.save()			
			return redirect(self.get_success_url())
		else:
			return self.form_invalid(form)

	def get_lineapedido_formset(self):
		self.object = self.get_object()
		post_data = self.request.POST if self.request.method == 'POST' else None
		formset = LineaPedidoInlineFormSet(post_data, instance=self.object)
		return formset
