from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from autenticacion.perms import gestiona_pedidos_required
from .views import *

urlpatterns = [
	url(r'^pedidos/$', login_required(PedidoListView.as_view()), name='pedidos'),    	
	url(r'^pedido/crear/$', login_required(PedidoCreateView.as_view()), name='crear_pedido'),    	
	url(r'^pedido/(?P<pk>\d+)/editar/$', login_required(PedidoUpdateView.as_view()), name='editar_pedido'),		
	url(r'^pedido/(?P<pk>\d+)/$', login_required(PedidoDetailView.as_view()), name='ver_pedido'),		

	url(r'^pedido/(?P<pk>\d+)/cancelar/$', login_required(CancelarPedidoUpdateView.as_view()), name='cancelar_pedido'),		
	url(r'^pedido/(?P<pk>\d+)/procesar/$', gestiona_pedidos_required(ProcesarPedidoUpdateView.as_view()), name='procesar_pedido'),		
	url(r'^pedido/(?P<pk>\d+)/negar/$', gestiona_pedidos_required(NegarPedidoUpdateView.as_view()), name='negar_pedido'),		
	url(r'^pedido/(?P<pk>\d+)/entregar/$', gestiona_pedidos_required(EntregarPedidoUpdateView.as_view()), name='entregar_pedido'),		
]