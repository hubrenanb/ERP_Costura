from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, Cliente, Empresa

@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome_fantasia')
    search_fields = ('nome_fantasia',)

@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    # Usa a classe UserAdmin para garantir a criptografia da senha
    model = Usuario
    list_display = ('email', 'username', 'tipo', 'empresa', 'is_staff')
    list_filter = ('tipo', 'empresa', 'is_staff', 'is_active')
    
    # Adiciona os campos customizados na tela de edição do Admin
    fieldsets = UserAdmin.fieldsets + (
        ('Informações da Ckaizen', {'fields': ('empresa', 'tipo', 'telefone')}),
    )
    
    # Adiciona os campos customizados na tela de criação do Admin
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Informações da Ckaizen', {'fields': ('email', 'empresa', 'tipo', 'telefone')}),
    )

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nome_completo', 'cpf', 'telefone', 'cidade', 'ativo') 
    search_fields = ('nome_completo', 'cpf')
    list_filter = ('ativo', 'cidade', 'empresa')