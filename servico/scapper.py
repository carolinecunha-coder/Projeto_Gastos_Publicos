import os
import pandas as pd

def carregar_dados_brutos(caminho_csv: str) -> pd.DataFrame:
    """Lê o arquivo CSV da pasta base-dados."""
    if not os.path.exists(caminho_csv):
        raise FileNotFoundError(f"Arquivo não encontrado no caminho: {caminho_csv}")
    
    print(f"Lendo dados do arquivo: {caminho_csv}...")
    df = pd.read_csv(caminho_csv, encoding="latin1", sep=";")
    return df