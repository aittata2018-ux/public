import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import date
from hijri_converter import Gregorian

# 1. إعدادات الصفحة - الواجهة الواسعة
st.set_page_config(page_title="مساعدك الرقمي الشامل", page_icon="🤖", layout="wide")

# تنسيق CSS احترافي لجميع الأدوات
st.markdown("""
    <style>
    .stApp { background-color: #f8fafc; color: #1e293b; }
    .card { background: white; padding: 25px; border-radius: 15px; border: 1px solid #e2e8f0; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05); color: #1e293b; }
    .stButton>button { width: 100%; border-radius: 12px; background: linear-gradient(45deg, #3b82f6, #2563eb); color: white; border: none; font-weight: bold; height: 3.5rem; }
    
    /* تنسيق الوثيقة الإدارية الرسمية */
    .report-header { text-align: left; font-family: Arial; font-weight: bold; font-size: 14px; line-height: 1.2; color: black; }
    .report-title { text-align: center; border: 2px solid black; padding: 5px; margin: 20px auto; width: 40%; font-weight: bold; font-size: 18px; color: black; }
    .table-container { width: 100%; border-collapse: collapse; margin-top: 20px; }
    .table-container th { background-color: #e8eefc; border: 1px solid black; padding: 8px; text-align: center; font-style: italic; font-size: 13px; color: black; }
    .table-container td { border: 1px solid black; padding: 8px; text-align: center; font-weight: bold; font-size: 13px; color: black; }
    .yellow-box { background-color: #ffff00; border: 1px solid black; padding: 5px 15px; font-weight: bold; text-align: center; display: inline-block; color: black; }
    </style>
    """, unsafe_allow_html=True)

# العنوان الرئيسي للمنصة
st.markdown("<h1 style='text-align: center; color: #0f172a;'>🤖 مساعدك الرقمي الشامل</h1>", unsafe_allow_html=True)
st.write("---")

# القائمة الجانبية (تضم كل الأدوات بما فيها الكشف الإداري الجديد)
with st.sidebar:
    st.header("⚙️ لوحة التحكم")
    choice = st.radio("اختر الأداة المطلوبة:", 
        ["📅 محول التاريخ الهجري", "📄 كشف الأجور الإداري", "🔢 الحاسبة المتطورة", "💱 بورصة العملات", "📝 مفكرة المهام"])

# --- 1. محول التاريخ الهجري ---
if choice == "📅 محول التاريخ الهجري":
    st.header("📅 Convertisseur Hijri")
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    d = st.date_input("Choisir la date Grégorienne :", date.today())
    hijri = Gregorian(d.year, d.month, d.day).to_hijri()
    st.markdown(f"<h2 style='text-align:center; color:#2563eb;'>{hijri.day} {hijri.month_name()} {hijri.year} AH</h2>", unsafe_allow_html=True)
    st.write(f"<p style='text-align:center;'>Jour : {hijri.day_name()}</p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# --- 2. كشف الأجور الإداري (النموذج الرسمي من الصورة) ---
elif choice == "📄 كشف الأجور الإداري":
    st.subheader("📑 État de la Somme Due (Modèle Officiel)")
    
    # إعدادات الكشف من القائمة الجانبية الإضافية
    with st.expander("⚙️ إعدادات الوثيقة الإدارية"):
        prov = st.text_input("Province", "AL HAOUZ")
        commune = st.text_input("Commune", "IMGDAL")
        date_range = st.text_input("Période", "01/01/2026 au : 31/03/2026")
        prix_h = st.number_input("Prix Heure", value=17.92)

    if 'agents' not in st.session_state:
        st.session_state.agents = [
            {"nom": "IDBOUNITE ABDERAHIME", "cin": "G12345", "heures": 8, "jours": 66},
            {"nom": "ABDLAZIZ OUAKRIME", "cin": "G67890", "heures": 8, "jours": 48},
            {"nom": "MOHAMED IDBOUSABOUNE", "cin": "G11223", "heures": 8, "jours": 14}
        ]

    with st.expander("👤 إضافة موظف جديد للجدول"):
        n_nom = st.text_input("Nom et Prénom")
        n_cin = st.text_input("N° CIN")
        n_h = st.number_input("Heures/Jour", 8)
        n_j = st.number_input("Nombre de Jours", 1)
        if st.button("إضافة"):
            st.session_state.agents.append({"nom": n_nom.upper(), "cin": n_cin.upper(), "heures": n_h, "jours": n_j})
            st.rerun()

    # عرض الوثيقة
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
    <div style="font-size: 13px; font-weight: bold; margin-bottom: 10px; color: black;">
        1° partie, chap 10, art/prog 20/20...<br>
        Salaires des Agent Occasionnels du Mois de : {date_range}
    </div>
    """, unsafe_allow_html=True)

    total_gen = sum(a['heures'] * prix_h * a['jours'] for a in st.session_state.agents)

    st.markdown(f"""
    <div style="margin: 15px 0; color: black;">
        <span style="font-weight: bold; text-decoration: underline;">somme à payer à:</span>
        <span class="yellow-box">{total_gen:,.2f}</span>
    </div>
    """, unsafe_allow_html=True)

    # بناء الجدول
    table_html = """
    <table class="table-container">
        <tr>
            <th>Nom et Prenom</th><th>N° CIN</th><th>Heures</th><th>Prix Heures</th>
            <th>Salaire Journalier</th><th>Nombres de jour</th><th>PRODUIT</th><th>emargement</th>
        </tr>
    """
    for a in st.session_state.agents:
        daily = round(a['heures'] * prix_h, 2)
        prod = round(daily * a['jours'], 2)
        table_html += f"<tr><td>{a['nom']}</td><td>{a['cin']}</td><td>{a['heures']}</td><td>{prix_h}</td><td>{daily}</td><td>{a['jours']}</td><td>{prod}</td><td style='color:#ccc;'>..........</td></tr>"
    
    table_html += f"<tr><td colspan='6' style='text-align:center;'>TOTAL</td><td class='yellow-box'>{total_gen:,.2f}</td><td></td></tr></table>"
    
    st.markdown(table_html, unsafe_allow_html=True)

    st.markdown(f"""
    <div style="display: flex; justify-content: space-between; margin-top: 50px; font-weight: bold; color: black;">
        <div>L'ORDONNATEUR</div>
        <div style="text-align: right;">A {commune} Le :{date.today().strftime('%d/%m/%Y')}<br><br>le Régisseur de Dépense</div>
    </div>
    """, unsafe_allow_html=True)

# --- 3. الحاسبة المتطورة ---
elif choice == "🔢 الحاسبة المتطورة":
    st.header("🔢 الحاسبة والنسبة المئوية")
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    n1 = st.number_input("الرقم الأول", value=0.0)
    n2 = st.number_input("الرقم الثاني", value=0.0)
    c1, c2, c3, c4 = st.columns(4)
    res = None
    if c1.button("➕"): res = n1 + n2
    if c2.button("➖"): res = n1 - n2
    if c3.button("✖️"): res = n1 * n2
    if c4.button("➗"): res = round(n1/n2, 2) if n2 != 0 else "خطأ"
    if res is not None: st.success(f"النتيجة: {res}")
    st.markdown("</div>", unsafe_allow_html=True)

# --- 4. بورصة العملات ---
elif choice == "💱 بورصة العملات":
    st.header("💱 أسعار العملات المباشرة")
    curr_dict = {"المغرب (MAD)": "USDMAD=X", "مصر (EGP)": "USDEGP=X", "السعودية (SAR)": "USDSAR=X"}
    target = st.selectbox("اختر العملة:", list(curr_dict.keys()))
    @st.cache_data(ttl=600)
    def get_rate(sym):
        try: return round(yf.Ticker(sym).history(period="1d")['Close'].iloc[-1], 2)
        except: return 10.0
    rate = get_rate(curr_dict[target])
    usd = st.number_input("المبلغ بالدولار ($)", value=1.0)
    st.metric(label=f"القيمة بـ {target}", value=f"{round(usd*rate, 2)}", delta=f"سعر الصرف: {rate}")

# --- 5. مفكرة المهام ---
elif choice == "📝 مفكرة المهام":
    st.header("📝 قائمة المهام اليومية")
    if 'tasks' not in st.session_state: st.session_state.tasks = []
    t = st.text_input("أضف مهمة:")
    if st.button("إضافة"):
        if t: st.session_state.tasks.append(t); st.rerun()
    for i, task in enumerate(st.session_state.tasks):
        st.write(f"✅ {task}")

st.divider()
st.caption("📢 مساعدك الرقمي الشامل - منصة الأدوات المتكاملة")
