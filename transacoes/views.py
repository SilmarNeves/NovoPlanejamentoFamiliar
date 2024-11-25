from django.shortcuts import render
from django.db import connection
import pandas as pd
from django.contrib.auth.decorators import login_required


@login_required
def get_transacoes_context(request):
    tabelas_nomes = {

        'transacoes_consolidadas': 'Consolidada',
        'transacoes_silmar': 'Silmar',
        'transacoes_monica': 'Monica'
    }

    tabela_selecionada = request.GET.get('tabela', 'transacoes_consolidadas')
    
    if tabela_selecionada not in tabelas_nomes:
        tabela_selecionada = 'transacoes_consolidadas'
    
    dados_por_tipo = {}
    columns = ['Data', 'Operação', 'Ativo', 'Quantidade', 'Preço']
    
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT Data, Operacao, Ativo, Quantidade, Preço FROM {tabela_selecionada} ORDER BY Data DESC")
        dados = cursor.fetchall()
    
    table_data = [
        [
            dado[0].strftime('%d-%m-%Y'),  # Data formatada
            dado[1],                        # Operação
            dado[2],                        # Ativo
            f"{dado[3]:.0f}",              # Quantidade
            f"R$ {dado[4]:.2f}"            # Preço
        ] for dado in dados
    ]

    grid_context = {
        'title': 'Transações',
        'columns': columns,
        'table_data': table_data
    }
    
    dados_por_tipo['Transações'] = grid_context


    return {
        'tabelas_nomes': tabelas_nomes,
        'tabela_selecionada': tabela_selecionada,
        'dados_por_tipo': dados_por_tipo
    }



@login_required
def transacoes_view(request):
    context = get_transacoes_context(request)
    return render(request, 'transacoes/transacoes.html', context)