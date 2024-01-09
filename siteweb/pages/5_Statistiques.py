import streamlit as st
import pymysql
import pandas as pd
import plotly.express as px

try:
    # Connexion à la base de données MySQL
    connexion = pymysql.connect(
        host='localhost',
        user='root',
        password='MySqlMatching',
        db='matching2'
    )

    # Extraire les données de la table Analyses
    df_analyses = pd.read_sql("SELECT * FROM Analyses", connexion)

    # Calculer le nombre d'occurrences pour chaque type d'analyse
    count_analysis = df_analyses['Nom_de_l_analyse'].value_counts()

    # Calculer les pourcentages
    total = count_analysis.sum()
    percentages = (count_analysis / total * 100).round(2)

    # Créer les étiquettes avec les pourcentages
    labels_with_percentages = [f"{label} ({percent}%)"
                               for label, percent in zip(count_analysis.index, percentages)]

    # Créer le graphique camembert pour la répartition des analyses
    fig_analysis = px.pie(names=labels_with_percentages, values=count_analysis.values, title="Répartition des analyses")

    # Afficher le graphique
    st.title("Répartition des analyses")
    st.plotly_chart(fig_analysis)

finally:
    # Fermer la connexion à la base de données
    if 'connexion' in locals():
        connexion.close()
