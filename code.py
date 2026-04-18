import streamlit as st
import yfinance as yf
from datetime import date
from hijri_converter import Gregorian

# 1. Configuration de la page - Layout Large
st.set_page_config(page_title="Assistant Digital", page_icon="🤖", layout="wide")

# Style CSS pour une interface moderne et large
st.markdown("""
    <style>
    .block-container { padding-top: 2rem; max-width: 92%; }
    .stApp { background: linear-gradient(to bottom, #0f172a, #1e293b); color: white; }
    .stButton>button { width: 100%; border-radius: 12px; background: linear-gradient(45deg, #00f2fe, #4facfe); color: white; border: none; font-weight: bold; height: 3.5rem; font-size: 18px; }
    .metric-card { background: rgba(255, 255, 255, 0.05); padding: 20px; border-radius: 15px; border: 1px solid rgba(79, 172, 254, 0.3); }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; font-size: 3rem;'>🤖 Assistant Digital Intelligent</h1>", unsafe_allow_html=True)
st.write("---")

# Barre latérale (Sidebar)
with st.sidebar:
    st.header("⚙️ Contrôle")
    choice = st.radio("Choisir l'outil :", ["📅 Calendrier Hijri", "🔢 Calculatrice", "💱 Bourse", "📝 Tâches"])

# --- 1. Calendrier Hijri (Version Française Large) ---
if choice == "📅 Calendrier Hijri":
    st.markdown("<h2 style='text-align: center;'>📅 Convertisseur de Date Hijri</h2>", unsafe_allow_html=True)
    col_sp1, col_in, col_sp2 = st.columns([1, 2, 1])
    with col_in:
        d = st.date_input("Choisir la date Grégorienne :", date.today())
    
    hijri = Gregorian(d.year, d.month, d.day).to_hijri()
    
    st.markdown(f"""
    <div style="background: rgba(255, 255, 255, 0.05); padding: 40px; border-radius: 20px; text-align: center; border: 2px solid rgba(79, 172, 254, 0.3); margin: 20px 0;">
        <h2 style='color: #4facfe; margin-bottom: 20px; font-size: 2.2rem;'>Date Hijri</h2>
        <div style='margin: 30px 0;'>
            <p style='font-size: 50px; font-weight: bold; color: #ffffff; margin: 0;'>{hijri.day} {hijri.month_name()} {hijri.year} AH</p>
            <p style='font-size: 20px; color: #4facfe; letter-spacing: 2px;'>CALENDRIER HIJRI</p>
        </div>
        <hr style='border: 0.5px solid rgba(255,255,255,0.1); width: 60%; margin: 30px auto;'>
        <p style='font-size: 22px; opacity: 0.9;'>Correspond au : <b>{d.day}/{d.month}/{d.year}</b></p>
    </div>
    """, unsafe_allow_html=True)

# --- 2. Calculatrice ---
elif choice == "🔢 Calculatrice":
    st.header("🔢 Calculatrice Intelligente")
    col1, col2 = st.columns(2)
    n1 = col1.number_input("Nombre 1", value=0.0)
    n2 = col2.number_input("Nombre 2", value=0.0)
    c1, c2, c3, c4 = st.columns(4)
    res = None
    if c1.button("➕"): res = n1 + n2
    if c2.button("➖"): res = n1 - n2
    if c3.button("✖️"): res = n1 * n2
    if c4.button("➗"): res = round(n1/n2, 2) if n2 != 0 else "Erreur"
    if res is not None: st.success(f"Résultat : {res}")

# --- 3. Bourse (Taux de Change Live) ---
elif choice == "💱 Bourse":
    st.header("💱 Taux de Change en Direct")
    
    # Dictionnaire des devises
    currencies = {"Maroc (MAD)": "USDMAD=X", "Egypte (EGP)": "USDEGP=X", "Europe (EUR)": "USDEUR=X", "Arabie S. (SAR)": "USDSAR=X"}
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
    <div class="metric-card">
        <h3 style='margin:0; color:#4facfe;'>Résultat de conversion</h3>
        <p style='font-size: 35px; font-weight: bold; margin: 10px 0;'>{round(amount*rate, 2)} {target.split()[-1]}</p>
        <p style='opacity:0.7;'>Taux actuel : 1 USD = {rate}</p>
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
        col_t, col_b = st.columns([0.85, 0.15])
        col_t.write(f"✅ {task}")
        if col_b.button("Supprimer", key=f"del_{i}"):
            st.session_state.tasks.pop(i); st.rerun()
