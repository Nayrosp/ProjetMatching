import streamlit as st
import pandas as pd
import mysql.connector

# Se connecter à la base de données MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="MySqlMatching",
    database="matching2"
)
cursor = conn.cursor()

# Fonctions pour ajouter des données
def ajouter_nouveau_patient(cursor, nom, prenom, date_naissance, sexe, adresse, telephone, email):
    cursor.execute(
        "INSERT INTO Patients (Nom, Prenom, Date_de_naissance, Sexe, Adresse, Telephone, Adresse_mail) VALUES (%s, %s, %s, %s, %s, %s, %s)",
        (nom, prenom, date_naissance, sexe, adresse, telephone, email)
    )
    conn.commit()

def ajouter_nouvelle_analyse(cursor, nom_analyse, description, concentration, valeur_reference, date_analyse, commentaire, id_patient):
    cursor.execute(
        "INSERT INTO Analyses (Nom_de_l_analyse, Description_de_l_analyse, Concentration__mg_L_, Valeur_de_reference__mg_L_, Date_analyse, Commentaire, Id_Patients) VALUES (%s, %s, %s, %s, %s, %s, %s)",
        (nom_analyse, description, concentration, valeur_reference, date_analyse, commentaire, id_patient)
    )
    conn.commit()

# Interface Streamlit pour ajouter un patient
with st.container():
     st.write("---")
     st.title("Création d'un nouveau patient")

nom = st.text_input("Nom :")
prenom = st.text_input("Prénom :")
date_naissance = st.date_input("Date de naissance :")
sexe = st.selectbox("Sexe :", ["Homme", "Femme", "Autre"])
adresse = st.text_area("Adresse :")
telephone = st.text_input("Téléphone :")
email = st.text_input("Adresse email :")

# Bouton pour ajouter un patient
if st.button("Ajouter Patient"):
    ajouter_nouveau_patient(cursor, nom, prenom, date_naissance, sexe, adresse, telephone, email)
    st.success("Nouveau patient ajouté avec succès !")

# Interface Streamlit pour ajouter une analyse
with st.container():
     st.write("---")
     st.title("Création d'une nouvelle analyse")

nom_analyse = st.text_input("Nom de l'analyse :")
description = st.text_area("Description de l'analyse :")
concentration = st.number_input("Concentration (mg/L) :", min_value=0.0)
valeur_reference = st.number_input("Valeur de référence (mg/L) :", min_value=0.0)
date_analyse = st.date_input("Date de l'analyse :")
commentaire = st.text_area("Commentaire :")
id_patient = st.number_input("ID du patient :", min_value=1)

# Bouton pour ajouter une analyse
if st.button("Ajouter Analyse") and id_patient:
    ajouter_nouvelle_analyse(cursor, nom_analyse, description, concentration, valeur_reference, date_analyse, commentaire, id_patient)
    st.success("Nouvelle analyse ajoutée avec succès !")

# Fermer le curseur et la connexion
cursor.close()
conn.close()

# Extraire les données de la table Patients
connexion = mysql.connector.connect(
    host="localhost",
    user="root",
    password="MySqlMatching",
    database="matching2"
)
cursor = connexion.cursor()
cursor.execute("SELECT * FROM Patients")
patients_data = cursor.fetchall()
columns_patients = [i[0] for i in cursor.description]
df_patients = pd.DataFrame(patients_data, columns=columns_patients)

# Extraire les données de la table Analyses
cursor.execute("SELECT * FROM Analyses")
analyses_data = cursor.fetchall()
columns_analyses = [i[0] for i in cursor.description]
df_analyses = pd.DataFrame(analyses_data, columns=columns_analyses)

# Fermer le curseur
cursor.close()


