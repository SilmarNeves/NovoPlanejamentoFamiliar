from django.shortcuts import render
from carteira.views import get_carteira_context
from patrimonio.views import get_patrimonio_context
from movimentacao.views import get_movimentacao_context
from transacoes.views import get_transacoes_context

def index(request):
      context = {
          **get_carteira_context(request),
          **get_patrimonio_context(request),
          **get_movimentacao_context(request),
          **get_transacoes_context(request),
      }
      return render(request, 'dashboard/index.html', context)
