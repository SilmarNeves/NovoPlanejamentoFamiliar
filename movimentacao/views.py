from django.shortcuts import render
from django.db import connection
from django.contrib.auth.decorators import login_required
import pandas as pd
from django.contrib.auth.decorators import login_required

@login_required
def get_movimentacao_context(request):
    tabelas_nomes = {
        'transacoes_consolidadas': 'Consolidada',
        'transacoes_silmar': 'Silmar',
        'transacoes_monica': 'Monica'
    }
    
    tabela_selecionada = request.GET.get('tabela', 'transacoes_consolidadas')
    periodo = request.GET.get('periodo')
    
    query = f"""
        SELECT 
            Data, 
            Operacao, 
            Ativo, 
            Quantidade, 
            Preço
        FROM {tabela_selecionada}
        WHERE 1=1
    """
    
    if periodo:
        query += f" AND strftime('%Y-%m', Data) = '{periodo}'"
    
    with connection.cursor() as cursor:
        cursor.execute(query)
        dados = cursor.fetchall()
    
    df = pd.DataFrame(dados, columns=['Data', 'Operacao', 'Ativo', 'Quantidade', 'Preço'])
    
    if not df.empty:
        df['Data'] = pd.to_datetime(df['Data'])
        df['AnoMes'] = df['Data'].dt.strftime('%Y-%m')
        df['ValorTotal'] = df['Quantidade'] * df['Preço']
        
        meses_unicos = sorted(df['AnoMes'].unique())
        movimentacao = pd.DataFrame(index=meses_unicos)
        
        movimentacao['Total_de_Compras'] = df[df['Operacao'].str.contains('COMPRA')].groupby('AnoMes')['ValorTotal'].sum()
        movimentacao['Total_de_Vendas'] = df[df['Operacao'].str.contains('VENDA')].groupby('AnoMes')['ValorTotal'].sum()
        movimentacao = movimentacao.fillna(0)
        
        movimentacao['Aportes'] = movimentacao['Total_de_Compras'] - movimentacao['Total_de_Vendas']
        
        movimentacao = movimentacao.reset_index()
        movimentacao.columns = ['AnoMes', 'Total_de_Compras', 'Total_de_Vendas', 'Aportes']
        
        # Mantenha a ordenação descendente para a tabela
        movimentacao = movimentacao.sort_values('AnoMes', ascending=False)

        # Crie uma cópia ordenada ascendente para o gráfico
        movimentacao_grafico = movimentacao.sort_values('AnoMes', ascending=True)
        
        totais = {
            'total_compras': movimentacao['Total_de_Compras'].sum(),
            'total_vendas': movimentacao['Total_de_Vendas'].sum(),
            'total_aportes': movimentacao['Aportes'].sum()
        }
    else:
        movimentacao = []
        movimentacao_grafico = []
        totais = {
            'total_compras': 0,
            'total_vendas': 0,
            'total_aportes': 0
        }

    context = {
        'tabelas_nomes': tabelas_nomes,
        'tabela_selecionada': tabela_selecionada,
        'movimentacao': movimentacao.to_dict('records') if isinstance(movimentacao, pd.DataFrame) else [],
        'movimentacao_grafico': movimentacao_grafico.to_dict('records') if isinstance(movimentacao_grafico, pd.DataFrame) else [],
        'totais': totais,
        'periodo_selecionado': periodo
    }

     # Cálculos para os novos cards
    if not df.empty:
        df['Data'] = pd.to_datetime(df['Data'])
        hoje = pd.Timestamp.now()
        
        # Aportes por período
        aportes_info = {
            'mes_atual': movimentacao.iloc[0]['Aportes'] if not movimentacao.empty else 0,
            'ultimos_6_meses': movimentacao.head(6)['Aportes'].sum(),
            'ultimos_12_meses': movimentacao.head(12)['Aportes'].sum(),
            'media_6_meses': movimentacao.head(6)['Aportes'].mean(),
            'media_12_meses': movimentacao.head(12)['Aportes'].mean(),
            'total_geral': movimentacao['Aportes'].sum()
        }
    else:
        aportes_info = {
            'mes_atual': 0,
            'ultimos_6_meses': 0,
            'ultimos_12_meses': 0,
            'media_6_meses': 0,
            'media_12_meses': 0,
            'total_geral': 0
        }

    context['aportes_info'] = aportes_info
    return context
    
    return context

@login_required
def movimentacao_view(request):
    context = get_movimentacao_context(request)
    return render(request, 'movimentacao/movimentacao.html', context)
