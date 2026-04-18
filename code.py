import streamlit as st
import yfinance as yf
from datetime import date, datetime
import pytz
import random
import string
from hijri_converter import Gregorian

# 1. إعدادات الصفحة
st.set_page_config(page_title="Assistant Digital Pro", page_icon="🤖", layout="wide")

# تنسيق CSS احترافي (النسخة الفاتحة والمريحة)
st.markdown("""
    <style>
    .stApp { background-color: #f8fafc; color: #1e293b; }
    .block-container { padding-top: 2rem; max-width: 92%; }
    .stButton>button { 
        width: 100%; border-radius: 12px; 
        background: linear-gradient(45deg, #3b82f6, #2563eb); 
        color: white; border: none; font-weight: bold; height: 3.5rem; 
    }
    .card { 
        background: white; padding: 30px; border-radius: 20px; 
        border: 1px solid #e2e8f0; margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
    }
    h1, h2, h3 { color: #0f172a !important; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1>🤖 Assistant Digital Intelligent Pro</h1>", unsafe_allow_html=True)
st.write("---")

# القائمة الجانبية المطورة
with st.sidebar:
    st.header("⚙️ Menu des Outils")
    choice = st.radio("Sélectionnez une catégorie :", 
        ["📅 Calendrier Hijri", "🔢 Calculatrice Pro", "💹 Bourse & Crypto", "⏰ Horloge Mondiale", "🔐 Sécurité", "📝 Tâches"])

# --- 1. Calendrier Hijri ---
if choice == "📅 Calendrier Hijri":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    d = st.date_input("Choisir la date Grégorienne :", date.today())
    hijri = Gregorian(d.year, d.month, d.day).to_hijri()
    st.markdown(f"<h2>{hijri.day} {hijri.month_name()} {hijri.year} AH</h2>", unsafe_allow_html=True)
    st.write(f"<p style='text-align:center;'>Jour : {hijri.day_name()}</p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# --- 2. Calculatrice Pro ---
elif choice == "🔢 Calculatrice Pro":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    n1 = col1.number_input("Nombre 1", value=0.0)
    n2 = col2.number_input("Nombre 2", value=0.0)
    c1, c2, c3, c4, c5 = st.columns(5)
    res = None
    if c1.button("➕"): res = n1 + n2
    if c2.button("➖"): res = n1 - n2
    if c3.button("✖️"): res = n1 * n2
    if c4.button("➗"): res = round(n1/n2, 2) if n2 != 0 else "Erreur"
    if c5.button("%"): res = round((n1 * n2) / 100, 2)
    if res is not None: st.success(f"Résultat : {res}")
    st.markdown("</div>", unsafe_allow_html=True)

# --- 3. Bourse & Crypto ---
elif choice == "💹 Bourse & Crypto":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    symbol = st.text_input("Entrez le symbole (ex: BTC-USD, AAPL, GC=F for Gold):", "BTC-USD").upper()
    if st.button("Obtenir le prix"):
        try:
            data = yf.Ticker(symbol).history(period="1d")
            price = round(data['Close'].iloc[-1], 2)
            st.metric(label=f"Prix Actuel de {symbol}", value=f"{price} $")
        except: st.error("Symbole non trouvé.")
    st.markdown("</div>", unsafe_allow_html=True)

# --- 4. Horloge Mondiale ---
elif choice == "⏰ Horloge Mondiale":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    zones = {'Rabat/Paris': 'Africa/Casablanca', 'New York': 'America/New_York', 'London': 'Europe/London', 'Dubai': 'Asia/Dubai', 'Tokyo': 'Asia/Tokyo'}
    for city, tz in zones.items():
        now = datetime.now(pytz.timezone(tz)).strftime("%H:%M:%S")
        st.write(f"**{city}** : {now}")
    st.markdown("</div>", unsafe_allow_html=True)

# --- 5. Sécurité (Password Generator) ---
elif choice == "🔐 Sécurité":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    length = st.slider("Longueur du mot de passe :", 8, 32, 12)
    if st.button("Générer un mot de passe fort"):
        chars = string.ascii_letters + string.digits + string.punctuation
        pwd = ''.join(random.choice(chars) for i in range(length))
        st.code(pwd)
        st.info("Copiez ce mot de passe et gardez-le en sécurité.")
    st.markdown("</div>", unsafe_allow_html=True)

# --- 6. Tâches ---
elif choice == "📝 Tâches":
    st.header("📝 Liste de Tâches")
    if 'tasks' not in st.session_state: st.session_state.tasks = []
    t = st.text_input("Ajouter une tâche :")
    if st.button("Ajouter"):
        if t: st.session_state.tasks.append(t); st.rerun()
    for i, task in enumerate(st.session_state.tasks):
        st.markdown(f"<div style='background:white; padding:10px; border-radius:10px; margin-bottom:5px; border:1px solid #e2e8f0;'>✅ {task}</div>", unsafe_allow_html=True)

st.divider()
st.caption("📢 Assistant Digital Pro - Votre compagnon quotidien intelligent")
