from django import forms
from django.forms import ModelForm, ValidationError
from decimal import Decimal
from django.forms.models import inlineformset_factory
from .models import *

class PedidoForm(ModelForm):
    class Meta:
        model = Pedido
        fields = ('nota','lugar','estado',)
        widgets = {
            'nota': forms.Textarea(attrs={'cols': 40, 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super(PedidoForm, self).__init__(*args, **kwargs)
        self.fields['estado'].required = False

class LineaPedidoForm(ModelForm):
    class Meta:
        model = LineaPedido
        fields = '__all__'

LineaPedidoInlineFormSet = inlineformset_factory(
    Pedido, LineaPedido, form=LineaPedidoForm, extra = 2, min_num = 1
)

class EntregarLineaPedidoForm(ModelForm):
    class Meta:
        model = LineaPedido
        fields = ('cantidad_recibida',)    

    def __init__(self, *args, **kwargs):
        super(EntregarLineaPedidoForm, self).__init__(*args, **kwargs)
        self.fields['cantidad_recibida'].required = True        

    def clean_cantidad_recibida(self):         
        cantidad_recibida = self.cleaned_data.get('cantidad_recibida')
        cantidad_pedida = self.instance.cantidad_pedida or None
        stock = self.instance.producto.stock or 0

        if cantidad_recibida and cantidad_recibida > stock:
            raise ValidationError('La cantidad a entregar no puede ser mayor al stock (%s).' % stock)                

        if cantidad_recibida and cantidad_recibida > cantidad_pedida:
            raise ValidationError('La cantidad a entregar no puede ser mayor a la cantidad pedida (%s).' % cantidad_pedida)
        
        return cantidad_recibida


EntregarLineaPedidoInlineFormSet = inlineformset_factory(
    Pedido, LineaPedido, form=EntregarLineaPedidoForm, extra = 0,
)