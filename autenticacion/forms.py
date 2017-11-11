#-*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .utils import validar_cedula
from .models import Perfil

class CustomUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = 'Número de cédula'
        self.fields['username'].help_text = 'Unicamente digitos, sin guión. 10 caracteres.'

    def clean_username(self):                
        cedula = self.data.get('username')
        valido, mensaje = validar_cedula(cedula)

        if valido:
            return cedula        
        raise forms.ValidationError(mensaje)
