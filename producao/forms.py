from django import forms
from django.forms import inlineformset_factory
from .models import Comanda, ItemComanda
from core.models import Cliente

class ComandaForm(forms.ModelForm):
    class Meta:
        model = Comanda
        fields = ['cliente', 'origem', 'data_entrega_prevista', 'observacoes']
        widgets = {
            'cliente': forms.Select(attrs={'class': 'form-select'}),
            'origem': forms.Select(attrs={'class': 'form-select'}),
            'data_entrega_prevista': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'observacoes': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        empresa = kwargs.pop('empresa', None)
        super().__init__(*args, **kwargs)
        if empresa:
            self.fields['cliente'].queryset = Cliente.objects.filter(empresa=empresa, ativo=True)

ItemComandaFormSet = inlineformset_factory(
    Comanda,
    ItemComanda,
    fields=['descricao_servico', 'tipo_servico', 'quantidade', 'preco_unitario'],
    extra=1,
    can_delete=True,
    widgets={
        'descricao_servico': forms.TextInput(attrs={'class': 'form-control'}),
        'tipo_servico': forms.Select(attrs={'class': 'form-select'}),
        'quantidade': forms.NumberInput(attrs={'class': 'form-control'}),
        'preco_unitario': forms.NumberInput(attrs={'class': 'form-control'}),
    }
)