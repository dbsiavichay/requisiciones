from autenticacion.perms import gestiona_pedidos_required
from django.conf.urls import url
from .views import *

urlpatterns = [
	url(r'^categorias/$', gestiona_pedidos_required(CategoriaListView.as_view()), name='categorias'),    	
	url(r'^categoria/crear/$', gestiona_pedidos_required(CategoriaCreateView.as_view()), name='crear_categoria'),    	
	url(r'^categoria/(?P<pk>\d+)/editar/$', gestiona_pedidos_required(CategoriaUpdateView.as_view()), name='editar_categoria'),	
	url(r'^categoria/(?P<pk>\d+)/eliminar/$', gestiona_pedidos_required(CategoriaDeleteView.as_view()), name='eliminar_categoria'),

	url(r'^productos/$', gestiona_pedidos_required(ProductoListView.as_view()), name='productos'),    	
	url(r'^producto/crear/$', gestiona_pedidos_required(ProductoCreateView.as_view()), name='crear_producto'),    	
	url(r'^producto/(?P<pk>\d+)/editar/$', gestiona_pedidos_required(ProductoUpdateView.as_view()), name='editar_producto'),	
	url(r'^producto/(?P<pk>\d+)/eliminar/$', gestiona_pedidos_required(ProductoDeleteView.as_view()), name='eliminar_producto'),
]