import json
import pandas as pd

def load_materials(file_path="data/materials.json"):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            materials = json.load(f)
        return materials
    except FileNotFoundError:
        return {}

def save_materials(materials, file_path="data/materials.json"):
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(materials, f, indent=4, ensure_ascii=False)

def calculate_total(materials):
    total = 0
    for item in materials.values():
        try:
            total += item.get("quantite", 0) * item.get("prix_unitaire", 0)
        except TypeError:
            continue
    return total

def materials_to_dataframe(materials):
    rows = []
    for key, data in materials.items():
        row = {
            "Nom": key,
            "Quantité": data.get("quantite", 0),
            "Prix Unitaire (Ar)": data.get("prix_unitaire", 0),
            "Total (Ar)": data.get("quantite", 0) * data.get("prix_unitaire", 0)
        }
        rows.append(row)
    return pd.DataFrame(rows)

def export_to_excel(materials, filename="devis_export.xlsx"):
    df = materials_to_dataframe(materials)
    df.to_excel(filename, index=False)

def export_to_csv(materials, filename="devis_export.csv"):
    df = materials_to_dataframe(materials)
    df.to_csv(filename, index=False, encoding="utf-8-sig")
