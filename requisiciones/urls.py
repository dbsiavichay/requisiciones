from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from .views import *

urlpatterns = [
	url(r'^pedidos/$', login_required(PedidoListView.as_view()), name='pedidos'),    	
	url(r'^pedido/crear/$', login_required(PedidoCreateView.as_view()), name='crear_pedido'),    	
	url(r'^pedido/(?P<pk>\d+)/editar/$', login_required(PedidoUpdateView.as_view()), name='editar_pedido'),		
	url(r'^pedido/(?P<pk>\d+)/cancelar/$', login_required(CancelarPedidoUpdateView.as_view()), name='cancelar_pedido'),		
	url(r'^pedido/(?P<pk>\d+)/$', login_required(PedidoDetailView.as_view()), name='ver_pedido'),		
]