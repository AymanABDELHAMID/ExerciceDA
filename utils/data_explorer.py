"""

Utility functions to explore data

"""
import pandas as pd
import numpy as np

# Explorer le dataset
def get_missing_values(df):
    """
    Compute number and % of missing values for each column of input data frame, and return result in a data frame
    with columns 'Variable', 'Nombre de valeurs manquantes', '% de valeurs manquantes'.
    Return data frame is sorted on 'Nombre de valeurs manquantes' (decreasing).

    Args:
        df : pandas data frame

    Return:
        data frame
    """
    number_missing = df.isna().sum()
    pct_missing = 100 * np.round(number_missing / len(df), 2)

    res = pd.DataFrame([number_missing, pct_missing]).T.reset_index()
    res = res.rename(columns={"index": "Variable", 0: "Nombre de valeurs manquantes", 1: "% de valeurs manquantes"})
    res = res.sort_values(by="Nombre de valeurs manquantes", ascending=False)

    return res