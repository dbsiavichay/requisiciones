# -*- coding: utf-8 -*-
from django.urls import reverse_lazy
from django.shortcuts import redirect

def gestiona_pedidos_required(function):
    def wrapper(request, *args, **kwargs):
    	next = request.path
    	user = request.user    	
    	if user.is_anonymous() and not user.is_authenticated():
    		url = '%s?next=%s' % (reverse_lazy('ingresar'), next)    		
    		return redirect(url)         
        if not user.perfil.gestiona_pedidos:
            return redirect('pedidos')
        else:
            return function(request, *args, **kwargs)
    return wrapper