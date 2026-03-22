from django.urls import path
from . import views

urlpatterns = [
    # Tela principal para lançar despesas de limpeza, materiais, etc.
    path('', views.listar_transacoes, name='listar_transacoes'),
    
    path('dashboard/', views.dashboard_financeiro, name='dashboard_financeiro'),
    path('pagamento/<int:comanda_id>/', views.registrar_pagamento, name='registrar_pagamento'),
    path('exportar/', views.exportar_relatorio_comandas, name='exportar_relatorio'),
]