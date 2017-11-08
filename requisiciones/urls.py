from django.conf.urls import url
from .views import *

urlpatterns = [
	url(r'^pedidos/$', PedidoListView.as_view(), name='pedidos'),    	
	url(r'^pedido/crear/$', PedidoCreateView.as_view(), name='crear_pedido'),    	
	url(r'^pedido/(?P<pk>\d+)/editar/$', PedidoUpdateView.as_view(), name='editar_pedido'),		
]