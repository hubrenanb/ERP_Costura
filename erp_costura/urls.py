"""
URL configuration for erp_costura project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Centraliza a autenticação (login/logout)
    path('contas/', include('django.contrib.auth.urls')),

    # Módulos com prefixos claros
    path('clientes/', include('core.urls')),
    path('estoque/', include('estoque.urls')),
    path('producao/', include('producao.urls')),
    path('financeiro/', include('financeiro.urls')),

    # Página inicial: Redireciona para a lista de comandas automaticamente
    path('', lambda request: redirect('listar_comandas')),
]