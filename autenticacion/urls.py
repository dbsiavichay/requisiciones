from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required

urlpatterns = [	
    url(r'^ingresar/$', auth_views.LoginView.as_view(template_name='autenticacion/ingresar.html'), name='ingresar'),
    url(r'^salir/$', login_required(auth_views.logout_then_login), name='salir'),
    #url(r'^registro/$', UsuarioCreateView.as_view(), name='registro'),
    
    #url(r'^user/profile/$', login_required(UserProfileView.as_view()), name='user_profile'),
    #url(r'^user/change-avatar/$', change_user_avatar),
]
