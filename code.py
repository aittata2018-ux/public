import streamlit as st
import pandas as pd
from datetime import date

# 1. إعدادات الصفحة - الواجهة الواسعة
st.set_page_config(page_title="نظام تسيير الأجور الإداري", page_icon="📝", layout="wide")

# تنسيق CSS لمحاكاة الوثيقة الرسمية والألوان المطلوبة
st.markdown("""
    <style>
    .stApp { background-color: white; color: black; }
    .report-header { text-align: left; font-family: Arial; font-weight: bold; font-size: 14px; }
    .report-title { text-align: center; border: 2px solid black; padding: 5px; margin: 20px auto; width: 50%; font-weight: bold; }
    .table-container { width: 100%; border-collapse: collapse; margin-top: 20px; }
    .table-container th { background-color: #e8eefc; border: 1px solid black; padding: 8px; text-align: center; font-style: italic; font-size: 13px; }
    .table-container td { border: 1px solid black; padding: 8px; text-align: center; font-weight: bold; font-size: 13px; }
    .yellow-box { background-color: #ffff00; border: 1px solid black; padding: 5px; font-weight: bold; text-align: center; }
    .footer-section { display: flex; justify-content: space-between; margin-top: 40px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- القائمة الجانبية للتحكم بالمعلومات ---
st.sidebar.header("📝 إعدادات الكشف الإداري")
prov = st.sidebar.text_input("Province", "AL HAOUZ")
commune = st.sidebar.text_input("Commune", "IMGDAL")
chapitre = st.sidebar.text_input("Détails Chapitre", "1° partie, chap 10, art/prog 20/20...")
date_range = st.sidebar.text_input("Période", "01/01/2026 au : 31/03/2026")
prix_h = st.sidebar.number_input("Prix Heure (Fixe)", value=17.92)

# --- نظام إدخال بيانات الموظفين (المعلومات المتحكم فيها) ---
st.sidebar.markdown("---")
st.sidebar.subheader("👤 إضافة/تعديل الموظفين")
if 'agents' not in st.session_state:
    # بيانات افتراضية بناءً على الصورة
    st.session_state.agents = [
        {"nom": "IDBOUNITE ABDERAHIME", "cin": "G12345", "heures": 8, "jours": 66},
        {"nom": "ABDLAZIZ OUAKRIME", "cin": "G67890", "heures": 8, "jours": 48},
        {"nom": "MOHAMED IDBOUSABOUNE", "cin": "G11223", "heures": 8, "jours": 14},
        {"nom": "YOUSSEF AIT TATA", "cin": "G44556", "heures": 7, "jours": 60},
        {"nom": "MALIKA AIT ELHAJ", "cin": "G77889", "heures": 4, "jours": 12}
    ]

with st.sidebar.expander("إضافة موظف جديد"):
    new_nom = st.text_input("Nom et Prenom")
    new_cin = st.text_input("N° CIN")
    new_h = st.number_input("Heures/Jour", value=8)
    new_j = st.number_input("Nombre de jours", value=1)
    if st.button("إضافة للجدول"):
        st.session_state.agents.append({"nom": new_nom, "cin": new_cin, "heures": new_h, "jours": new_j})
        st.rerun()

if st.sidebar.button("🗑️ مسح الجدول والبدء من جديد"):
    st.session_state.agents = []
    st.rerun()

# --- عرض الوثيقة الرسمية ---
# الهيدر (جهة اليسار)
st.markdown(f"""
<div class="report-header">
    MINISTERE DE L'INTERIEUR<br>
    PROVINCE {prov}<br>
    CERCLE ASNI<br>
    CAIDAT OUIRGUANE<br>
    *****<br>
    COMMUNE {commune}
</div>
""", unsafe_allow_html=True)

# العنوان الرئيسي
st.markdown('<div class="report-title">ÉTAT DE LA SOMME DUE</div>', unsafe_allow_html=True)

# تفاصيل الكشف
st.markdown(f"""
<div style="font-size: 13px; font-weight: bold;">
    {chapitre}<br>
    Salaires des Agent Occasionnels du Mois de : {date_range}
</div>
""", unsafe_allow_html=True)

# حساب المجموع الكلي مسبقاً
total_general = sum(a['heures'] * prix_h * a['jours'] for a in st.session_state.agents)

# سطر "Somme à payer"
st.markdown(f"""
<div style="display: flex; align-items: center; margin-top: 15px;">
    <div style="font-weight: bold; text-decoration: underline; margin-right: 10px;">somme à payer à:</div>
    <div class="yellow-box" style="width: 120px;">{total_general:,.2f}</div>
</div>
""", unsafe_allow_html=True)

# --- بناء الجدول ---
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

for agent in st.session_state.agents:
    daily = round(agent['heures'] * prix_h, 2)
    produit = round(daily * agent['jours'], 2)
    table_html += f"""
    <tr>
        <td>{agent['nom']}</td>
        <td>{agent['cin']}</td>
        <td>{agent['heures']}</td>
        <td>{prix_h}</td>
        <td>{daily}</td>
        <td>{agent['jours']}</td>
        <td>{produit}</td>
        <td style="color: #ccc;">............</td>
    </tr>
    """

# سطر التوتال الأسفل
table_html += f"""
    <tr>
        <td colspan="6" style="text-align: center;">TOTAL</td>
        <td class="yellow-box">{total_general:,.2f}</td>
        <td></td>
    </tr>
</table>
"""

st.markdown(table_html, unsafe_allow_html=True)

# الفوتر (التوقيعات)
st.markdown(f"""
<div class="footer-section">
    <div>
        L'ORDONNATEUR
    </div>
    <div style="text-align: right;">
        A {commune} Le :{date.today().strftime('%d/%m/%Y')}<br><br>
        le Régisseur de Dépense
    </div>
</div>
""", unsafe_allow_html=True)

# زر للطباعة
if st.button("🖨️ طباعة الكشف"):
    st.write("استخدم اختصار (Ctrl + P) لطباعة هذه الصفحة كملف PDF رسمي.")
