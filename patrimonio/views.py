from django.shortcuts import render
from django.db import connection
import pandas as pd
from django.contrib.auth.decorators import login_required

@login_required
def get_patrimonio_context(request):
    carteiras = {
        'transacoes_consolidadas': 'Consolidada',
        'transacoes_silmar': 'Silmar',
        'transacoes_monica': 'Monica'
    }
    
    carteira_selecionada = request.GET.get('carteira', 'transacoes_consolidadas')
    
    query_movimentacoes = f"""
        SELECT 
            strftime('%Y-%m', Data) as AnoMes,
            SUM(CASE WHEN Operacao LIKE '%COMPRA%' THEN Quantidade * Preço ELSE 0 END) as Total_Compras,
            SUM(CASE WHEN Operacao LIKE '%VENDA%' THEN Quantidade * Preço ELSE 0 END) as Total_Vendas
        FROM {carteira_selecionada}
        GROUP BY strftime('%Y-%m', Data)
        ORDER BY AnoMes
    """
    
    query_patrimonio = f"""
        SELECT 
            SUM("Patrimônio Atual") as Patrimonio_Total
        FROM {carteira_selecionada.replace('transacoes', 'portfolio')}
    """
    
    with connection.cursor() as cursor:
        cursor.execute(query_movimentacoes)
        dados_movimentacoes = cursor.fetchall()
        
        cursor.execute(query_patrimonio)
        dados_patrimonio = cursor.fetchone()
    
    df_mov = pd.DataFrame(dados_movimentacoes, columns=['AnoMes', 'Total_Compras', 'Total_Vendas'])
    df_mov['Aportes'] = df_mov['Total_Compras'] - df_mov['Total_Vendas']
    
    return {
        'carteiras': carteiras,
        'carteira_selecionada': carteira_selecionada,
        'patrimonio_total': dados_patrimonio[0] if dados_patrimonio else 0,
        'total_aportes': df_mov['Aportes'].sum(),
        'evolucao_mensal': {
            'periodos': df_mov['AnoMes'].tolist(),
            'valores': df_mov['Aportes'].cumsum().tolist()
        }
    }

@login_required
def patrimonio_view(request):
    context = get_patrimonio_context(request)
    return render(request, 'patrimonio/patrimonio.html', context)
