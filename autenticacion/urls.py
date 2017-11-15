from django.conf.urls import url
from django.urls import reverse_lazy
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from .views import *

urlpatterns = [	
    url(r'^ingresar/$', auth_views.LoginView.as_view(template_name='autenticacion/ingresar.html'), name='ingresar'),
    url(r'^salir/$', login_required(auth_views.logout_then_login), name='salir'),
    url(r'^perfil/(?P<username>[\w.@+-]+)/$', login_required(PerfilDetailView.as_view()), name='perfil'),
    url(
    	r'^cambiar-password/$', auth_views.password_change, 
    	{
    		'template_name': 'autenticacion/change-password.html',
    		'post_change_redirect': reverse_lazy('cambiar-password-done')
    	},
    	name ='cambiar-password'
    ), 
    url(
    	r'^cambiar-password-ok/$', auth_views.password_change_done, 
    	{
    		'template_name': 'autenticacion/change-password-done.html',
    	},
    	name='cambiar-password-done'
    ),  
]
