import streamlit as st
import plotly.express as px
from fpdf import FPDF
from PIL import Image
import pandas as pd
from io import BytesIO
import base64
from lang import translations

# --- Langue ---
lang = st.selectbox("🌐 Select Language / Fidio fiteny / Choisissez la langue", ["fr", "en", "mg"])
T = translations[lang]

# --- Logo ---
st.image("mialyg.png", width=120)

# --- Titre ---
st.title(f"📐 {T['title']} – DEVIABTP")

# --- Formulaire ---
client = st.text_input(f"👤 {T['client']}")
type_projet = st.selectbox(f"🏗️ {T['project']}", ["Maison", "Pont", "Route"])
param = st.slider(f"📏 {T['param']} (étage ou longueur)", 1, 25, 1)
cout = param * 35000000

st.success(f"💰 {T['cost']}: {cout:,} MGA")

# --- Upload ---
upload = st.file_uploader("📤 Téléversez un croquis ou plan", type=["jpg", "png", "pdf"])
if upload:
    if upload.type.startswith("image"):
        st.image(upload, caption="Croquis reçu", use_column_width=True)
    else:
        st.info("📄 PDF téléversé : aperçu non affiché")

# --- PDF Génération ---
def create_pdf():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="DEVIABTP – Mialy&G", ln=1, align="C")
    pdf.cell(200, 10, txt=f"Client : {client}", ln=2)
    pdf.cell(200, 10, txt=f"Projet : {type_projet}", ln=3)
    pdf.cell(200, 10, txt=f"{T['param']} : {param}", ln=4)
    pdf.cell(200, 10, txt=f"{T['cost']} : {cout:,} MGA", ln=5)
    buffer = BytesIO()
    pdf.output(buffer)
    buffer.seek(0)
    b64 = base64.b64encode(buffer.read()).decode()
    href = f'<a href="data:application/octet-stream;base64,{b64}" download="devis_{client}.pdf">📥 Télécharger le PDF</a>'
    st.markdown(href, unsafe_allow_html=True)

if st.button(T['generate']):
    create_pdf()

# --- Tableau Projets (exemple dynamique) ---
df = pd.DataFrame({
    "Client": [client],
    "Projet": [type_projet],
    "Paramètre": [param],
    "Coût (MGA)": [cout]
})
st.dataframe(df)

# --- Graphique ---
fig = px.bar(df, x="Projet", y="Coût (MGA)", color="Client", title="Vue des coûts par projet")
st.plotly_chart(fig)
