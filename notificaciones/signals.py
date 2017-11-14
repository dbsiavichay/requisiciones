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

    if instance.estado != 2:
        return        
    user = get_user()

    #instance.save_notification(user.profile)
    ctype = ContentType.objects.get_for_model(instance)
    perfiles = Perfil.objects.filter(gestiona_pedidos=True)
    mensaje = 'Ha generado un pedido.'

    for perfil in perfiles:
        Notificacion.objects.create(
            remitente=user,
            receptor=perfil.usuario,
            mensaje= mensaje, 
            id_objecto= instance.id,
            tipo_contenido= ctype,            
        )
    # if created:
    # elif not raw: #Cuando edita un objeto
    #     instance.save_notification(user.profile)

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