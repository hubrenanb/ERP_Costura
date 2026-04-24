from django.urls import path
from . import views

urlpatterns = [
    path('comandas/', views.listar_comandas, name='listar_comandas'),
    path('comandas/nova/', views.nova_comanda, name='nova_comanda'),
    path('comandas/editar/<int:comanda_id>/', views.editar_comanda, name='editar_comanda'),
    path('comandas/status/<int:comanda_id>/', views.atualizar_status, name='atualizar_status'),
    path('comandas/imprimir/<int:comanda_id>/', views.imprimir_comanda, name='imprimir_comanda'),
    path('comandas/remover/<int:comanda_id>/', views.remover_comanda, name='remover_comanda'),
]