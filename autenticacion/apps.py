# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.apps import AppConfig


class AutenticacionConfig(AppConfig):
    name = 'autenticacion'
    verbose_name = 'Autenticación'

    def ready(self):		
		import autenticacion.signals