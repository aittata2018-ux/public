import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import date

# 1. إعدادات الصفحة
st.set_page_config(page_title="Assistant Digital Pro", page_icon="🤖", layout="wide")

# تنسيق الألوان الفاتحة (Light Theme)
st.markdown("""
    <style>
    .stApp { background-color: #f8fafc; color: #1e293b; }
    .card { background: white; padding: 25px; border-radius: 15px; border: 1px solid #e2e8f0; margin-bottom: 20px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05); }
    h1, h2 { color: #0f172a; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1>🤖 Assistant Digital - Version Tableaux</h1>", unsafe_allow_html=True)
st.write("---")

# القائمة الجانبية
with st.sidebar:
    st.header("⚙️ Menu")
    choice = st.radio("Sélectionnez un outil :", 
        ["💱 Tableau des Devises", "🕌 Horaires de Prière", "⚖️ Guide Santé (BMI)", "🔢 Calculatrice"])

# --- 1. جدول العملات (Devises) ---
if choice == "💱 Tableau des Devises":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("📊 Comparaison des Devises Arabes (vs 1 USD)")
    
    @st.cache_data(ttl=3600)
    def get_all_rates():
        symbols = {"Maroc (MAD)": "USDMAD=X", "Égypte (EGP)": "USDEGP=X", "Arabie (SAR)": "USDSAR=X", "Émirats (AED)": "USDAED=X"}
        data = []
        for name, sym in symbols.items():
            rate = yf.Ticker(sym).history(period="1d")['Close'].iloc[-1]
            data.append({"Pays/Devise": name, "Taux de Change": round(rate, 2), "Symbole": sym.split('=')[0]})
        return pd.DataFrame(data)

    df_currencies = get_all_rates()
    # عرض الجدول بشكل أنيق
    st.table(df_currencies) 
    st.info("💡 Les taux sont mis à jour automatiquement depuis la bourse.")
    st.markdown("</div>", unsafe_allow_html=True)

# --- 2. جدول مواقيت الصلاة (Prière) ---
elif choice == "🕌 Horaires de Prière":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("🕌 Horaires de Prière (Aujourd'hui)")
    
    # بيانات تجريبية منظمة في جدول (يمكن ربطها بـ API مستقبلاً)
    prayer_data = {
        "Prière": ["Fajr", "Chourouk", "Dhuhr", "Asr", "Maghrib", "Isha"],
        "Heure": ["05:12", "06:45", "13:20", "16:55", "19:40", "21:00"]
    }
    df_prayer = pd.DataFrame(prayer_data)
    st.table(df_prayer)
    st.markdown("</div>", unsafe_allow_html=True)

# --- 3. جدول دليل الصحة (BMI Guide) ---
elif choice == "⚖️ Guide Santé (BMI)":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("⚖️ Guide de l'Indice de Masse Corporelle (IMC)")
    
    bmi_guide = {
        "Classification": ["Poids insuffisant", "Poids normal (Idéal)", "Surpoids", "Obésité"],
        "Indice IMC": ["Moins de 18.5", "18.5 – 24.9", "25.0 – 29.9", "30.0 ou plus"],
        "Conseil": ["Manger plus", "Maintenir", "Faire du sport", "Consulter un médecin"]
    }
    df_bmi = pd.DataFrame(bmi_guide)
    st.table(df_bmi)
    
    st.write("---")
    st.write("### Calculez le vôtre :")
    w = st.number_input("Poids (kg)", value=70.0)
    h = st.number_input("Taille (cm)", value=170.0) / 100
    if st.button("Calculer mon IMC"):
        res = round(w/(h*h), 1)
        st.metric("Votre IMC", res)
    st.markdown("</div>", unsafe_allow_html=True)

# --- 4. الحاسبة (Calculatrice) ---
elif choice == "🔢 Calculatrice":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    n1 = st.number_input("Nombre 1", value=0.0)
    n2 = st.number_input("Nombre 2", value=0.0)
    if st.button("Calculer Somme"): st.success(f"Résultat: {n1 + n2}")
    st.markdown("</div>", unsafe_allow_html=True)

st.divider()
st.caption("📢 Assistant Digital Pro - Version Tableaux Intelligents")
