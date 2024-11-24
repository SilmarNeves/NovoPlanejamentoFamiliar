import sqlite3
import pandas as pd
import numpy as np

import sqlite3
import pandas as pd
import numpy as np

def calcular_posicao_portfolio(df, asset_type):
    df_asset = df[df['Operacao'].str.contains(asset_type, case=False)]
    df_asset = df_asset.sort_values(by='Data')

    asset_info = {}

    for _, row in df_asset.iterrows():
        date = row['Data']
        asset = row['Ativo']
        quantity = row['Quantidade'] if 'COMPRA' in row['Operacao'] else -row['Quantidade']
        price = row['Preço']

        if 'AÇÃO' in row['Operacao']:
            asset_type = 'Ação'
        elif 'FII' in row['Operacao']:
            asset_type = 'FII'
        elif 'ETF' in row['Operacao']:
            asset_type = 'ETF'
        else:
            asset_type = 'Desconhecido'

        if asset not in asset_info:
            asset_info[asset] = {
                'records': [],
                'cum_shares': 0,
                'avg_price_weight': np.nan,
                'type': asset_type,
            }

        asset_info[asset]['records'].append({
            'date': date,
            'quantity': quantity,
            'price': price,
        })

    assets = []
    asset_types = []
    avg_prices = []
    total_quantities = []

    for asset, info in asset_info.items():
        records = info['records']

        position_shares = 0
        shares_cost = 0
        avg_price_weight = np.nan

        for record in records:
            position_shares += record['quantity']
            shares_cost += record['price'] * record['quantity']

            if position_shares == 0:
                avg_price_weight = 0
            elif np.isnan(avg_price_weight):
                avg_price_weight = record['price']
            elif record['quantity'] < 0:
                pass
            else:
                avg_price_weight = (avg_price_weight * info['cum_shares'] + record['price'] * record['quantity']) / position_shares

            info['cum_shares'] = position_shares
            info['avg_price_weight'] = avg_price_weight

        if position_shares > 0:
            assets.append(asset)
            asset_types.append(info['type'])
            avg_prices.append(round(avg_price_weight, 2))  # Arredondar o preço médio
            total_quantities.append(position_shares)

    df_result = pd.DataFrame({
        'Ativo': assets,
        'Tipo': asset_types,
        'Preço Médio': avg_prices,
        'Quantidade': total_quantities,
    })

    return df_result
def criar_tabelas_no_banco(database_path):
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    tabelas_nomes = {
        "portfolio_consolidadas": "Carteira Consolidadas",
        "portfolio_silmar": "Carteira Silmar",
        "portfolio_monica": "Carteira Mônica"
    }

    for tabela_nome in tabelas_nomes.keys():
        cursor.execute(f'DROP TABLE IF EXISTS {tabela_nome}')
        cursor.execute(f'''CREATE TABLE {tabela_nome} 
                    (Ativo TEXT, Tipo TEXT, Quantidade INTEGER, "Preço Médio" REAL, "Preço Atual" REAL, "Preço Anterior" REAL, 
                     "Ganho/Perda Hoje %" REAL,  "Ganho/Perda Hoje R$" REAL, "Variação Total %" REAL, "Patrimônio Atual" REAL,"% Ativo" REAL, "% Carteira" REAL)''')

    conn.commit()
    conn.close()

def salvar_portfolio_no_banco(df_result, database_path, table_name):
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    for _, row in df_result.iterrows():
        cursor.execute(f'''
            INSERT INTO {table_name} (Ativo, Tipo, Quantidade, "Preço Médio")
            VALUES (?, ?, ?, ?)
        ''', (row['Ativo'], row['Tipo'], row['Quantidade'], round(row['Preço Médio'], 2)))

    conn.commit()
    conn.close()


def gerar_portfolios():
    database_path = r'C:\Users\Silmar Moreno\Desktop\Django-main\db.sqlite3'
    criar_tabelas_no_banco(database_path)
    conn = sqlite3.connect(database_path)

    tabelas_nomes = {
        "transacoes_consolidadas": "portfolio_consolidadas",
        "transacoes_silmar": "portfolio_silmar",
        "transacoes_monica": "portfolio_monica"
    }

    for tabela_selecionada_bd, tabela_selecionada in tabelas_nomes.items():
        print(f"Gerando a tabela de portfolio para a {tabela_selecionada_bd}...")
        query = f"SELECT * FROM {tabela_selecionada_bd}"
        df = pd.read_sql_query(query, conn)

        df_actions = calcular_posicao_portfolio(df, 'COMPRA AÇÃO|VENDA AÇÃO|COMPRA FII|VENDA FII|COMPRA ETF|VENDA ETF')

        salvar_portfolio_no_banco(df_actions, database_path, tabela_selecionada)

    conn.close()

if __name__ == "__main__":
    gerar_portfolios()
