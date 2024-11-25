from django.contrib.auth.views import LoginView, PasswordResetView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect

class LoginView(LoginView):
    template_name = 'autenticacao/login.html'
    success_url = reverse_lazy('index')
    
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('index')
        return super().get(request, *args, **kwargs)

