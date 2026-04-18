import streamlit as st
import pandas as pd
from datetime import date

# 1. إعدادات الصفحة - الواجهة الواسعة لمحاكاة الورقة الرسمية
st.set_page_config(page_title="نظام كشوفات الأجور - إمجدال", page_icon="📝", layout="wide")

# تنسيق CSS دقيق لمحاكاة نموذج الـ PDF الجديد
st.markdown("""
    <style>
    .stApp { background-color: white; color: black; }
    .report-header { text-align: left; font-family: 'Times New Roman', serif; font-weight: bold; font-size: 15px; line-height: 1.2; }
    .report-title { text-align: center; border: 1px solid black; padding: 5px; margin: 10px auto; width: 40%; font-weight: bold; font-size: 18px; }
    .table-container { width: 100%; border-collapse: collapse; margin-top: 20px; }
    .table-container th { background-color: #dbeafe; border: 1px solid black; padding: 10px; text-align: center; font-weight: bold; font-size: 14px; }
    .table-container td { border: 1px solid black; padding: 10px; text-align: center; font-weight: bold; font-size: 14px; height: 30px; }
    .yellow-box { background-color: #eab308; border: 1px solid black; padding: 5px 20px; font-weight: bold; text-align: center; display: inline-block; font-size: 18px; color: black; }
    .footer-section { display: flex; justify-content: space-between; margin-top: 50px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# القائمة الجانبية للتحكم في المعطيات (المعلومات المتحكم فيها)
with st.sidebar:
    st.header("⚙️ إعدادات النموذج")
    choice = st.radio("اختر الأداة:", ["📄 محاكي الكشف الرسمي", "🔢 الحاسبة الذكية"])
    
    if choice == "📄 محاكي الكشف الرسمي":
        st.divider()
        st.subheader("✍️ تعديل البيانات الإدارية")
        commune = st.text_input("Commune", "IMGDAL")
        periode = st.text_input("Période", "01/01/2026 au: 31/03/2026")
        prix_h = st.number_input("Prix Heures (سعر الساعة)", value=17.92)
        
        st.divider()
        st.subheader("👤 إدارة الموظفين")
        if 'agents' not in st.session_state:
            st.session_state.agents = [{"nom": "", "cin": "", "heures": 0, "jours": 0}]

        # إضافة سطر جديد للجدول
        if st.button("➕ إضافة موظف جديد"):
            st.session_state.agents.append({"nom": "", "cin": "", "heures": 0, "jours": 0})
        
        # مدخلات لكل موظف في القائمة الجانبية
        for i, agent in enumerate(st.session_state.agents):
            with st.expander(f"الموظف {i+1}"):
                agent['nom'] = st.text_input(f"Prenom et Nom", value=agent['nom'], key=f"nom_{i}")
                agent['cin'] = st.text_input(f"N° CIN", value=agent['cin'], key=f"cin_{i}")
                agent['heures'] = st.number_input(f"Heures", value=agent['heures'], key=f"h_{i}")
                agent['jours'] = st.number_input(f"Nombres de jour", value=agent['jours'], key=f"j_{i}")
        
        if st.button("🗑️ تفريغ الجدول"):
            st.session_state.agents = [{"nom": "", "cin": "", "heures": 0, "jours": 0}]
            st.rerun()

# --- 1. محاكاة كشف الأجور الرسمي ---
if choice == "📄 محاكي الكشف الرسمي":
    # الترويسة (Header) كما في الـ PDF
    st.markdown(f"""
    <div class="report-header">
        ROYAUME DU MAROC<br>
        MINISTERE DE L'INTERIEUR<br>
        PROVINCE AL HAOUZ<br>
        CERCLE ASNI<br>
        CAIDAT OUIRGUANE<br>
        *****<br>
        COMMUNE {commune}
    </div>
    <div class="report-title">ÉTAT DE LA SOMME DUE</div>
    <div style="font-weight: bold; margin-bottom: 20px; text-align: left; margin-left: 28%;">
        1° partie,chap 10 ,art/prog 20/20,projet/action,10 Ling,14<br>
        Salaires des Agent Occasionnels du Mois de : {periode}
    </div>
    """, unsafe_allow_html=True)

    # حساب المجموع الكلي
    total_val = sum(a['heures'] * prix_h * a['jours'] for a in st.session_state.agents)

    # سطر "somme à payer à"
    st.markdown(f"""
    <div style="margin: 20px 0; font-weight: bold;">
        <span>somme à payer à:</span>
        <span style="margin-left: 50px;">{total_val:,.2f}</span>
    </div>
    """, unsafe_allow_html=True)

    # بناء الجدول الرسمي
    table_html = """
    <table class="table-container">
        <thead>
            <tr>
                <th>Prenom et Nom</th>
                <th>N° CIN</th>
                <th>Heures</th>
                <th>Prix Heures</th>
                <th>Salaire Journalier</th>
                <th>Nombres de jour</th>
                <th>PRODUIT</th>
            </tr>
        </thead>
        <tbody>
    """

    for a in st.session_state.agents:
        daily = round(a['heures'] * prix_h, 2)
        prod = round(daily * a['jours'], 2)
        table_html += f"""
        <tr>
            <td>{a['nom'].upper()}</td>
            <td>{a['cin'].upper()}</td>
            <td>{a['heures'] if a['heures'] > 0 else ''}</td>
            <td>{prix_h if a['heures'] > 0 else ''}</td>
            <td>{daily if a['heures'] > 0 else ''}</td>
            <td>{a['jours'] if a['jours'] > 0 else ''}</td>
            <td>{prod if prod > 0 else ''}</td>
        </tr>
        """

    # سطر TOTAL النهائي
    table_html += f"""
        <tr>
            <td colspan="6" style="text-align: center; font-weight: bold;">TOTAL</td>
            <td class="yellow-box">{total_val:,.2f}</td>
        </tr>
        </tbody>
    </table>
    """

    st.markdown(table_html, unsafe_allow_html=True)

    # التذييل (Footer)
    st.markdown(f"""
    <div style="margin-top: 20px; font-weight: bold;">Relevant à la somme de:=</div>
    <div class="footer-section">
        <div>
            certifié conforme aux attachements tenues<br><br><br>
            L'ORDONNATEUR
        </div>
        <div style="text-align: right;">
            A {commune} Le :{date.today().strftime('%d/%m/%Y')}<br><br><br>
            le Régisseur de Dépense
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- 2. الحاسبة الذكية ---
elif choice == "🔢 الحاسبة الذكية":
    st.header("🔢 الحاسبة والنسبة المئوية")
    n1 = st.number_input("الرقم الأول", value=0.0)
    n2 = st.number_input("الرقم الثاني", value=0.0)
    if st.button("احسب المجموع"):
        st.success(f"النتيجة: {n1 + n2}")

st.sidebar.divider()
st.sidebar.info("💡 ملاحظة: يمكنك طباعة هذا الكشف بالضغط على Ctrl + P")
