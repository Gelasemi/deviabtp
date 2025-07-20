
import streamlit as st
from fpdf import FPDF
from num2words import num2words
from PIL import Image
import io
import base64

st.set_page_config(page_title="DEVIABTP", layout="wide")

# Titre principal
st.image("mialyg.png", width=120)
st.title("DEVIABTP - Générateur de devis BTP intelligent")

# Upload image du plan
uploaded_file = st.file_uploader("Téléverser le plan d'architecture (JPG, PNG)", type=["jpg", "jpeg", "png"])
if uploaded_file:
    st.image(uploaded_file, caption="Plan téléversé", use_column_width=True)

# Informations client
client = st.text_input("Nom du client", "Client inconnu")
construction_type = st.selectbox("Type de construction", ["Villa basse", "2 étages", "3 étages"])
etages = {"Villa basse": 1, "2 étages": 2, "3 étages": 3}[construction_type]

# Matériaux simulés
materiaux = {
    "Ciment (sacs)": (400, 35000),
    "Fer à béton (kg)": (1500, 7000),
    "Parpaings (unités)": (4000, 1000),
}

st.subheader("Résumé des matériaux")
total = 0
for libelle, (qte, prix_unit) in materiaux.items():
    st.markdown(f"- **{libelle}** : {qte} x {prix_unit} Ar = {qte * prix_unit:,} Ar")
    total += qte * prix_unit

st.markdown(f"### Coût total estimé : {total:,} Ariary")

# Génération du PDF
def create_pdf():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="DEVIABTP - Devis BTP", ln=True, align="C")
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Client : {client}", ln=True)
    pdf.cell(200, 10, txt=f"Type de construction : {construction_type} ({etages} étages)", ln=True)
    pdf.ln(5)
    pdf.cell(200, 10, txt="Matériaux : ", ln=True)
    for libelle, (qte, prix_unit) in materiaux.items():
        pdf.cell(200, 10, txt=f"- {libelle} : {qte} x {prix_unit} = {qte * prix_unit:,} Ar", ln=True)
    pdf.ln(5)
    pdf.cell(200, 10, txt=f"Coût total : {total:,} Ariary", ln=True)
    total_lettres = num2words(total, lang="fr").capitalize()
    pdf.cell(200, 10, txt=f"Montant en lettres : {total_lettres} ariary", ln=True)
    return pdf

# Affichage bouton de téléchargement PDF
if st.button("Générer le PDF du devis"):
    pdf = create_pdf()
    buffer = io.BytesIO()
    pdf.output(buffer)
    buffer.seek(0)
    b64 = base64.b64encode(buffer.read()).decode()
    href = f'<a href="data:application/octet-stream;base64,{b64}" download="devis_btp.pdf">📄 Télécharger le devis en PDF</a>'
    st.markdown(href, unsafe_allow_html=True)
