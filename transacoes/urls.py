from django.urls import path
from . import views

urlpatterns = [
    path('', views.transacoes_view, name='transacoes_acoes'),
]
