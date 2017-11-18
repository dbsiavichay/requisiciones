# -*- coding: utf-8 -*-
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import ProductoLog

@receiver(post_save, sender=ProductoLog)
def afectar_stock(sender, instance, created, raw, update_fields, **kwargs):    
    if created:
		producto = instance.producto    	
		producto.stock = producto.stock + instance.cantidad if producto.stock else instance.cantidad
		producto.save()