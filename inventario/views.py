# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import *

class CategoriaListView(ListView):
	model = Categoria

class CategoriaCreateView(CreateView):
	model = Categoria
	fields = '__all__'
	success_url = reverse_lazy('categorias')
