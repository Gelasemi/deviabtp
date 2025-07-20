
import streamlit as st
from fpdf import FPDF
from num2words import num2words
from PIL import Image
import matplotlib.pyplot as plt
import io
import base64
from lang import translations
from utils import (
    initialize_session_state,
    process_uploaded_image,
    run_ai_simulation,
    analyze_plan,
    calculate_costs,
    generate_pdf
)

st.set_page_config(page_title="DEVIABTP", layout="wide")

initialize_session_state()

st.sidebar.image("assets/logo.png", width=250)
st.sidebar.title("DEVIABTP")
language = st.sidebar.selectbox("🌐 Choisissez la langue", ["fr", "en"])
st.session_state["language"] = language

st.title("🏗️ DEVIABTP - Générateur de Devis & Facture")
st.markdown(translations[language]["ai_note"])

client_name = st.text_input(translations[language]["client"], value=st.session_state["client_name"])
st.session_state["client_name"] = client_name

uploaded_file = st.file_uploader("📤 " + translations[language]["title_description"], type=["jpg", "png", "jpeg", "webp"])
if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="🖼️ Plan téléversé", use_column_width=True)
    st.session_state["image"] = image

construction_type = st.selectbox(
    translations[language]["type_construction"],
    ["2 étages", "3 étages", "Villa basse"] if language == "fr" else ["2 floors", "3 floors", "Single-story villa"]
)
st.session_state["construction_type"] = construction_type

if st.button("⚙️ Analyser le plan & Générer le devis"):
    if not client_name or not uploaded_file:
        st.warning("Veuillez renseigner toutes les informations nécessaires.")
    else:
        run_ai_simulation(language)
        analyze_plan(construction_type, language)
        calculate_costs()
        pdf_file = generate_pdf()
        st.success("✅ PDF généré avec succès.")

        with open(pdf_file, "rb") as f:
            base64_pdf = base64.b64encode(f.read()).decode("utf-8")
        href = f'<a href="data:application/octet-stream;base64,{base64_pdf}" download="DEVIABTP_Devis.pdf">📥 Télécharger le PDF</a>'
        st.markdown(href, unsafe_allow_html=True)
