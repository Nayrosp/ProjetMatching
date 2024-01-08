import streamlit as st
import requests
from streamlit_lottie import st_lottie
import psycopg2

st.header("Si vous voulez me contacter")

contact_form = """
    <form action="https://formsubmit.co/thomas.herveux.0112@gmail.com" method="POST">
        <input type="hidden" name="_captcha" value="false">
        <input type="text" name="name" placeholder="Votre nom" required>
        <input type="email" name="email" placeholder="Votre email" required>
        <textarea name="message" placeholder="Votre message" required></textarea>
        <button type="submit">Send</button>
    </form>
    """
st.markdown(contact_form, unsafe_allow_html=True)

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

local_css("style/style.css")