from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from autenticacion.perms import gestiona_pedidos_required
from .views import *

urlpatterns = [
	url(r'^lugares/$', gestiona_pedidos_required(LugarListView.as_view()), name='lugares'),    	
	url(r'^lugar/crear/$', gestiona_pedidos_required(LugarCreateView.as_view()), name='crear_lugar'),
	url(r'^lugar/(?P<pk>\d+)/editar/$', gestiona_pedidos_required(LugarUpdateView.as_view()), name='editar_lugar'),	
	url(r'^lugar/(?P<pk>\d+)/eliminar/$', gestiona_pedidos_required(LugarDeleteView.as_view()), name='eliminar_lugar'),    	

	url(r'^pedidos/$', login_required(PedidoListView.as_view()), name='pedidos'),    	
	url(r'^pedido/crear/$', login_required(PedidoCreateView.as_view()), name='crear_pedido'),    	
	url(r'^pedido/(?P<pk>\d+)/editar/$', login_required(PedidoUpdateView.as_view()), name='editar_pedido'),		
	url(r'^pedido/(?P<pk>\d+)/$', login_required(PedidoDetailView.as_view()), name='ver_pedido'),		

	url(r'^pedido/(?P<pk>\d+)/cancelar/$', login_required(CancelarPedidoUpdateView.as_view()), name='cancelar_pedido'),		
	url(r'^pedido/(?P<pk>\d+)/procesar/$', gestiona_pedidos_required(ProcesarPedidoUpdateView.as_view()), name='procesar_pedido'),		
	url(r'^pedido/(?P<pk>\d+)/negar/$', gestiona_pedidos_required(NegarPedidoUpdateView.as_view()), name='negar_pedido'),		
	url(r'^pedido/(?P<pk>\d+)/entregar/$', gestiona_pedidos_required(EntregarPedidoUpdateView.as_view()), name='entregar_pedido'),		
	url(r'^pedido/(?P<pk>\d+)/recibir/$', login_required(RecibirPedidoUpdateView.as_view()), name='recibir_pedido'),		

	url(r'^reporte/$', login_required(ReporteView.as_view()), name='reporte_pedido'),		
	url(r'^reporte/(?P<estado>\d+)/estado/$', login_required(pedido_por_estado_view)),		
]