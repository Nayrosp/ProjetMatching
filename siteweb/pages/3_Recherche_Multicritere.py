import streamlit as st
import mysql.connector
import pandas as pd

# Connexion à la base de données MySQL
connexion = mysql.connector.connect(
    host="localhost",
    user="root",
    password="MySqlMatching",
    database="matching2"
)

# Fonction pour récupérer les données filtrées
def get_filtered_data(nom_patient, prenom_patient, nom_analyse):
    query = """
    SELECT Patients.Nom, Patients.Prenom, Analyses.Nom_de_l_analyse, Analyses.Concentration__mg_L_, Analyses.Valeur_de_reference__mg_L_, Analyses.Commentaire
    FROM Patients
    INNER JOIN Analyses ON Patients.Id_Patients = Analyses.Id_Patients
    WHERE Patients.Nom = '{}' AND Patients.Prenom = '{}' AND Analyses.Nom_de_l_analyse = '{}'
    """.format(nom_patient, prenom_patient, nom_analyse)
    df = pd.read_sql(query, connexion)
    return df

# Interface utilisateur avec Streamlit
st.title("Filtrage des données MySQL avec Streamlit")

# Récupération des noms uniques des patients et des analyses
patients = pd.read_sql("SELECT DISTINCT Nom, Prenom FROM Patients", connexion)
analyses = pd.read_sql("SELECT DISTINCT Nom_de_l_analyse FROM Analyses", connexion)

# Trier les options par ordre alphabétique
patients = patients.sort_values(['Nom', 'Prenom'])
analyses = analyses.sort_values('Nom_de_l_analyse')

# Définir les critères de filtrage
nom_patient = st.selectbox("Choisir un nom de patient :", patients['Nom'].tolist())
prenom_patient = st.selectbox("Choisir un prénom de patient :", patients[patients['Nom'] == nom_patient]['Prenom'].tolist())
nom_analyse = st.selectbox("Choisir un nom d'analyse :", analyses['Nom_de_l_analyse'].tolist())

# Afficher les données filtrées
filtered_df = get_filtered_data(nom_patient, prenom_patient, nom_analyse)
st.write(filtered_df)
