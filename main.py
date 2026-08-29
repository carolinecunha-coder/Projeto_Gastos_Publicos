import os
import logging
from urllib.parse import quote_plus
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from servico.scapper import carregar_dados_brutos
from servico.transformador import construir_star_schema

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Configuração dos Logs (Grava no arquivo local e exibe no terminal)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [%(levelname)s] - %(message)s",
    handlers=[
        logging.FileHandler("execucao_etl.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)

# Leitura segura das credenciais via .env
USUARIO = os.getenv("DB_USER", "postgres")
SENHA = os.getenv("DB_PASSWORD")
HOST = os.getenv("DB_HOST", "127.0.0.1")
PORTA = os.getenv("DB_PORT", "5432")
BANCO = os.getenv("DB_NAME", "dw_gastos_publicos")

CAMINHO_CSV = os.path.join("base-dados", "202608_Despesas.csv")

def executar_pipeline():
    logging.info("=== INICIANDO PIPELINE ETL DE GASTOS PÚBLICOS ===")
    
    try:
        if not SENHA:
            raise ValueError("A senha do banco de dados não foi encontrada no arquivo .env!")

        # 1. Extração
        logging.info("Passo 1/3: Carregando dados brutos do CSV...")
        df_bruto = carregar_dados_brutos(CAMINHO_CSV)
        logging.info(f"Dados brutos carregados com sucesso. Linhas encontradas: {len(df_bruto)}")
        
        # 2. Transformação
        logging.info("Passo 2/3: Processando transformações do Star Schema...")
        dim_orgao, dim_funcao, dim_elemento, dim_tempo, fato_despesas = construir_star_schema(df_bruto)
        logging.info("Modelagem relacional (Tabela Fato e Dimensões) gerada.")
        
        # 3. Conexão e Carga
        logging.info("Passo 3/3: Conectando ao PostgreSQL para recriação das tabelas...")
        SENHA_ENCODED = quote_plus(SENHA)
        engine = create_engine(f"postgresql+psycopg2://{USUARIO}:{SENHA_ENCODED}@{HOST}:{PORTA}/{BANCO}")
        
        with engine.begin() as conn:
            logging.info("Limpando tabelas antigas (DROP TABLE CASCADE)...")
            conn.execute(text("DROP TABLE IF EXISTS fato_despesas CASCADE;"))
            conn.execute(text("DROP TABLE IF EXISTS dim_orgao CASCADE;"))
            conn.execute(text("DROP TABLE IF EXISTS dim_funcao CASCADE;"))
            conn.execute(text("DROP TABLE IF EXISTS dim_elemento_despesa CASCADE;"))
            conn.execute(text("DROP TABLE IF EXISTS dim_tempo CASCADE;"))
            
            logging.info("Enviando novas tabelas para o Data Warehouse...")
            dim_orgao.to_sql("dim_orgao", conn, if_exists="replace", index=False)
            dim_funcao.to_sql("dim_funcao", conn, if_exists="replace", index=False)
            dim_elemento.to_sql("dim_elemento_despesa", conn, if_exists="replace", index=False)
            dim_tempo.to_sql("dim_tempo", conn, if_exists="replace", index=False)
            fato_despesas.to_sql("fato_despesas", conn, if_exists="replace", index=False)

        logging.info("=== PIPELINE EXECUTADO COM SUCESSO! ===")

    except Exception as e:
        logging.error(f"Falha crítica na execução do pipeline: {str(e)}", exc_info=True)

if __name__ == "__main__":
    executar_pipeline()