# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig


class RequisicionesConfig(AppConfig):
    name = 'requisiciones'

    def ready(self):		
		import notificaciones.signals
