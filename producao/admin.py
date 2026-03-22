from django.contrib import admin
from .models import Comanda, ItemComanda

class ItemComandaInline(admin.TabularInline):
    model = ItemComanda
    extra = 1

@admin.register(Comanda)
class ComandaAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente', 'status', 'data_entrega_prevista', 'valor_total')
    list_filter = ('status', 'data_entrega_prevista')
    search_fields = ('cliente__nome_completo', 'cliente__cpf')
    inlines = [ItemComandaInline]
    readonly_fields = ('data_entrada',)