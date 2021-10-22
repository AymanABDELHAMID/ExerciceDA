
"""
@author Ayman Mahmoud
22.10.21

Exercice entretien PWC :
"""
# libraries to use
import pandas as pd
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from utils import data_explorer
import calendar

"""
Exercice partie 1

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
# parameters pandas
pd.options.display.max_columns = 100
pd.options.display.max_rows = 100

# path
inputDirectory = "./data/"
outputDirectory = "./output/"
# 1. entrer des données :
# lecture du fichier "Popular Movie Data Non Financial.xlsx"
movieData = pd.ExcelFile(inputDirectory+"popularMovieDataNonFinancial.xlsx")
md = movieData.parse("Movie Data")

# 2. supprimer les premiers lignes vides de la tables
md = md.iloc[6:]
# 3. Attribution dynamique d'un nouveau nom: Faire en sorte que la 1ere ligne soit l’en-tête
md = md.rename(columns=md.iloc[0])
# maintenant je supprime la 1ere ligne.
md = md.iloc[1:]
# Je change l'index pour commencer à 0.
md = md.reset_index(drop=True)

# exploration, nettoyage et préparation des données :

# 4. Nettoyage des données
# 4.1. Remplacer les données manquantes par vide
md = md.fillna("")
# 4.2. mettre à jour la casse en majuscule pour les champs: Genre, MPAA Rating et Source
columnsToModify = ["Genre", "MPAA Rating", "Source"]
for columnName in columnsToModify:
    md[columnName] = md[columnName].str.upper()

# 5. Champ automatique
# 5.1. Video Release : Date
md["Video Release"] = pd.to_datetime(md["Video Release"])
# 5.2. Opening Weekend Theaters : Double/Decimal
md["Opening Weekend Theaters"] = pd.to_numeric(md["Opening Weekend Theaters"])
# 5.3. Maximum Theaters: Double/Decimal
md["Maximum Theaters"] = pd.to_numeric(md["Maximum Theaters"])

# data exploration
genre = md["Genre"].unique()

"""
Exercice partie 2

Exercice entretien PWC :
Après un examen du fichier "Popular Movie Data Financial All v2",
il faut charger, optimiser puis nettoyer la table avant
la joindre avec les données "Popular Movie Data Non Financial".
"""
# Lecture du fichier "Popular Movie Data Financial All v2"
movieDataFinancial = pd.ExcelFile(inputDirectory+"popularMovieFinancialALL.xlsx")
mdf = movieDataFinancial.parse("BoxOffice")

# 2. Champ automatique:
# 2.1. Optimise la taille des champs
# 2.2. Mettre "Release Year" au format date
# j'ai remarqué que quand la date se transorme en DateTime format, il devient 1970.
# cette étape n'est pas nécessaire pour le jeu des données.

# mdf["Release Year"] = pd.to_datetime(mdf["Release Year"])
# mdf["Release Year"] = mdf["Release Year"].dt.year

# 3. Nettoyage des données:
#Remplacer les données manquantes par vide
mdf = mdf.fillna("")
# supprimer les doubles espaces
mdf.columns = mdf.columns.str.replace('  ', ' ')

"""
Exercice partie 3

Jointure entre "Popular Movie Data Non Financial" et "Popular Movie Data Financial All v2" 
"""
# 2. Créer une nouvelle collonne de "Release Year"
md["Release Year"] = md["Theater Release"].dt.year

# on remarque que le film n'est pas écrit de la même façon dans les 2 fichiers
mdf = mdf.convert_dtypes()
md = md.convert_dtypes()
mdf["Movie Title"] = mdf["Movie Title"].str.upper()
md["Movie Title"] = md["Movie Title"].str.upper()

## Jointure
md_mdf = pd.merge(md, mdf, how='left', left_on=["Movie Title", "Release Year"], right_on = ["Movie Title", "Release Year"], indicator='Exist')
print("Dimension de la table après jointure : {}".format(md_mdf.shape))
data_explorer.get_missing_values(md_mdf)

# Vérification des données
md_mdf["Exist"].value_counts()


# Exploration, nettoyage des données
"""
Cette étape d'analyse des données est importante pour ajouter les infos imortante 
à l'étape de la visualization des données.
"""
# Visuel 1
# Profit Margin %
md_mdf["Profit Margin (%)"] = ((md_mdf["Profit ($)"])/(md_mdf["Global Box Office ($)"]))*100.

# Visuel 2
# Realisateurs et films
realisateur = md_mdf.groupby("Director").mean()
realisateur1 = realisateur[["Profit Margin (%)","Global Box Office ($)"]]
realisateur1 = realisateur1.sort_values(by = "Profit Margin (%)", ascending=False)
realisateur2 = realisateur[["Profit Margin (%)","Global Box Office ($)"]]
realisateur2 = realisateur2.sort_values(by = "Global Box Office ($)", ascending=False)

# Visuel 3
# nous aurons besoins de release month
md_mdf["Release Month"] = md_mdf["Theater Release"].dt.month
md_mdf["Release Month Str"] = md_mdf["Release Month"].apply(lambda x: calendar.month_abbr[x])
releaseMonthRevenueMean = md_mdf.groupby(["Release Month Str", "Release Month"]).mean()
releaseMonthRevenueMean = releaseMonthRevenueMean["Global Box Office ($)"]
releaseMonthRevenueSum = md_mdf.groupby(["Release Month Str", "Release Month"]).sum()
releaseMonthRevenueSum = releaseMonthRevenueSum["Global Box Office ($)"]
releaseMonthRevenue = pd.concat([releaseMonthRevenueMean, releaseMonthRevenueSum], axis=1)
releaseMonthRevenue = releaseMonthRevenue.sort_values(by = "Release Month", ascending=True)


# Visuel 4
# nous nous interessons au top 10 seulement
top10 = md_mdf.sort_values(by = "Global Box Office ($)", ascending=False)
top10 = top10[:10]
top10 = top10[["Movie Title","Release Year","Genre","Global Box Office ($)", "Profit Margin (%)"]]


# J'exporte les données en format csv et je la relie dans le script de @link exercice_partie_4.py
# md_mdf
file_name = outputDirectory+"md_mdf.xlsx"
# saving the excel
md_mdf.to_excel(file_name)

# 1. Genre
genre = md_mdf.groupby("Genre").sum()
genre["# of movies"] = md_mdf.groupby("Genre").size()
genre = genre[["# of movies", "Profit Margin (%)", "Global Box Office ($)"]]

file_name = outputDirectory+"genre.xlsx"
# saving the excel
genre.to_excel(file_name)


# 2. Réalisateurs
file_name = outputDirectory+"directorProfit.xlsx"
# saving the excel
realisateur1.to_excel(file_name)

file_name = outputDirectory+"directorGBO.xlsx"
# saving the excel
realisateur2.to_excel(file_name)

# 3. Revenues et mois
file_name = outputDirectory+"revenues.xlsx"
# saving the excel
releaseMonthRevenue.to_excel(file_name)

# 4. Top 10
file_name = outputDirectory+"top10.xlsx"
# saving the excel
top10.to_excel(file_name)


print('DataFrames sont sauvgardés dans output.')