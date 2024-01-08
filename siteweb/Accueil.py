import streamlit as st
import requests
from streamlit_lottie import st_lottie
import psycopg2

st.set_page_config(
    page_title="Accueil",
    page_icon="😈",
)

def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json

# ---- LOAD ASSETS ----

lottie_coding = "https://lottie.host/cb413a1f-c73f-47c7-ba8b-b9948defcbfc/7ST4jeTPwB.json"

# ---- En tête ----

st.title("Bienvenue sur CESI Medical - Votre Partenaire en Analyses Biomédicales")
st.write("""
Chez CESI Medical, nous sommes dévoués à fournir des services d'analyses biomédicales de haute qualité, précis et fiables. 
Forts d'une équipe d'experts qualifiés et équipés des technologies les plus avancées, nous nous engageons à soutenir les professionnels de la santé, les chercheurs et les patients dans leurs besoins d'analyses diagnostiques et de recherche.
         """)

# ---- BUT du projet -----

with st.container():
    st.write("---")
    left_column, right_column = st.columns(2)
    with left_column:
        st.header("Nos Services")
        st.write("##")
        st.write(
            """
- Analyses Diagnostiques : 
Nous offrons une gamme complète d'analyses pour aider au diagnostic et au suivi des maladies.

- Recherche Biomédicale : 
Notre laboratoire est équipé pour soutenir la recherche avancée dans divers domaines biomédicaux.

- Conseil et Formation : 
Nous proposons des services de conseil et de formation pour aider les professionnels à interpréter les résultats des analyses et à optimiser leurs pratiques
            """
                )
        
with right_column:
    st_lottie(lottie_coding, height=400, key="coding")

with st.container():
    st.write("---")
    st.header("Technologie Avancée")
    texte_technologie = ("""
    Notre laboratoire est équipé des technologies les plus récentes, garantissant des analyses précises, 
    rapides et conformes aux normes internationales. Nous investissons continuellement dans la formation de notre personnel 
    et la mise à jour de nos équipements pour garantir l'excellence dans nos services.
    """)
    st.markdown(f"<div style='text-align: justify;'>{texte_technologie}</div>", unsafe_allow_html=True)

with st.container():
    st.write("---")
    st.header("Engagement envers la Qualité")
    texte_qualite = ("""
    La qualité est au cœur de tout ce que nous faisons. 
    Nous suivons des protocoles stricts de contrôle qualité et participons régulièrement à des programmes d'évaluation 
    externe pour assurer la fiabilité et la précision de nos analyses.
    """)
    st.markdown(f"<div style='text-align: justify;'>{texte_qualite}</div>", unsafe_allow_html=True)