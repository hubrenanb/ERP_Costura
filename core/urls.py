from django.urls import path
from . import views

urlpatterns = [
    path('cadastrar/', views.cadastrar_cliente, name='cadastrar_cliente'),
    path('listar/', views.listar_clientes, name='listar_clientes'), # ESTA LINHA É A CHAVE
]