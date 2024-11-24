from django.urls import path
from . import views

app_name = 'carteira'

urlpatterns = [
    # Removemos 'carteira/' do início
    path('', views.carteira_view, name='carteira'),
    path('graficos/', views.graficos_view, name='graficos'),
]
