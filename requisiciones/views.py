# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime
from django.http import HttpResponse
from django.db.models import Q
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from pure_pagination.mixins import PaginationMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, TemplateView
from inventario.models import ProductoLog
from django.contrib.auth.models import User
from .forms import *
from .models import *
from .reports import get_pedido_por_estado_pdf, get_pedido_por_rango_pdf, get_pedido_por_usuario_pdf

class LugarListView(PaginationMixin, ListView):
	paginate_by=10
	model = Lugar

class LugarCreateView(CreateView):
	model = Lugar
	fields = '__all__'
	success_url = reverse_lazy('lugares')

class LugarUpdateView(UpdateView):
	model = Lugar
	fields = '__all__'
	success_url = reverse_lazy('lugares')

class LugarDeleteView(DeleteView):
	model = Lugar
	success_url = reverse_lazy('lugares')

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
	formset_class = LineaPedidoInlineFormSet
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
		formset = self.formset_class(post_data, instance=self.object)
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

class CancelarPedidoUpdateView(UpdateView):
	model = Pedido
	fields = ()
	estado = 10
	success_url = reverse_lazy('pedidos')

	def post(self, request, *args, **kwargs):
		return redirect(self.get_success_url())

	def get(self, request, *args, **kwargs):
		self.object = self.get_object()
		if self.object.usuario != request.user:
			return redirect('pedidos')
		if self.object.estado > 2:
			return redirect('ver_pedido', self.object.id)			
		self.object.estado = self.estado
		self.object.save()
		return redirect('ver_pedido', self.object.id)

class ProcesarNegarBaseView(UpdateView):
	model = Pedido
	fields = ('nota',)
	success_url = reverse_lazy('pedidos')
	estado = 1

	def get(self, request, *args, **kwargs):
		return redirect(self.get_success_url())

	def form_valid(self, form):
		self.object = form.save(commit=False)
		self.object.estado = self.estado 
		self.object.save()
		return redirect('ver_pedido', self.object.id)

class ProcesarPedidoUpdateView(ProcesarNegarBaseView):
	estado = 3

	def post(self, request, *args, **kwargs):
		self.object = self.get_object()
		if self.object.estado != 2:
			return redirect('ver_pedido', self.object.id)
			
		return super(ProcesarNegarBaseView, self).post(request, *args, **kwargs)

class NegarPedidoUpdateView(ProcesarNegarBaseView):
	estado = 4

	def post(self, request, *args, **kwargs):
		self.object = self.get_object()
		if self.object.estado != 2 and self.object.estado != 3:
			return redirect('ver_pedido', self.object.id)
			
		return super(ProcesarNegarBaseView, self).post(request, *args, **kwargs)

class EntregarPedidoUpdateView(PedidoUpdateView):
	formset_class = EntregarLineaPedidoInlineFormSet
	template_name = 'requisiciones/pedido_entregar.html'

	def form_valid(self, form):		
		formset = self.get_lineapedido_formset()
		
		if formset.is_valid():						
			self.object = form.save(commit=False)
			self.object.estado = 5						
			self.object.save()

			for form in formset:
				form.save()
				ProductoLog.objects.create(
					tipo=2,
					producto = form.instance.producto,
					cantidad = form.cleaned_data['cantidad_recibida'] * -1,					
					pedido = form.instance.pedido.id
				)			

			return redirect(self.get_success_url())
		else:
			return self.form_invalid(form)	

	def get(self, request, *args, **kwargs):
		self.object = self.get_object()

		if self.object.usuario == request.user and not request.user.perfil.gestiona_pedidos:
			return redirect('ver_pedido', self.object.id)		

		if self.object.estado != 2 and self.object.estado != 3:
			return redirect('ver_pedido', self.object.id)

		return super(PedidoUpdateView, self).get(request, *args, **kwargs)

class RecibirPedidoUpdateView(UpdateView):
	model = Pedido
	fields = ()
	success_url = reverse_lazy('pedidos')
	estado = 6

	def get(self, request, *args, **kwargs):
		self.object = self.get_object()
		if self.object.usuario != request.user:
			if request.user.perfil.gestiona_pedidos:
				return redirect('ver_pedido', self.object.id)
			else:			
				return redirect('pedidos')
		if self.object.estado != 5:
			return redirect('ver_pedido', self.object.id)		
		
		self.object.estado = self.estado
		self.object.save()		
		return redirect('ver_pedido', self.object.id)

	def post(self, request, *args, **kwargs):
		return redirect(self.get_success_url())

class ReporteView(TemplateView):
	template_name = 'requisiciones/reporte.html'

	def get_context_data(self, **kwargs):
		context = super(ReporteView, self).get_context_data(**kwargs)
		context['estados'] = Pedido.ESTADO_CHOICES
		context['usuarios'] = User.objects.filter(is_active=True)

		return context

def pedido_por_estado_view(request, estado):    
	response = HttpResponse(content_type='application/pdf')
	response['Content-Disposition'] = 'inline; filename=reporte.pdf'
	
	pdf = get_pedido_por_estado_pdf(estado)

	response.write(pdf)
	return response

def pedido_por_rango_view(request, fecha_inicial, fecha_final):    
	response = HttpResponse(content_type='application/pdf')
	response['Content-Disposition'] = 'inline; filename=reporte.pdf'

	fecha1 = datetime.strptime(fecha_inicial, '%Y-%m-%d').date()	
	fecha2 = datetime.strptime(fecha_final, '%Y-%m-%d').date()	
	
	pdf = get_pedido_por_rango_pdf(fecha1, fecha2)

	response.write(pdf)
	return response

def pedido_por_usuario_view(request, usuario):    
	response = HttpResponse(content_type='application/pdf')
	response['Content-Disposition'] = 'inline; filename=reporte.pdf'
	
	user = User.objects.get(pk=usuario)
	pdf = get_pedido_por_usuario_pdf(user)

	response.write(pdf)
	return response