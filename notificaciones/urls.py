from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from .views import *

urlpatterns = [	    
    url(r'^$', login_required(NotificacionListView.as_view()), name='notificaciones'),    
    url(r'^notificacion/(?P<pk>\d+)/$', login_required(NotificationDetailView.as_view()), name='ver_notificacion'),
]