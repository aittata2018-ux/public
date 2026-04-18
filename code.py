import streamlit as st
import yfinance as yf
from datetime import date
from hijri_converter import Gregorian

# 1. إعدادات الصفحة - الواجهة الواسعة
st.set_page_config(page_title="Assistant Digital", page_icon="🤖", layout="wide")

# تنسيق CSS جديد: ألوان فاتحة، مريحة، وعصرية
st.markdown("""
    <style>
    /* خلفية التطبيق فاتحة وهادئة */
    .stApp {
        background-color: #f8fafc;
        color: #1e293b;
    }
    
    /* توسيع الحاوية */
    .block-container { padding-top: 2rem; max-width: 90%; }
    
    /* تصميم الأزرار: أزرق احترافي */
    .stButton>button { 
        width: 100%; border-radius: 12px; 
        background: linear-gradient(45deg, #3b82f6, #2563eb); 
        color: white; border: none; font-weight: bold; 
        height: 3.5rem; font-size: 18px; transition: 0.3s;
    }
    .stButton>button:hover { 
        background: linear-gradient(45deg, #2563eb, #1d4ed8); 
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.2); 
    }
    
    /* تصميم البطاقات: أبيض مع ظل خفيف */
    .card { 
        background: white; 
        padding: 40px; border-radius: 20px; 
        text-align: center; border: 1px solid #e2e8f0; 
        margin: 20px 0; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    
    /* تخصيص نصوص العناوين */
    h1, h2, h3 { color: #0f172a !important; }
    
    /* تعديل شريط التنقل الجانبي */
    .css-1d391kg { background-color: #ffffff !important; }
    </style>
    """, unsafe_allow_html=True)

# العنوان الرئيسي
st.markdown("<h1 style='text-align: center; font-size: 3rem;'>🤖 Assistant Digital Intelligent</h1>", unsafe_allow_html=True)
st.write("---")

# القائمة الجانبية
with st.sidebar:
    st.header("⚙️ Contrôle")
    choice = st.radio("Choisir l'outil :", ["📅 Calendrier Hijri", "🔢 Calculatrice", "💱 Bourse", "📝 Tâches"])

# --- 1. Calendrier Hijri (Light Version) ---
if choice == "📅 Calendrier Hijri":
    st.markdown("<h2 style='text-align: center;'>📅 Convertisseur de Date Hijri</h2>", unsafe_allow_html=True)
    
    col_sp1, col_in, col_sp2 = st.columns([1, 2, 1])
    with col_in:
        d = st.date_input("Choisir la date Grégorienne :", date.today())
    
    hijri = Gregorian(d.year, d.month, d.day).to_hijri()
    
    st.markdown(f"""
    <div class="card">
        <h2 style='color: #2563eb; margin-bottom: 20px; font-size: 2.2rem;'>Date Hijri</h2>
        <div style='margin: 30px 0;'>
            <p style='font-size: 55px; font-weight: bold; color: #0f172a; margin: 0;'>
                {hijri.day} {hijri.month_name()} {hijri.year} AH
            </p>
            <p style='font-size: 18px; color: #64748b; letter-spacing: 3px; font-weight: bold;'>CALENDRIER HIJRI</p>
        </div>
        <hr style='border: 0.5px solid #e2e8f0; width: 60%; margin: 30px auto;'>
        <p style='font-size: 22px; color: #475569;'>
            Correspond au : <b style='color: #0f172a;'>{d.day}/{d.month}/{d.year}</b>
        </p>
    </div>
    """, unsafe_allow_html=True)
    st.success(f"Jour : {hijri.day_name()}")

# --- 2. Calculatrice (Light Version) ---
elif choice == "🔢 Calculatrice":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.header("🔢 Calculatrice")
    col1, col2 = st.columns(2)
    n1 = col1.number_input("Nombre 1", value=0.0)
    n2 = col2.number_input("Nombre 2", value=0.0)
    st.write("### Opérations :")
    c1, c2, c3, c4 = st.columns(4)
    res = None
    if c1.button("➕"): res = n1 + n2
    if c2.button("➖"): res = n1 - n2
    if c3.button("✖️"): res = n1 * n2
    if c4.button("➗"): res = round(n1/n2, 2) if n2 != 0 else "Erreur"
    if res is not None: st.success(f"Résultat : {res}")
    st.markdown("</div>", unsafe_allow_html=True)

# --- 3. Bourse ---
elif choice == "💱 Bourse":
    st.header("💱 Taux de Change Live")
    currencies = {"Maroc (MAD)": "USDMAD=X", "Egypte (EGP)": "USDEGP=X", "Europe (EUR)": "USDEUR=X"}
    target = st.selectbox("Convertir USD ($) vers :", list(currencies.keys()))
    
    @st.cache_data(ttl=600)
    def get_rate(symbol):
        try:
            ticker = yf.Ticker(symbol)
            return round(ticker.history(period="1d")['Close'].iloc[-1], 2)
        except: return 10.0

    rate = get_rate(currencies[target])
    amount = st.number_input("Montant en USD ($)", value=1.0)
    
    st.markdown(f"""
    <div class="card">
        <h3 style='margin:0; color: #2563eb;'>Résultat</h3>
        <p style='font-size: 45px; font-weight: bold; color: #0f172a; margin: 15px 0;'>{round(amount*rate, 2)} {target.split()[-1]}</p>
        <p style='color: #64748b;'>1 USD = {rate} {target.split()[-1]}</p>
    </div>
    """, unsafe_allow_html=True)

# --- 4. Tâches ---
elif choice == "📝 Tâches":
    st.header("📝 Liste de Tâches")
    if 'tasks' not in st.session_state: st.session_state.tasks = []
    t = st.text_input("Ajouter une tâche :")
    if st.button("Ajouter"):
        if t: st.session_state.tasks.append(t); st.rerun()
    for i, task in enumerate(st.session_state.tasks):
        st.markdown(f"<div style='background:white; padding:10px; border-radius:10px; margin-bottom:5px; border:1px solid #e2e8f0;'>✅ {task}</div>", unsafe_allow_html=True)
