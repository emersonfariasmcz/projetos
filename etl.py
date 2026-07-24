import os
import sqlite3
import pandas as pd

# 1. Configurações de Caminho Absoluto
DIRETORIO_ATUAL = os.path.dirname(os.path.abspath(__file__))
ARQUIVO_EXCEL = os.path.join(DIRETORIO_ATUAL, "vendas.xlsx")
BANCO_DADOS = os.path.join(DIRETORIO_ATUAL, "vendas.db")


def criar_tabela(cursor):
    """Cria a tabela tb_vendas no SQLite com schema em snake_case."""
    query = """
    CREATE TABLE IF NOT EXISTS tb_vendas (
        id INTEGER PRIMARY KEY,
        data TEXT,
        cliente TEXT,
        uf TEXT,
        cidade TEXT,
        produto TEXT,
        marca TEXT,
        qtde REAL,
        preco_unitario REAL,
        valor_bruto REAL,
        pct_desconto REAL,
        valor_desconto REAL,
        valor_venda REAL,
        vencimento TEXT,
        data_pagamento TEXT,
        documento TEXT,
        canal_venda TEXT,
        vendedor TEXT,
        pct_comissao REAL,
        valor_comissao REAL,
        forma_pagamento TEXT
    );
    """
    cursor.execute(query)

def padronizar_colunas(df: pd.DataFrame) -> pd.DataFrame:
    """Padroniza e mapeia dinamicamente nomes de colunas com apelidos tolerantes."""
    mapeamento = {}
    for col in df.columns:
        c_orig = col
        c = str(col).strip().lower()
        # Limpeza de acentos e caracteres especiais
        c = (
            c.replace("ã", "a")
            .replace("ç", "c")
            .replace("é", "e")
            .replace("á", "a")
        )
        c = c.replace("%", "pct").replace(" ", "_").replace(".", "")

        # Mapeamento estrito de apelidos para os nomes da tabela SQLite
        if c in ["id", "codigo"]:
            c = "id"
        elif c in ["qtd", "qtde", "quantidade"]:
            c = "qtde"
        elif c in ["preco_unitario", "preco_unit", "vlr_unit"]:
            c = "preco_unitario"
        elif c in ["canal_de_venda", "canal_venda", "canal"]:
            c = "canal_venda"
        elif c in ["forma_de_pagamento", "forma_pagamento", "pagamento"]:
            c = "forma_pagamento"
        elif c in ["pct_comis", "pct_comissao", "comis_pct", "comissao_pct"]:
            c = "pct_comissao"
        elif c in ["comissao", "valor_comissao", "vlr_comissao"]:
            c = "valor_comissao"

        mapeamento[c_orig] = c

    return df.rename(columns=mapeamento)

def extrair_e_transformar():
    """Lê a planilha, limpa dados e padroniza para inserção no SQLite."""
    if not os.path.exists(ARQUIVO_EXCEL):
        print(f"❌ Erro: O arquivo '{ARQUIVO_EXCEL}' não foi encontrado.")
        return None, None

    print("🔄 Extraindo e transformando dados do Excel...")
    try:
        df = pd.read_excel(ARQUIVO_EXCEL)

        # 1. Padronização Inteligente de Colunas
        df = padronizar_colunas(df)

        # 2. Conversão de datas para formato ISO (YYYY-MM-DD)
        colunas_datas = ["data", "vencimento", "data_pagamento"]
        for col in colunas_datas:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors="coerce").dt.strftime(
                    "%Y-%m-%d"
                )

        # 3. Validação e Ordem das Colunas da Tabela SQL
        ordem_colunas = [
            "id",
            "data",
            "cliente",
            "uf",
            "cidade",
            "produto",
            "marca",
            "qtde",
            "preco_unitario",
            "valor_bruto",
            "pct_desconto",
            "valor_desconto",
            "valor_venda",
            "vencimento",
            "data_pagamento",
            "documento",
            "canal_venda",
            "vendedor",
            "pct_comissao",
            "valor_comissao",
            "forma_pagamento",
        ]

        # Garante criação de colunas faltantes caso alguma falhe no mapeamento
        for col in ordem_colunas:
            if col not in df.columns:
                df[col] = None

        df = df[ordem_colunas]

        # Substitui NaN do Pandas por None (NULL nativo no SQLite)
        df = df.where(pd.notnull(df), None)

        registros = [tuple(row) for row in df.itertuples(index=False, name=None)]
        ids_excel = set(df["id"].dropna().tolist())

        return registros, ids_excel

    except Exception as e:
        print(f"❌ Erro ao processar o arquivo Excel: {e}")
        return None, None


def carregar_no_sqlite(registros, ids_excel):
    """Persiste dados no SQLite com lógica de Upsert e Sync de Exclusão."""
    if registros is None:
        return

    print("🔌 Conectando ao banco de dados SQLite...")
    try:
        conexao = sqlite3.connect(BANCO_DADOS)
        cursor = conexao.cursor()

        criar_tabela(cursor)

        # UPSERT (INSERT OR UPDATE)
        query_upsert = """
        INSERT INTO tb_vendas (
            id, data, cliente, uf, cidade, produto, marca,
            qtde, preco_unitario, valor_bruto, pct_desconto, valor_desconto,
            valor_venda, vencimento, data_pagamento, documento,
            canal_venda, vendedor, pct_comissao, valor_comissao, forma_pagamento
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(id) DO UPDATE SET
            data=excluded.data,
            cliente=excluded.cliente,
            uf=excluded.uf,
            cidade=excluded.cidade,
            produto=excluded.produto,
            marca=excluded.marca,
            qtde=excluded.qtde,
            preco_unitario=excluded.preco_unitario,
            valor_bruto=excluded.valor_bruto,
            pct_desconto=excluded.pct_desconto,
            valor_desconto=excluded.valor_desconto,
            valor_venda=excluded.valor_venda,
            vencimento=excluded.vencimento,
            data_pagamento=excluded.data_pagamento,
            documento=excluded.documento,
            canal_venda=excluded.canal_venda,
            vendedor=excluded.vendedor,
            pct_comissao=excluded.pct_comissao,
            valor_comissao=excluded.valor_comissao,
            forma_pagamento=excluded.forma_pagamento;
        """
        cursor.executemany(query_upsert, registros)
        print(f"✅ Registros processados (Insert/Update): {len(registros)}")

        # DELETE DE REGISTROS REMOVIDOS
        cursor.execute("SELECT id FROM tb_vendas")
        ids_banco = set(row[0] for row in cursor.fetchall())
        ids_para_deletar = list(ids_banco - ids_excel)

        if ids_para_deletar:
            registros_deletar = [(id_del,) for id_del in ids_para_deletar]
            cursor.executemany(
                "DELETE FROM tb_vendas WHERE id = ?", registros_deletar
            )
            print(f"🗑️ Registros excluídos do banco: {len(ids_para_deletar)}")
        else:
            print("✨ Nenhum registro precisou ser excluído.")

        conexao.commit()
        print(
            "\n🚀 ETL concluído com sucesso! Tabela 'tb_vendas' sincronizada."
        )

    except sqlite3.Error as e:
        print(f"❌ Erro no SQLite: {e}")
    finally:
        if "conexao" in locals() and conexao:
            conexao.close()


if __name__ == "__main__":
    registros, ids_excel = extrair_e_transformar()
    if registros:
        carregar_no_sqlite(registros, ids_excel)