from .models import Notificacion

def get_notificaciones(request):
	if request.user.is_anonymous:
		return []

	notificaciones = Notificacion.objects.filter(
		receptor=request.user, visto=False
	)
	
	return { 
		'notificaciones': notificaciones
	}