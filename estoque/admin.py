from django.contrib import admin
from .models import Produto, MovimentacaoEstoque

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'tipo', 'quantidade_atual', 'unidade_medida', 'estoque_minimo')
    list_filter = ('tipo',)
    search_fields = ('nome',)

@admin.register(MovimentacaoEstoque)
class MovimentacaoEstoqueAdmin(admin.ModelAdmin):
    list_display = ('produto', 'tipo', 'quantidade', 'data_movimento', 'comanda')
    list_filter = ('tipo', 'data_movimento')
    search_fields = ('produto__nome', 'comanda__id')