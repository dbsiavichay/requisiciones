from django.conf.urls import url
from .views import *

urlpatterns = [
	url(r'^pedidos/$', PedidoListView.as_view(), name='pedidos'),    	
	url(r'^pedido/crear/$', PedidoCreateView.as_view(), name='crear_pedido'),    	
	url(r'^pedido/(?P<pk>\d+)/editar/$', PedidoUpdateView.as_view(), name='editar_pedido'),		
	url(r'^pedido/(?P<pk>\d+)/cancelar/$', CancelarPedidoUpdateView.as_view(), name='cancelar_pedido'),		
	url(r'^pedido/(?P<pk>\d+)/$', PedidoDetailView.as_view(), name='ver_pedido'),		
]