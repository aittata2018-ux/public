import streamlit as st
import yfinance as yf
from datetime import date
from hijri_converter import Gregorian

# 1. إعدادات الصفحة - الواجهة الواسعة
st.set_page_config(page_title="مساعدك الرقمي الذكي", page_icon="🤖", layout="wide")

# تنسيق الجماليات (CSS)
st.markdown("""
    <style>
    .block-container { padding-top: 2rem; max-width: 90%; }
    .stApp { background: linear-gradient(to bottom, #0f172a, #1e293b); color: white; }
    .stButton>button { width: 100%; border-radius: 12px; background: linear-gradient(45deg, #00f2fe, #4facfe); color: white; border: none; font-weight: bold; height: 3.5rem; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; font-size: 3rem;'>🤖 مساعدك الرقمي الذكي</h1>", unsafe_allow_html=True)
st.write("---")

# القائمة الجانبية
with st.sidebar:
    st.header("⚙️ لوحة التحكم")
    choice = st.radio("Choisir l'outil :", ["📅 Calendrier Hijri", "🔢 Calculatrice", "💱 Bourse", "📝 Tâches"])

# --- 1. محول التاريخ الهجري (النسخة الفرنسية المتسعة) ---
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
            <p style='font-size: 50px; font-weight: bold; color: #ffffff; margin: 0;'>
                {hijri.day} {hijri.month_name()} {hijri.year} AH
            </p>
            <p style='font-size: 20px; color: #4facfe; letter-spacing: 2px;'>CALENDRIER HIJRI</p>
        </div>
        <hr style='border: 0.5px solid rgba(255,255,255,0.1); width: 60%; margin: 30px auto;'>
        <p style='font-size: 22px; opacity: 0.9;'>
            Correspond au : <b>{d.day}/{d.month}/{d.year}</b>
        </p>
    </div>
    """, unsafe_allow_html=True)
    st.success(f"Jour : {hijri.day_name()}")

# --- باقي الأقسام لضمان التشغيل ---
elif choice == "🔢 Calculatrice":
    st.header("🔢 Calculatrice")
    n1 = st.number_input("Nombre 1", value=0.0)
    n2 = st.number_input("Nombre 2", value=0.0)
    if st.button("Calculer"): st.success(f"Résultat: {n1 + n2}")

elif choice == "💱 Bourse":
    st.header("💱 Taux de Change")
    st.info("Les données seront affichées ici.")

elif choice == "📝 Tâches":
    st.header("📝 Liste de tâches")
    st.write("Gérez vos tâches ici.")
