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


# Explorer le dataset
def get_value_counts(df):
    """
    Getting value counts in each columns to see if there is unuseful data

    Args:
        df : pandas data frame

    Return:
        data frame with column name and values
    """
    columns = df.columns.values
    valueCount = []
    for columnName in columns:
        valueCount.append([columnName, df[columnName].value_counts().size])

    res = pd.DataFrame(valueCount, columns=["Column", "Value Count"])
    res = res.sort_values(by = "Value Count", ascending=True)

    return res