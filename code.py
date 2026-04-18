import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import date
from hijri_converter import Gregorian

# 1. إعدادات الصفحة - الواجهة الواسعة
st.set_page_config(page_title="مساعدك الرقمي Pro", page_icon="🤖", layout="wide")

# تنسيق CSS احترافي لمحاكاة شكل الجدول المرفق في الصورة
st.markdown("""
    <style>
    .stApp { background-color: #f8fafc; }
    /* تنسيق جدول الرواتب المخصص */
    .salary-table {
        width: 100%;
        border-collapse: collapse;
        margin: 20px 0;
        font-family: Arial, sans-serif;
    }
    .salary-table th {
        background-color: #e8eefc; /* لون أزرق باهت مثل الصورة */
        color: #000;
        border: 1px solid #000;
        padding: 10px;
        text-align: center;
        font-style: italic;
    }
    .salary-table td {
        border: 1px solid #000;
        padding: 10px;
        text-align: center;
        font-weight: bold;
    }
    .total-label {
        text-align: center;
        font-weight: bold;
        font-size: 18px;
    }
    .total-value {
        background-color: #fef08a; /* اللون الأصفر المميز للمجموع */
        border: 2px solid #000;
        padding: 10px;
        text-align: center;
        font-weight: bold;
        font-size: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# العنوان الرئيسي
st.markdown("<h1 style='text-align: center; color: #1e3a8a;'>🤖 Assistant Digital Pro</h1>", unsafe_allow_html=True)
st.write("---")

# القائمة الجانبية (Sidebar)
with st.sidebar:
    st.header("⚙️ Menu des Outils")
    choice = st.radio("Sélectionnez l'outil :", 
        ["📅 Calendrier Hijri", "💰 Gestion de Paie (Tableau)", "🔢 Calculatrice", "💱 Bourse Live"])

# --- 1. محول التاريخ الهجري ---
if choice == "📅 Calendrier Hijri":
    st.header("📅 Convertisseur Hijri")
    d = st.date_input("Date Grégorienne :", date.today())
    hijri = Gregorian(d.year, d.month, d.day).to_hijri()
    st.info(f"Date : {hijri.day} {hijri.month_name()} {hijri.year} AH ({hijri.day_name()})")

# --- 2. إدارة الرواتب (الشكل المطلوب في الصورة) ---
elif choice == "💰 Gestion de Paie (Tableau)":
    st.header("📊 Calcul de Salaire Professionnel")
    
    # مدخلات البيانات
    col1, col2, col3 = st.columns(3)
    with col1: h_price = st.number_input("Prix Heure (سعر الساعة)", value=17.92)
    with col2: hours = st.number_input("Heures (ساعات العمل)", value=8)
    with col3: days = st.number_input("Nombres de jour (عدد الأيام)", value=30)
    
    # الحسابات
    daily = round(hours * h_price, 2)
    product = round(daily * days, 2)
    
    # بناء الجدول بنظام HTML ليطابق الصورة تماماً
    st.markdown(f"""
    <table class="salary-table">
        <tr>
            <th>Heures</th>
            <th>Prix Heures</th>
            <th>Salaire Journalier</th>
            <th>Nombres de jour</th>
            <th>PRODUIT</th>
        </tr>
        <tr>
            <td>{hours}</td>
            <td>{h_price}</td>
            <td>{daily}</td>
            <td>{days}</td>
            <td>{product}</td>
        </tr>
    </table>
    
    <div style="display: flex; justify-content: flex-end; align-items: center; gap: 20px; margin-top: -21px;">
        <div class="total-label" style="width: 20%; border: 1px solid #000; padding: 11px; border-top: none;">TOTAL</div>
        <div class="total-value" style="width: 20%;">{product}</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.write("---")
    st.caption("تنبيه: هذا الجدول مصمم ليطابق الشكل الذي طلبته في الصورة.")

# --- 3. الحاسبة ---
elif choice == "🔢 Calculatrice":
    st.header("🔢 Calculatrice")
    n1 = st.number_input("Nombre 1", value=0.0)
    n2 = st.number_input("Nombre 2", value=0.0)
    if st.button("Calculer"): st.success(f"Résultat : {n1 + n2}")

# --- 4. البورصة ---
elif choice == "💱 Bourse Live":
    st.header("💱 Taux de Change")
    st.info("Données en cours de chargement من البورصة العالمية...")

st.divider()
st.caption("🤖 Assistant Digital Pro - 2024")
