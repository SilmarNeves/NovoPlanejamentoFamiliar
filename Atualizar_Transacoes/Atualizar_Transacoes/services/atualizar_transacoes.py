import pandas as pd
import sqlite3

def atualizar_transacoes():
    origem_path1 = r"C:\Users\Silmar Moreno\Desktop\TRADERSPLAN-3.401 MONICA\TRADERS PLAN_3.45 PRO.xlsm"
    origem_path2 = r"C:\Users\Silmar Moreno\Desktop\TRADERSPLAN-3.401 SILMAR\TRADERS PLAN_3.45 PRO.xlsm"
    database_path = r'C:\Users\Silmar Moreno\Desktop\Django-main\db.sqlite3'

    # Função para ler e processar planilha
    def processar_planilha(path):
        df = pd.read_excel(path, sheet_name="OPERAÇÕES", usecols="A:G")
        df = df.iloc[1:]  # Excluindo a primeira linha
        df.columns = ['Data', 'Operacao', 'Ativo', 'Quantidade', 'Preço', 'Nota', 'Corretora']
        df['Data'] = pd.to_datetime(df['Data']).dt.date
        return df

    # Ler planilhas
    df_monica = processar_planilha(origem_path1)
    df_silmar = processar_planilha(origem_path2)

    # Conectar ao banco de dados
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

        # Limpar tabelas existentes
    cursor.execute("DELETE FROM transacoes_monica")
    cursor.execute("DELETE FROM transacoes_silmar")
    cursor.execute("DELETE FROM transacoes_consolidadas")

    # Função para criar tabela
    def criar_tabela(nome_tabela):
        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {nome_tabela} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                Data DATE,
                Operacao TEXT,
                Ativo TEXT,
                Quantidade INTEGER,
                Preço REAL,
                Nota TEXT,
                Corretora TEXT
            )
        """)

    # Criar tabelas
    criar_tabela("transacoes_monica")
    criar_tabela("transacoes_silmar")
    criar_tabela("transacoes_consolidadas")

    # Função para inserir dados
    def inserir_dados(df, tabela):
        cursor.executemany(f"""
            INSERT INTO {tabela} (Data, Operacao, Ativo, Quantidade, Preço, Nota, Corretora)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, df.values.tolist())

    # Inserir dados
    inserir_dados(df_monica, "transacoes_monica")
    inserir_dados(df_silmar, "transacoes_silmar")
    
    # Consolidar dados
    cursor.execute("""
        INSERT INTO transacoes_consolidadas (Data, Operacao, Ativo, Quantidade, Preço, Nota, Corretora)
        SELECT Data, Operacao, Ativo, Quantidade, Preço, Nota, Corretora FROM transacoes_monica
        UNION ALL
        SELECT Data, Operacao, Ativo, Quantidade, Preço, Nota, Corretora FROM transacoes_silmar
    """)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    atualizar_transacoes()