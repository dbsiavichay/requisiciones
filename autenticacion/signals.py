# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Perfil

@receiver(post_save, sender=User)
def generar_perfil(sender, instance, created, raw, update_fields, **kwargs):    
    if created:
        Perfil.objects.create(usuario=instance)

    instance.perfil.save()