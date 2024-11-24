from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('atualizar-sistema/', views.atualizar_sistema, name='atualizar_sistema'),
]
