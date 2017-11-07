from django.conf.urls import url
from .views import *

urlpatterns = [
	url(r'^categorias/$', CategoriaListView.as_view(), name='categorias'),    
	url(r'^categoria/crear/$', CategoriaCreateView.as_view(), name='crear_categoria'),    	
	# url(r'^product/(?P<pk>\d+)/$', ProductDetailView.as_view(), name='detail_product'),    
]