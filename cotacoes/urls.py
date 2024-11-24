from django.urls import path
from . import views

urlpatterns = [
    path('', views.atualizar_cotacao_view, name='atualizacao'),
    path('atualizar-cotacao/', views.atualizar_cotacao_view, name='atualizar_cotacao'),
]
