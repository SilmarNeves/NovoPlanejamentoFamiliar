from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

app_name = 'autenticacao'

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='autenticacao:login'), name='logout'),
]