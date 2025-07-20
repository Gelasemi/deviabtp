# pdf_generator.py
from fpdf import FPDF
from utils import clean_text

def generate_pdf(analysis_results, total_cost, construction_type, language, usd_to_ar, eur_to_ar, client_name, total_cost_in_words, translations):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)

    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, txt=clean_text(translations[language]["title_description"]), ln=1, align='C')
    pdf.ln(10)
    pdf.cell(0, 10, txt=clean_text(f"{translations[language]['type_construction']}: {construction_type}"), ln=2)
    pdf.cell(0, 10, txt=clean_text(f"{translations[language]['nb_etages']}: {analysis_results['etages']}"), ln=3)
    pdf.cell(0, 10, txt=clean_text(f"{translations[language]['nb_pieces']}: {analysis_results['pieces']}"), ln=4)
    pdf.cell(0, 10, txt=clean_text(f"{translations[language]['nb_murs']}: {analysis_results['murs']}"), ln=5)

    for section in ["materiaux", "equipements", "prestations"]:
        pdf.cell(0, 10, txt=clean_text(translations[language][section] + ":"), ln=1)
        for name, data in analysis_results[section].items():
            desc = f"- {name.capitalize()} ({data['type']}): {data['quantite']} {data['unite']}"
            pdf.cell(0, 10, txt=clean_text(desc), ln=1)
        pdf.ln(5)

    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, txt=clean_text(translations[language]["title_facture"]), ln=1, align='C')
    pdf.ln(10)
    pdf.cell(0, 10, txt=clean_text(f"{translations[language]['client']}: {client_name}"), ln=1)
    pdf.cell(0, 10, txt=clean_text(f"{translations[language]['type_construction']}: {construction_type}"), ln=1)
    pdf.cell(0, 10, txt=clean_text(f"{translations[language]['cout_total']}: {int(total_cost)} Ariary"), ln=1)
    pdf.cell(0, 10, txt=clean_text(f"{translations[language]['cout_total']} (USD): {int(total_cost / usd_to_ar)} USD"), ln=1)
    pdf.cell(0, 10, txt=clean_text(f"{translations[language]['cout_total']} (EUR): {int(total_cost / eur_to_ar)} EUR"), ln=1)
    pdf.cell(0, 10, txt=clean_text(f"{translations[language]['montant_en_lettres']}: {total_cost_in_words}"), ln=1)
    pdf.ln(5)
    pdf.cell(0, 10, txt=clean_text(translations[language]["note_facture"]), ln=1)

    filename = "devis_facture.pdf"
    pdf.output(filename)
    return filename
