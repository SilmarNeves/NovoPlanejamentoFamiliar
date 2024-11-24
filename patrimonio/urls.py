from django.urls import path
from . import views

app_name = 'patrimonio'

urlpatterns = [
    path('', views.patrimonio_view, name='patrimonio'),
]
