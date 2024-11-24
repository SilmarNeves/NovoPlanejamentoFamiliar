
from django.shortcuts import render
from django.db import connection
from collections import defaultdict
from django.contrib.auth.decorators import login_required
import pandas as pd

def get_carteira_context(request):
    tabelas_nomes = {
        'transacoes_consolidadas': 'Consolidada',
        'transacoes_silmar': 'Silmar',
        'transacoes_monica': 'Monica'
    }
    
    tabela_selecionada = request.GET.get('tabela', 'transacoes_consolidadas')
    tabela_portfolio = tabela_selecionada.replace('transacoes', 'portfolio')
    
    query = f"""
        SELECT 
            Ativo,
            Tipo,
            Quantidade,
            "Preço Médio",
            "Preço Atual",
            "Ganho/Perda Hoje %",
            "Ganho/Perda Hoje R$",
            "Variação Total %",
            "Patrimônio Atual",
            "% Ativo",
            "% Carteira"
        FROM {tabela_portfolio}
    """
    
    with connection.cursor() as cursor:
        cursor.execute(query)
        dados = cursor.fetchall()
        
    columns = [
        'Nome',
        'Quantidade', 
        'Preço Médio',
        'Preço Atual',
        'Ganho/Perda Hoje %',
        'Ganho/Perda Hoje R$',
        'Variação Total %',
        'Patrimônio Atual',
        '% Ativo',
        '% Carteira'
    ]

    dados_por_tipo = {}
    totais = defaultdict(float)
    ativos_acoes = defaultdict(float)
    ativos_fiis = defaultdict(float)
    
    # Cálculo das variações ponderadas
    total_patrimonio_acao = 0
    total_variacao_ponderada_acao = 0
    total_patrimonio_fii = 0
    total_variacao_ponderada_fii = 0

    for tipo in ['Ação', 'FII']:
        table_data = []
        for ativo in dados:
            if ativo[1] == tipo:
                patrimonio_atual = ativo[8]  # Patrimônio Atual
                variacao_hoje = ativo[5]     # Ganho/Perda Hoje %
                
                if tipo == 'Ação':
                    total_patrimonio_acao += patrimonio_atual
                    total_variacao_ponderada_acao += (variacao_hoje * patrimonio_atual)
                    ativos_acoes[ativo[0]] = patrimonio_atual
                else:
                    total_patrimonio_fii += patrimonio_atual
                    total_variacao_ponderada_fii += (variacao_hoje * patrimonio_atual)
                    ativos_fiis[ativo[0]] = patrimonio_atual
                
                row = [
                    ativo[0],  # Nome
                    f"{ativo[2]:.0f}",  # Quantidade
                    f"R$ {ativo[3]:.2f}",  # Preço Médio
                    f"R$ {ativo[4]:.2f}",  # Preço Atual
                    f'<span class="{"text-success" if ativo[5] > 0 else "text-danger"}">{ativo[5]:.2f}%</span>',
                    f'<span class="{"text-success" if ativo[6] > 0 else "text-danger"}">R$ {ativo[6]:.2f}</span>',
                    f'<span class="{"text-success" if ativo[7] > 0 else "text-danger"}">{ativo[7]:.2f}%</span>',
                    f"R$ {patrimonio_atual:.2f}",
                    f"{ativo[9]:.2f}%",
                    f"{ativo[10]:.2f}%"
                ]
                table_data.append(row)
                totais[tipo] += patrimonio_atual

        dados_por_tipo[tipo] = {
            'title': f'Carteira - {tipo}',
            'columns': columns,
            'table_data': table_data
        }

    # Cálculo das variações finais
    variacao_acao = total_variacao_ponderada_acao / total_patrimonio_acao if total_patrimonio_acao else 0
    variacao_fii = total_variacao_ponderada_fii / total_patrimonio_fii if total_patrimonio_fii else 0
    
    patrimonio_total = total_patrimonio_acao + total_patrimonio_fii
    variacao_total = ((variacao_acao * total_patrimonio_acao) + 
                     (variacao_fii * total_patrimonio_fii)) / patrimonio_total if patrimonio_total else 0

    totais['Total Geral'] = patrimonio_total

    variacoes = {
        'FII': {
            'percentual': variacao_fii,
            'absoluta': total_patrimonio_fii * (variacao_fii/100)
        },
        'Ação': {
            'percentual': variacao_acao,
            'absoluta': total_patrimonio_acao * (variacao_acao/100)
        },
        'Total': {
            'percentual': variacao_total,
            'absoluta': patrimonio_total * (variacao_total/100)
        }
    }

    return {
        'tabelas_nomes': tabelas_nomes,
        'tabela_selecionada': tabela_selecionada,
        'dados_por_tipo': dados_por_tipo,
        'totais': dict(totais),
        'variacoes': variacoes,
        'grafico_tipos_labels': list(totais.keys())[:-1],
        'grafico_tipos_data': [totais[tipo] for tipo in list(totais.keys())[:-1]],
        'grafico_acoes_labels': list(ativos_acoes.keys()),
        'grafico_acoes_data': list(ativos_acoes.values()),
        'grafico_fiis_labels': list(ativos_fiis.keys()),
        'grafico_fiis_data': list(ativos_fiis.values())
    }

@login_required
def carteira_view(request):
    context = get_carteira_context(request)
    return render(request, 'carteira/carteira.html', context)

@login_required
def graficos_view(request):
    context = get_carteira_context(request)
    return render(request, 'carteira/graficos.html', context)
