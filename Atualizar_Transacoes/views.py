from django.shortcuts import render
from django.http import HttpResponse
from .services.atualizar_transacoes import atualizar_transacoes
from .services.gerar_portfolios import gerar_portfolios

def index(request):
    return render(request, 'atualizar_transacoes/index.html')

def atualizar_sistema(request):
    atualizar_transacoes()
    gerar_portfolios()
    return HttpResponse("Sistema atualizado com sucesso!")
