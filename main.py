import streamlit as st
from fpdf import FPDF
from database import init_db, save_plan, get_plan
import os

# Initialiser la base
init_db()

# Crée le dossier plans s'il n'existe pas
if not os.path.exists("plans"):
    os.makedirs("plans")

st.title("📋 Générateur de Plan de Prévention")

mode = st.radio("Que veux-tu faire ?", ["Créer un plan", "Rechercher un plan"])

if mode == "Créer un plan":
    keyword = st.text_input("Mot-clé unique pour retrouver ce plan (ex : site usine A)")
    contenu = st.text_area("Contenu du plan")

    if st.button("Créer et sauvegarder"):
        if keyword and contenu:
            filename = f"plans/{keyword}.pdf"  # PDF stocké dans plans/
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.multi_cell(0, 10, contenu)
            pdf.output(filename)

            save_plan(keyword, filename)
            st.success(f"Plan enregistré sous le nom : {filename}")
            with open(filename, "rb") as f:
                st.download_button("📥 Télécharger le PDF", f, file_name=f"{keyword}.pdf")
        else:
            st.warning("Veuillez entrer un mot-clé et un contenu.")

elif mode == "Rechercher un plan":
    keyword = st.text_input("Entre le mot-clé du plan que tu veux retrouver")
    if st.button("Rechercher"):
        result = get_plan(keyword)
        if result and os.path.exists(result):
            st.success(f"Plan trouvé : {result}")
            with open(result, "rb") as f:
                st.download_button("📥 Télécharger le plan", f, file_name=os.path.basename(result))
        else:
            st.error("Aucun plan trouvé avec ce mot-clé.")
