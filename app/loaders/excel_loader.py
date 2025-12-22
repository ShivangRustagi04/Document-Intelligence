import pandas as pd

def load_parameters(path):
    df = pd.read_excel(path)
    return df.to_dict(orient="records")
