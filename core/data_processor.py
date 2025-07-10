import pandas as pd

def clean_data(df):
    """Realiza limpeza básica dos dados"""
    # Remover duplicatas
    df_clean = df.drop_duplicates()
    
    # Converter strings para minúsculas nos nomes das colunas
    df_clean.columns = df_clean.columns.str.lower()
    
    return df_clean