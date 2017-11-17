# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from pure_pagination import PaginationMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from .models import *
from .forms import *

class CategoriaListView(PaginationMixin, ListView):	
	model = Categoria
	paginate_by=10

class CategoriaCreateView(CreateView):
	model = Categoria
	fields = '__all__'
	success_url = reverse_lazy('categorias')

class CategoriaUpdateView(UpdateView):
	model = Categoria
	fields = '__all__'
	success_url = reverse_lazy('categorias')

class CategoriaDeleteView(DeleteView):
	model = Categoria
	success_url = reverse_lazy('categorias')

class ProductoListView(PaginationMixin, ListView):
	model = Producto
	paginate_by=10

class ProductoCreateView(CreateView):
	model = Producto
	fields = '__all__'
	success_url = reverse_lazy('productos')

class ProductoUpdateView(UpdateView):
	model = Producto
	fields = '__all__'
	success_url = reverse_lazy('productos')

class ProductoDeleteView(DeleteView):
	model = Producto
	success_url = reverse_lazy('productos')

class ProductoLogCreateView(CreateView):
	model = ProductoLog
	fields = ('cantidad', 'observacion')
	success_url = reverse_lazy('productos')

	def get_context_data(self, **kwargs):		
		context = super(ProductoLogCreateView, self).get_context_data(**kwargs)
		context.update({
			'producto': self.get_producto()
		})
		return context

	def form_valid(self, form):
		producto = self.get_producto()
		if producto is None:
			return redirect(self.success_url)
		self.object = form.save(commit=False)
		self.object.tipo = 1
		self.object.producto = producto
		self.object.save()		
		return redirect(self.get_success_url())

	def get(self, request, *args, **kwargs):
		producto = self.get_producto()
		if producto is None:
			return redirect(self.success_url)
		else:
			return super(ProductoLogCreateView, self).get(request, *args, **kwargs)

	def get_producto(self):
		pk = self.request.GET.get('pk') or self.kwargs.get('pk') or None
		try:
			producto = Producto.objects.get(pk=pk)
		except Producto.DoesNotExist:
			producto = None			
		return producto
		
