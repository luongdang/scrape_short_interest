import numpy as np
import pandas as pd


def convert(str):
    try:
        return float(str.replace(',', ''))
    except:
        return None


df = pd.DataFrame([
    ['A', '1,234', '456,789'],
    ['B', '1', '---']
], columns=['Company Name', 'X', 'Y'])


def convert_series(x):
    return pd.to_numeric(x.str.replace(',', ''), errors='coerce')

df.iloc[:, 1:] = df.iloc[:, 1:].apply(convert_series, axis=1)
print(df)