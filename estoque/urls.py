from django.urls import path
from . import views

urlpatterns = [
    path('', views.listar_estoque, name='listar_estoque'),
    path('cadastrar/', views.cadastrar_produto, name='cadastrar_produto'),
    path('movimentar/', views.movimentar_estoque, name='movimentar_estoque'),
]