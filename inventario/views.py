# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from pure_pagination import PaginationMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from .models import *

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