from django.forms import ModelForm
from decimal import Decimal
from django.forms.models import inlineformset_factory
from .models import *

class PedidoForm(ModelForm):
    class Meta:
        model = Pedido
        fields = ('estado',)

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