import streamlit as st
import pandas as pd
from datetime import date

# 1. إعدادات الصفحة - الواجهة الواسعة
st.set_page_config(page_title="نظام الكشوفات الإدارية", page_icon="📝", layout="wide")

# تنسيق CSS لمحاكاة الوثيقة الرسمية
st.markdown("""
    <style>
    .stApp { background-color: white; color: black; }
    .report-header { text-align: left; font-family: Arial; font-weight: bold; font-size: 14px; line-height: 1.2; }
    .report-title { text-align: center; border: 2px solid black; padding: 5px; margin: 20px auto; width: 40%; font-weight: bold; font-size: 18px; }
    .table-container { width: 100%; border-collapse: collapse; margin-top: 20px; }
    .table-container th { background-color: #e8eefc; border: 1px solid black; padding: 8px; text-align: center; font-style: italic; font-size: 13px; }
    .table-container td { border: 1px solid black; padding: 8px; text-align: center; font-weight: bold; font-size: 13px; color: black; }
    .yellow-box { background-color: #ffff00; border: 1px solid black; padding: 5px 15px; font-weight: bold; text-align: center; display: inline-block; }
    </style>
    """, unsafe_allow_html=True)

# --- القائمة الجانبية للتحكم ---
with st.sidebar:
    st.header("📝 إعدادات الكشف")
    prov = st.text_input("Province", "AL HAOUZ")
    commune = st.text_input("Commune", "IMGDAL")
    date_range = st.text_input("Période", "01/01/2026 au : 31/03/2026")
    prix_h = st.number_input("Prix Heure", value=17.92)

    st.divider()
    st.subheader("👤 بيانات الموظفين")
    if 'agents' not in st.session_state:
        st.session_state.agents = [
            {"nom": "IDBOUNITE ABDERAHIME", "cin": "G12345", "heures": 8, "jours": 66},
            {"nom": "ABDLAZIZ OUAKRIME", "cin": "G67890", "heures": 8, "jours": 48},
            {"nom": "MOHAMED IDBOUSABOUNE", "cin": "G11223", "heures": 8, "jours": 14}
        ]

    with st.expander("إضافة موظف"):
        n_nom = st.text_input("Nom")
        n_cin = st.text_input("CIN")
        n_h = st.number_input("H/Jour", 8)
        n_j = st.number_input("Jours", 1)
        if st.button("إضافة"):
            st.session_state.agents.append({"nom": n_nom, "cin": n_cin, "heures": n_h, "jours": n_j})
            st.rerun()

# --- عرض الوثيقة الرسمية ---
# 1. الترويسة
st.markdown(f"""
<div class="report-header">
    MINISTERE DE L'INTERIEUR<br>
    PROVINCE {prov}<br>
    CERCLE ASNI<br>
    CAIDAT OUIRGUANE<br>
    *****<br>
    COMMUNE {commune}
</div>
<div class="report-title">ÉTAT DE LA SOMME DUE</div>
<div style="font-size: 13px; font-weight: bold; margin-bottom: 10px;">
    1° partie, chap 10, art/prog 20/20...<br>
    Salaires des Agent Occasionnels du Mois de : {date_range}
</div>
""", unsafe_allow_html=True)

# 2. حساب المجموع وسطر الدفع
total_gen = sum(a['heures'] * prix_h * a['jours'] for a in st.session_state.agents)

st.markdown(f"""
<div style="margin: 15px 0;">
    <span style="font-weight: bold; text-decoration: underline;">somme à payer à:</span>
    <span class="yellow-box">{total_gen:,.2f}</span>
</div>
""", unsafe_allow_html=True)

# 3. بناء الجدول (الجزء الذي كان يظهر ككود)
table_html = """
<table class="table-container">
    <tr>
        <th>Nom et Prenom</th>
        <th>N° CIN</th>
        <th>Heures</th>
        <th>Prix Heures</th>
        <th>Salaire Journalier</th>
        <th>Nombres de jour</th>
        <th>PRODUIT</th>
        <th>emargement</th>
    </tr>
"""

for a in st.session_state.agents:
    daily = round(a['heures'] * prix_h, 2)
    prod = round(daily * a['jours'], 2)
    table_html += f"""
    <tr>
        <td>{a['nom']}</td>
        <td>{a['cin']}</td>
        <td>{a['heures']}</td>
        <td>{prix_h}</td>
        <td>{daily}</td>
        <td>{a['jours']}</td>
        <td>{prod}</td>
        <td style="color: #ccc;">............</td>
    </tr>
    """

table_html += f"""
    <tr>
        <td colspan="6" style="text-align: center;">TOTAL</td>
        <td class="yellow-box">{total_gen:,.2f}</td>
        <td></td>
    </tr>
</table>
"""

# عرض الجدول النهائي
st.markdown(table_html, unsafe_allow_html=True)

# 4. التوقيعات
st.markdown(f"""
<div style="display: flex; justify-content: space-between; margin-top: 50px; font-weight: bold;">
    <div>L'ORDONNATEUR</div>
    <div style="text-align: right;">
        A {commune} Le :{date.today().strftime('%d/%m/%Y')}<br><br>
        le Régisseur de Dépense
    </div>
</div>
""", unsafe_allow_html=True)
