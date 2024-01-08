import streamlit as st
import requests
import pymysql
import pandas as pd

# Fonction pour récupérer les données depuis l'API Flask
def get_data_from_api(endpoint):
    url = f"http://localhost:8501/{endpoint}"
    response = requests.get(url)
    if response.status_code == 200:
        return pd.DataFrame(response.json())
    else:
        st.error(f"Erreur {response.status_code}: {response.text}")
        return pd.DataFrame()

# Connexion à la base de données MySQL
connection = pymysql.connect(
    host='localhost',
    user='root',
    password='MySqlMatching',
    db='matching2'
)

# Extraire les données de la table Patients
df_patients = pd.read_sql("SELECT * FROM Patients", connection)

# Extraire les données de la table Analyses
df_analyses = pd.read_sql("SELECT * FROM Analyses", connection)

# Fermer la connexion à la base de données
connection.close()

# Fusionner les DataFrames en utilisant la colonne 'Id_Patients'
df_merged = pd.merge(df_patients, df_analyses, on='Id_Patients', how='inner')

# Afficher le DataFrame fusionné dans Streamlit
st.title("Analyses des patients")

# Widget de saisie pour la recherche
recherche = st.text_input("Quelles informations voulez-vous ?")

# Filtrer le DataFrame en fonction de la requête de recherche
if recherche:
    df_filtre = df_merged[df_merged.apply(lambda row: row.astype(str).str.contains(recherche, case=False).any(), axis=1)]
    
    # Vérifier si le DataFrame filtré est vide
    if df_filtre.empty:
        st.warning(f"Aucun résultat trouvé pour '{recherche}'. Veuillez essayer une autre requête.")
    else:
        st.subheader(f"Résultats de la recherche pour '{recherche}'")
        st.dataframe(df_filtre)
