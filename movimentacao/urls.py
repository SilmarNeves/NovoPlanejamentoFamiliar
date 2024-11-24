from django.urls import path
from .views import movimentacao_view

urlpatterns = [
    path('', movimentacao_view, name='movimentacao'),
]
