from django.shortcuts import render
from django.http import HttpResponse
from .services.atualizar_transacoes import atualizar_transacoes
from .services.gerar_portfolios import gerar_portfolios

def index(request):
    return render(request, 'atualizar_transacoes/index.html')

def atualizar(request):
    atualizar_transacoes()
    return HttpResponse("Transações atualizadas com sucesso!")

def gerar(request):
    gerar_portfolios()
    return HttpResponse("Portfólios gerados com sucesso!")