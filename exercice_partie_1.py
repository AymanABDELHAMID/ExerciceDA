"""
@author Ayman Mahmoud
22.10.21

Exercice entretien PWC :
1. Entrer des données: Charger le fichier «Popular Movie Data Non Financial.xlsx»
2. Sélectionner des enregistrements: Supprimer les premières lignes vides de la table
3. Attribution dynamique d'un nouveau nom: Faire en sorte que la 1ere ligne soit l’en-tête
4. Nettoyage des données:
    - Remplacer les Nulls par des vides, supprimer les doubles espaces
    - Mettre à jour la casse en majuscule pour les champs : Genres, MPAA Rating et Source
    - Champ automatique: Optimiser le type des champs et mettre à jour le type des données:
        Video Release : Date
        Opening Weekend Theaters : Double/Decimal
        Maximum Theaters : Double/Decimal
"""

# libraries to use
import pandas as pd
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from utils import *

# parameters pandas
pd.options.display.max_columns = 100
pd.options.display.max_rows = 100

# path
path = "./data/"

# 1. entrer des données :
# lecture du fichier "Popular Movie Data Non Financial.xlsx"
movieData = pd.ExcelFile(path+"popularMovieDataNonFinancial.xlsx")
md = movieData.parse("Movie Data")

# 2. supprimer les premiers lignes vides de la tables
md = md.iloc[6:]
# 3. Attribution dynamique d'un nouveau nom: Faire en sorte que la 1ere ligne soit l’en-tête
md = md.rename(columns=md.iloc[0])
# maintenant je supprime la 1ere ligne.
md = md.iloc[1:]
# Je change l'indew pour commencer à 0.
md = md.reset_index(drop=True)

# exploration, nettoyage et préparation des données :
# 4. Nettoyage des données
# 4.1. remplacer les nulles par des vides

# 4.2. mettre à jour la casse en majuscule pour les champs: Genre, MPAA Rating et Source


# data exploration
genre = md["Genre"].unique()



