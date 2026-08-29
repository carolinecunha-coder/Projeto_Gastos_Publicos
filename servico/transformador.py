import pandas as pd

def tratar_valores_numericos(df: pd.DataFrame) -> pd.DataFrame:
    """Converte valores monetários de texto para formato numérico float."""
    colunas_financeiras = [
        "Valor Empenhado (R$)",
        "Valor Liquidado (R$)",
        "Valor Pago (R$)",
        "Valor Restos a Pagar Pagos (R$)"
    ]
    
    for col in colunas_financeiras:
        if col in df.columns:
            df[col] = (
                df[col]
                .astype(str)
                .str.replace(".", "", regex=False)
                .str.replace(",", ".", regex=False)
                .astype(float)
            )
    return df

def construir_star_schema(df: pd.DataFrame):
    """Cria as tabelas de Dimensão e Fato (Modelo Estrela)."""
    df = tratar_valores_numericos(df)
    
    # Dimensão Órgão
    dim_orgao = df[[
        "Código Órgão Superior", "Nome Órgão Superior",
        "Código Órgão Subordinado", "Nome Órgão Subordinado"
    ]].drop_duplicates().reset_index(drop=True)
    dim_orgao["id_orgao"] = dim_orgao.index + 1
    dim_orgao.columns = [
        "codigo_orgao_superior", "nome_orgao_superior",
        "codigo_orgao_subordinado", "nome_orgao_subordinado", "id_orgao"
    ]

    # Dimensão Função
    dim_funcao = df[[
        "Código Função", "Nome Função",
        "Código Subfução", "Nome Subfunção"
    ]].drop_duplicates().reset_index(drop=True)
    dim_funcao["id_funcao"] = dim_funcao.index + 1
    dim_funcao.columns = [
        "codigo_funcao", "nome_funcao",
        "codigo_subfuncao", "nome_subfuncao", "id_funcao"
    ]

    # Dimensão Elemento de Despesa
    dim_elemento = df[[
        "Código Grupo de Despesa", "Nome Grupo de Despesa",
        "Código Elemento de Despesa", "Nome Elemento de Despesa"
    ]].drop_duplicates().reset_index(drop=True)
    dim_elemento["id_elemento"] = dim_elemento.index + 1
    dim_elemento.columns = [
        "codigo_grupo", "nome_grupo",
        "codigo_elemento", "nome_elemento", "id_elemento"
    ]

    # Dimensão Tempo
    ano_mes_str = df["Ano e mês do lançamento"].iloc[0]
    ano, mes = map(int, ano_mes_str.split("/"))
    dim_tempo = pd.DataFrame([{
        "id_tempo": int(f"{ano}{mes:02d}"),
        "ano_mes": ano_mes_str,
        "ano": ano,
        "mes": mes
    }])

    # Tabela Fato
    fato = df.merge(
        dim_orgao,
        left_on=["Código Órgão Superior", "Nome Órgão Superior", "Código Órgão Subordinado", "Nome Órgão Subordinado"],
        right_on=["codigo_orgao_superior", "nome_orgao_superior", "codigo_orgao_subordinado", "nome_orgao_subordinado"]
    ).merge(
        dim_funcao,
        left_on=["Código Função", "Nome Função", "Código Subfução", "Nome Subfunção"],
        right_on=["codigo_funcao", "nome_funcao", "codigo_subfuncao", "nome_subfuncao"]
    ).merge(
        dim_elemento,
        left_on=["Código Grupo de Despesa", "Nome Grupo de Despesa", "Código Elemento de Despesa", "Nome Elemento de Despesa"],
        right_on=["codigo_grupo", "nome_grupo", "codigo_elemento", "nome_elemento"]
    )

    fato["id_tempo"] = int(f"{ano}{mes:02d}")

    fato_despesas = fato[[
        "id_orgao", "id_funcao", "id_elemento", "id_tempo",
        "Valor Empenhado (R$)", "Valor Liquidado (R$)", "Valor Pago (R$)", "Valor Restos a Pagar Pagos (R$)"
    ]]
    fato_despesas.columns = [
        "id_orgao", "id_funcao", "id_elemento", "id_tempo",
        "valor_empenhado", "valor_liquidado", "valor_pago", "valor_restos_pagos"
    ]

    return dim_orgao, dim_funcao, dim_elemento, dim_tempo, fato_despesas