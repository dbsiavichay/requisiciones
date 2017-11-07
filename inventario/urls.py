from django.conf.urls import url
from .views import *

urlpatterns = [
	url(r'^categorias/$', CategoriaListView.as_view(), name='categorias'),    	
	url(r'^categoria/crear/$', CategoriaCreateView.as_view(), name='crear_categoria'),    	
	url(r'^categoria/(?P<pk>\d+)/editar/$', CategoriaUpdateView.as_view(), name='editar_categoria'),	
	url(r'^categoria/(?P<pk>\d+)/eliminar/$', CategoriaDeleteView.as_view(), name='eliminar_categoria'),

	url(r'^productos/$', ProductoListView.as_view(), name='productos'),    	
	url(r'^producto/crear/$', ProductoCreateView.as_view(), name='crear_producto'),    	
	url(r'^producto/(?P<pk>\d+)/editar/$', ProductoUpdateView.as_view(), name='editar_producto'),	
	url(r'^producto/(?P<pk>\d+)/eliminar/$', ProductoDeleteView.as_view(), name='eliminar_producto'),
]