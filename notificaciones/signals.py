# -*- coding: utf-8 -*-
from notificaciones.middleware import RequestMiddleware
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType
from autenticacion.models import Perfil
from .models import Notificacion

@receiver(post_save)
def generar_notificacion(sender, instance, created, raw, update_fields, **kwargs):
    #Lista de los modelos que se requienran que escuche
    list_of_models = ['Pedido',]
    model_name = sender.__name__
    if model_name not in list_of_models:
        return

    if instance.estado == 1 or instance.estado==10:
        return

    user = get_user()
    if instance.estado == 2:
        mensaje = '%s ha generado un pedido.'
    elif instance.estado == 3:
        mensaje = '%s esta procesando tu pedido.'
    elif instance.estado == 4:
        mensaje = '%s ha negado tu pedido.'
    elif instance.estado == 5:
        mensaje = '%s ha entregado tu pedido.'
    else:
        mensaje = None
        
    mensaje = mensaje % user.get_full_name() if mensaje is not None else ''

    ctype = ContentType.objects.get_for_model(instance)

    if instance.estado == 2:    
        perfiles = Perfil.objects.filter(gestiona_pedidos=True)    
        for perfil in perfiles:
            Notificacion.objects.create(
                remitente=user,
                receptor=perfil.usuario,
                mensaje= mensaje, 
                id_objecto= instance.id,
                tipo_contenido= ctype,            
            )
    else:
        Notificacion.objects.create(
            remitente=user,
            receptor=instance.usuario,
            mensaje= mensaje, 
            id_objecto= instance.id,
            tipo_contenido= ctype,            
        )

@receiver(post_delete)
def notification_delete_log(sender, instance, **kwargs):
    #Lista de los modelos que se requienran que escuche  
    list_of_models = ['Friendship', 'Guest']
    if sender.__name__ not in list_of_models:
        return
    #user = get_user() 
    instance.delete_notification()

def get_user():
    thread_local = RequestMiddleware.thread_local
    if hasattr(thread_local, 'user'):
        user = thread_local.user
    else:
        user = None
    return user