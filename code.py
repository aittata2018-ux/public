import streamlit as st
import pandas as pd
from datetime import date
from hijri_converter import Gregorian

# 1. إعدادات الصفحة - الواجهة الواسعة لمحاكاة الورقة
st.set_page_config(page_title="محاكي الكشوفات الإدارية", page_icon="📝", layout="wide")

# تنسيق CSS دقيق لمحاكاة الوثيقة الرسمية
st.markdown("""
    <style>
    .stApp { background-color: white; color: black; }
    .report-header { text-align: left; font-family: 'Times New Roman', serif; font-weight: bold; font-size: 15px; line-height: 1.2; }
    .report-title { text-align: center; border: 2px solid black; padding: 8px; margin: 20px auto; width: 45%; font-weight: bold; font-size: 20px; }
    .table-container { width: 100%; border-collapse: collapse; margin-top: 20px; }
    .table-container th { background-color: #e8eefc; border: 1px solid black; padding: 10px; text-align: center; font-style: italic; font-size: 14px; }
    .table-container td { border: 1px solid black; padding: 10px; text-align: center; font-weight: bold; font-size: 14px; }
    .yellow-box { background-color: #ffff00; border: 1px solid black; padding: 5px 20px; font-weight: bold; text-align: center; display: inline-block; font-size: 18px; }
    </style>
    """, unsafe_allow_html=True)

# القائمة الجانبية للتنقل بين المحاكي والحاسبة
with st.sidebar:
    st.header("⚙️ لوحة التحكم")
    choice = st.radio("اختر الأداة:", ["📄 محاكي كشف الأجور", "🔢 الحاسبة الذكية"])

# --- 1. محاكي كشف الأجور (لتغيير المعطيات فقط) ---
if choice == "📄 محاكي كشف الأجور":
    st.sidebar.divider()
    st.sidebar.subheader("✍️ تغيير معطيات الكشف")
    
    # معطيات عامة قابلة للتغيير
    prov = st.sidebar.text_input("Province", "AL HAOUZ")
    comm = st.sidebar.text_input("Commune", "IMGDAL")
    prix_h = st.sidebar.number_input("سعر الساعة (Prix Heure)", value=17.92)
    period = st.sidebar.text_input("الفترة (Période)", "01/01/2026 au : 31/03/2026")

    # إدارة جدول الموظفين (المعطيات المتغيرة)
    if 'data_list' not in st.session_state:
        st.session_state.data_list = [
            {"nom": "IDBOUNITE ABDERAHIME", "cin": "G12345", "heures": 8, "jours": 66},
            {"nom": "ABDLAZIZ OUAKRIME", "cin": "G67890", "heures": 8, "jours": 48},
            {"nom": "MOHAMED IDBOUSABOUNE", "cin": "G11223", "heures": 8, "jours": 14}
        ]

    # إضافة موظف جديد لتغيير محتوى الجدول
    with st.sidebar.expander("👤 إضافة/تعديل موظف"):
        new_nom = st.text_input("Nom Complet")
        new_cin = st.text_input("CIN")
        new_h = st.number_input("ساعات اليوم", value=8)
        new_j = st.number_input("عدد الأيام", value=1)
        if st.button("إضافة للجدول"):
            st.session_state.data_list.append({"nom": new_nom.upper(), "cin": new_cin.upper(), "heures": new_h, "jours": new_j})
            st.rerun()
    
    if st.sidebar.button("🗑️ مسح الجدول بالكامل"):
        st.session_state.data_list = []
        st.rerun()

    # --- عرض المحاكاة الرسمية ---
    st.markdown(f"""
    <div class="report-header">
        MINISTERE DE L'INTERIEUR<br>
        PROVINCE {prov}<br>
        CERCLE ASNI<br>
        CAIDAT OUIRGUANE<br>
        *****<br>
        COMMUNE {comm}
    </div>
    <div class="report-title">ÉTAT DE LA SOMME DUE</div>
    <div style="font-weight: bold; margin-bottom: 10px;">
        1° partie, chap 10, art/prog 20/20, projet/action, 10 Ling, 14<br>
        Salaires des Agent Occasionnels du Mois de : {period}
    </div>
    """, unsafe_allow_html=True)

    # حساب المجموع الكلي بناءً على المعطيات الجديدة
    total_sum = sum(a['heures'] * prix_h * a['jours'] for a in st.session_state.data_list)

    st.markdown(f"""
    <div style="margin: 20px 0;">
        <span style="font-weight: bold; text-decoration: underline; font-size: 18px;">somme à payer à:</span>
        <span class="yellow-box">{total_sum:,.2f}</span>
    </div>
    """, unsafe_allow_html=True)

    # بناء الجدول التلقائي
    table_body = ""
    for a in st.session_state.data_list:
        daily = round(a['heures'] * prix_h, 2)
        prod = round(daily * a['jours'], 2)
        table_body += f"""
        <tr>
            <td>{a['nom']}</td>
            <td>{a['cin']}</td>
            <td>{a['heures']}</td>
            <td>{prix_h}</td>
            <td>{daily}</td>
            <td>{a['jours']}</td>
            <td>{prod}</td>
            <td style='color:#ccc;'>..........</td>
        </tr>"""

    st.markdown(f"""
    <table class="table-container">
        <tr>
            <th>Nom et Prenom</th><th>N° CIN</th><th>Heures</th><th>Prix Heures</th>
            <th>Salaire Journalier</th><th>Nombres de jour</th><th>PRODUIT</th><th>emargement</th>
        </tr>
        {table_body}
        <tr>
            <td colspan='6' style='text-align:center;'>TOTAL</td>
            <td class="yellow-box">{total_sum:,.2f}</td>
            <td></td>
        </tr>
    </table>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div style="display: flex; justify-content: space-between; margin-top: 60px; font-weight: bold;">
        <div>L'ORDONNATEUR</div>
        <div style="text-align: right;">A {comm} Le :{date.today().strftime('%d/%m/%Y')}<br><br>le Régisseur de Dépense</div>
    </div>
    """, unsafe_allow_html=True)

# --- 2. الحاسبة الذكية (تظل موجودة ومستقلة) ---
elif choice == "🔢 الحاسبة الذكية":
    st.header("🔢 الحاسبة والنسبة المئوية")
    n1 = st.number_input("الرقم الأول", value=0.0)
    n2 = st.number_input("الرقم الثاني", value=0.0)
    if st.button("احسب"):
        st.success(f"النتيجة: {n1 + n2}")

st.sidebar.divider()
st.sidebar.info("💡 غير المعطيات من اليسار ليتم تحديث المحاكاة تلقائياً.")
