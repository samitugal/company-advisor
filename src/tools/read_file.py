import pandas as pd
def read_csv(file_path: str) -> pd.DataFrame:
    return pd.read_csv(file_path)

def read_excel(file_path: str) -> pd.DataFrame:
    return pd.read_excel(file_path)

def read_json(file_path: str) -> pd.DataFrame:
    return pd.read_json(file_path)

def read_txt(file_path: str) -> pd.DataFrame:
    return pd.read_txt(file_path)

