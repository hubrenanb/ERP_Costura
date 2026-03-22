from django.contrib import admin
from .models import Usuario, Cliente, Empresa

@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    # Exibe o ID e o Nome Fantasia direto na listagem para facilitar a gestão
    list_display = ('id', 'nome_fantasia')
    search_fields = ('nome_fantasia',)

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    # Adicionado 'empresa' para visualização rápida do vínculo Multi-tenant
    list_display = ('username', 'tipo', 'empresa', 'is_staff')
    list_filter = ('tipo', 'empresa')

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nome_completo', 'cpf', 'telefone', 'cidade', 'ativo') 
    search_fields = ('nome_completo', 'cpf')
    list_filter = ('ativo', 'cidade', 'empresa')