#-*- coding: utf-8 -*-
import math

def validar_cedula(cedula=None):    
    if cedula is None:
        return (False, 'Este campo es requerido.')        
    if not cedula.isdigit:
        return (False, 'Ingrese una cédula válida.')        
    if len(cedula) != 10:
        return (False, 'La cédula debe contener 10 dígitos numéricos.')        

    total = 0
    coeficientes = (2,1,2,1,2,1,2,1,2,)
    
    verificador_recibido = int(cedula[9])
    for i, cf in enumerate(coeficientes):        
        mult = int(cedula[i]) * cf
        total = total + mult if mult <= 9 else total + ( mult - 9 )

    band = total%10    
    verificador_obtenido = total if total < 10 else 10 - band if band != 0  else band

    if verificador_recibido == verificador_obtenido:
        return (True, None)
    
    return (False, 'Ingrese una cédula válida.')