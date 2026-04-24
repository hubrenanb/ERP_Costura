from django.urls import path
from . import views

urlpatterns = [
    path('cadastrar/', views.cadastrar_cliente, name='cadastrar_cliente'),
    path('listar/', views.listar_clientes, name='listar_clientes'),
    path('editar/<uuid:cliente_id>/', views.editar_cliente, name='editar_cliente'),
    path('inativar/<uuid:cliente_id>/', views.inativar_cliente, name='inativar_cliente'),
]