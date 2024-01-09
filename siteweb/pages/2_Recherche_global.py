import streamlit as st
import pymysql
import pandas as pd

# Connexion à la base de données MySQL
connexion = pymysql.connect(
    host='localhost',
    user='root',
    password='MySqlMatching',
    db='matching2'
)

# Extraction des données des tables
df_patients = pd.read_sql("SELECT * FROM Patients", connexion)
df_analyses = pd.read_sql("SELECT * FROM Analyses", connexion)

connexion.close()

# Fusion des DataFrames 
df_merged = pd.merge(df_patients, df_analyses, on='Id_Patients', how='inner')

st.title("Analyses des patients")

# Widget de saisie pour la recherche
recherche = st.text_input("Quelles informations voulez-vous ?")

# Filtrer le DataFrame en fonction de la requête de recherche
if recherche:
    df_filtre = df_merged[df_merged.apply(lambda row: row.astype(str).str.contains(recherche, case=False).any(), axis=1)]
    
    if df_filtre.empty:
        st.warning(f"Aucun résultat trouvé pour '{recherche}'. Veuillez essayer une autre requête.")
    else:
        st.subheader(f"Résultats de la recherche pour '{recherche}'")
        st.dataframe(df_filtre)