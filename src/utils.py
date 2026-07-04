import pandas as pd
from datetime import datetime

def format_timestamp(ts_string: str) -> str:
    """
    Standardizes timestamp strings from various formats into a common HH:MM:SS format.
    Handles '2026-06-30T10:14:00' and '10:14:00'.
    """
    if 'T' in ts_string:
        return ts_string.split('T')[-1]
    return ts_string

def safe_divide(a: float, b: float) -> float:
    """Safe division avoiding ZeroDivisionError, useful for metric calculations."""
    return a / b if b != 0 else 0.0

def load_and_clean_csv(filepath: str) -> pd.DataFrame:
    """Robust CSV loader with basic sanitization."""
    try:
        df = pd.read_csv(filepath)
        df.columns = [col.strip().lower() for col in df.columns]
        return df
    except FileNotFoundError:
        print(f"Error: {filepath} not found.")
        return pd.DataFrame()
