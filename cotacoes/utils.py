
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
from django.db import connection
import concurrent.futures
from django.core.cache import cache
import logging

logger = logging.getLogger(__name__)

def get_ultimo_dia_util():
    hoje = datetime.today().date()
    
    # Se for domingo, pega sexta (22/11)
    if hoje.weekday() == 6:
        return hoje - timedelta(days=2)
    # Se for sábado, pega sexta
    elif hoje.weekday() == 5:
        return hoje - timedelta(days=1)
    # Se for segunda, pega sexta
    elif hoje.weekday() == 0:
        return hoje - timedelta(days=3)
    # Outros dias, pega o dia anterior
    else:
        return hoje - timedelta(days=1)

def get_dia_util_anterior():
    ultimo_dia_util = get_ultimo_dia_util()
    
    # Sempre pega o dia útil anterior ao último
    return ultimo_dia_util - timedelta(days=1)

def obter_preco(ativo, data=None):
    try:
        ticker_symbol = f"{ativo}.SA"
        ticker = yf.Ticker(ticker_symbol)
        
        if data:
            hist = ticker.history(start=data, end=data + timedelta(days=1))
            logger.info(f"Buscando preço histórico para {ativo} na data {data}")
        else:
            hist = ticker.history(period="1d")
            logger.info(f"Buscando preço atual para {ativo}")
        
        if not hist.empty:
            preco = round(hist['Close'][0], 2)
            logger.info(f"Preço obtido do yfinance para {ativo}: {preco} - Data: {data if data else 'atual'}")
            return preco
            
        logger.warning(f"Nenhum preço encontrado para {ativo} na data {data if data else 'atual'}")
        return 0.0
        
    except Exception as e:
        logger.error(f"Erro ao buscar preço para {ativo}: {str(e)}")
        return 0.0

def buscar_precos(ativos):
    ativos_precos = {}
    ativos_precos_anteriores = {}
    ultimo_dia_util = get_ultimo_dia_util()
    dia_util_anterior = get_dia_util_anterior()

    logger.info(f"""
    Iniciando busca de preços:
    - Último dia útil: {ultimo_dia_util}
    - Dia útil anterior: {dia_util_anterior}
    - Ativos a consultar: {ativos}
    """)

    def obter_precos(ativo):
        preco_atual = obter_preco(ativo, data=ultimo_dia_util)
        preco_anterior = obter_preco(ativo, data=dia_util_anterior)
        
        logger.info(f"""
        Resultado para {ativo}:
        - Data Atual ({ultimo_dia_util}): R$ {preco_atual}
        - Data Anterior ({dia_util_anterior}): R$ {preco_anterior}
        - Variação: {((preco_atual - preco_anterior) / preco_anterior * 100):.2f}%
        """)
        
        return ativo, preco_atual, preco_anterior

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        results = executor.map(obter_precos, ativos)
    
    for ativo, preco_atual, preco_anterior in results:
        if preco_atual:
            ativos_precos[ativo] = preco_atual
        if preco_anterior:
            ativos_precos_anteriores[ativo] = preco_anterior
    
    return ativos_precos, ativos_precos_anteriores

def atualizar_cotacao_otimizado():
    tabelas_portfolio = ["portfolio_silmar", "portfolio_monica", "portfolio_consolidadas"]

    with connection.cursor() as cursor:
        for tabela in tabelas_portfolio:
            cursor.execute(f"SELECT Ativo, Quantidade, Tipo FROM {tabela}")
            ativos_info = cursor.fetchall()

            ativos_precos, ativos_precos_anteriores = buscar_precos([info[0] for info in ativos_info])

            patrimonio_por_tipo = {}
            total_geral = 0

            for ativo, quantidade, tipo in ativos_info:
                preco_atual = ativos_precos.get(ativo)
                if preco_atual is not None:
                    patrimonio_atual = round(quantidade * preco_atual, 2)
                    if tipo not in patrimonio_por_tipo:
                        patrimonio_por_tipo[tipo] = 0
                    patrimonio_por_tipo[tipo] += patrimonio_atual
                    total_geral += patrimonio_atual

            rows_to_update = []
            for ativo, quantidade, tipo in ativos_info:
                preco_atual = ativos_precos.get(ativo)
                preco_anterior = ativos_precos_anteriores.get(ativo)
                if preco_atual is not None and preco_anterior is not None:
                    patrimonio_atual = round(quantidade * preco_atual, 2)
                    ganho_perda = round(((preco_atual - preco_anterior) / preco_anterior) * 100, 2)
                    diferenca = round((preco_atual - preco_anterior) * quantidade, 2)
                    
                    percentual_ativo = round((patrimonio_atual / patrimonio_por_tipo[tipo]) * 100, 2) if patrimonio_por_tipo[tipo] else 0
                    percentual_carteira = round((patrimonio_atual / total_geral) * 100, 2) if total_geral else 0

                    cursor.execute(f"SELECT \"Preço Médio\" FROM {tabela} WHERE Ativo = %s", (ativo,))
                    preco_medio = cursor.fetchone()[0]
                    
                    variacao_total = round(((preco_atual - preco_medio) / preco_medio) * 100, 2)

                    rows_to_update.append((preco_atual, preco_anterior, ganho_perda, diferenca, patrimonio_atual, percentual_ativo, percentual_carteira, variacao_total, ativo))

            cursor.executemany(f"""
                UPDATE {tabela}
                SET "Preço Atual" = %s, "Preço Anterior" = %s, "Ganho/Perda Hoje %" = %s, "Ganho/Perda Hoje R$" = %s, 
                    "Patrimônio Atual" = %s, "% Ativo" = %s, "% Carteira" = %s, "Variação Total %" = %s
                WHERE Ativo = %s
            """, rows_to_update)

        connection.commit()
