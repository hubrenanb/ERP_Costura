from django.contrib import admin
from .models import Transacao

@admin.register(Transacao)
class TransacaoAdmin(admin.ModelAdmin):
    list_display = ('data_transacao', 'tipo', 'descricao', 'valor', 'metodo_pagamento')
    list_filter = ('tipo', 'metodo_pagamento', 'data_transacao')
    search_fields = ('descricao', 'comanda__id')