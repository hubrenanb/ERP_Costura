from django import forms
from django.forms import inlineformset_factory
from .models import Comanda, ItemComanda
from core.models import Cliente

class ComandaForm(forms.ModelForm):
    class Meta:
        model = Comanda
        fields = ['cliente', 'data_entrega_prevista', 'observacoes']
        widgets = {
            'data_entrega_prevista': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'observacoes': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'cliente': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        # Captura a empresa passada pela View
        empresa = kwargs.pop('empresa', None)
        super().__init__(*args, **kwargs)
        if empresa:
            # FILTRO CRÍTICO: Exibe apenas clientes da empresa do usuário logado
            self.fields['cliente'].queryset = Cliente.objects.filter(empresa=empresa, ativo=True)

ItemComandaFormSet = inlineformset_factory(
    Comanda,
    ItemComanda,
    fields=['descricao_servico', 'quantidade', 'preco_unitario'],
    extra=1,
    can_delete=True,
    widgets={
        'descricao_servico': forms.TextInput(attrs={'class': 'form-control'}),
        'quantidade': forms.NumberInput(attrs={'class': 'form-control'}),
        'preco_unitario': forms.NumberInput(attrs={'class': 'form-control'}),
    }
)