from datetime import datetime

def format_timestamp(timestamp=None):
    """Formata timestamp para exibição"""
    if timestamp is None:
        timestamp = datetime.now()
    return timestamp.strftime("%d/%m/%Y %H:%M:%S")

def safe_divide(numerator, denominator):
    """Divisão segura (evita divisão por zero)"""
    return numerator / denominator if denominator != 0 else 0