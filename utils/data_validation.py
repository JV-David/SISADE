import pandas as pd

def validate_data_for_analysis(df):
    """Valida se os dados são adequados para análise"""
    if not isinstance(df, pd.DataFrame):
        raise ValueError("Os dados devem ser um DataFrame do pandas")
    
    if df.empty:
        raise ValueError("O DataFrame está vazio")
    
    if len(df.columns) < 2:
        raise ValueError("O DataFrame deve ter pelo menos 2 colunas")