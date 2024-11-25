"""
URL configuration for controle_financeiro project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.contrib.auth.views import LogoutView
from django.urls import path


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('autenticacao.urls', namespace='autenticacao')),
    path('', include('financeiro.urls')),
    path('carteira/', include('carteira.urls')),
    path('transacoes/', include('transacoes.urls')),
    path('atualizar_transacoes/', include('Atualizar_Transacoes.urls')),
    path('movimentacao/', include('movimentacao.urls')),
    path('cotacoes/', include('cotacoes.urls')),
    path('patrimonio/', include('patrimonio.urls')),
    path('', include('dashboard.urls')),
]