from django.urls import path
from .views import carteira_view, graficos_view

app_name = 'carteira'

urlpatterns = [
    path('', carteira_view, name='carteira'),
    path('graficos/', graficos_view, name='carteira_graficos'),
]