import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import date
from hijri_converter import Gregorian

# 1. إعدادات الصفحة - الواجهة الواسعة
st.set_page_config(page_title="مساعدك الرقمي الذكي", page_icon="🤖", layout="wide")

# تنسيق CSS احترافي (النسخة الفاتحة)
st.markdown("""
    <style>
    .stApp { background-color: #f8fafc; color: #1e293b; }
    .block-container { padding-top: 2rem; max-width: 90%; }
    .card { background: white; padding: 25px; border-radius: 15px; border: 1px solid #e2e8f0; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05); color: #1e293b; }
    .stButton>button { width: 100%; border-radius: 12px; background: linear-gradient(45deg, #3b82f6, #2563eb); color: white; border: none; font-weight: bold; height: 3.5rem; }
    th { background-color: #dbeafe !important; color: #1e3a8a !important; }
    .total-box { background-color: #fef08a; padding: 10px; border-radius: 5px; font-weight: bold; font-size: 20px; text-align: center; border: 2px solid #eab308; color: black; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color: #0f172a;'>🤖 مساعدك الرقمي الذكي</h1>", unsafe_allow_html=True)
st.write("---")

# القائمة الجانبية (تضم كل الأدوات بما فيها حاسبة الرواتب الجديدة)
with st.sidebar:
    st.header("⚙️ لوحة التحكم")
    choice = st.radio("اختر الأداة المطلوبة:", 
        ["📅 محول التاريخ الهجري", "💰 حاسبة الرواتب (Tableau)", "🔢 الحاسبة المتطورة", "💱 بورصة العملات", "📝 مفكرة المهام"])

# --- 1. محول التاريخ الهجري (يبقى كما هو) ---
if choice == "📅 محول التاريخ الهجري":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    d = st.date_input("Choisir la date Grégorienne :", date.today())
    hijri = Gregorian(d.year, d.month, d.day).to_hijri()
    st.markdown(f"<h2 style='text-align:center; color:#2563eb;'>{hijri.day} {hijri.month_name()} {hijri.year} AH</h2>", unsafe_allow_html=True)
    st.write(f"<p style='text-align:center;'>Jour : {hijri.day_name()}</p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# --- 2. حاسبة الرواتب (الإضافة الجديدة بناءً على الصورة) ---
elif choice == "💰 حاسبة الرواتب (Tableau)":
    st.header("📊 Gestionnaire des Salaires")
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1: h_price = st.number_input("Prix Heure (سعر الساعة)", value=17.92)
    with col2: hours = st.number_input("Heures (ساعات العمل)", value=8)
    with col3: days = st.number_input("Jours (الأيام)", value=30)
    
    daily = round(hours * h_price, 2)
    total = round(daily * days, 2)
    
    # الجدول المماثل للصورة
    df = pd.DataFrame({
        "Heures": [hours], "Prix Heures": [h_price], 
        "Salaire Journalier": [daily], "Nombres de jour": [days], "PRODUIT": [total]
    })
    st.table(df)
    
    # خانة المجموع الأصفر
    st.markdown(f"<div style='display: flex; justify-content: flex-end;'><div style='width:200px;'><p style='text-align:center; margin-bottom:5px;'>TOTAL</p><div class='total-box'>{total}</div></div></div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# --- 3. الحاسبة المتطورة ---
elif choice == "🔢 الحاسبة المتطورة":
    st.header("🔢 الحاسبة والنسبة")
    n1 = st.number_input("الرقم 1", value=0.0)
    n2 = st.number_input("الرقم 2", value=0.0)
    if st.button("➕ احسب المجموع"): st.success(f"النتيجة: {n1 + n2}")

# --- 4. بورصة العملات ---
elif choice == "💱 بورصة العملات":
    st.header("💱 أسعار العملات لايف")
    st.info("بيانات البورصة تظهر هنا...")

# --- 5. مفكرة المهام ---
elif choice == "📝 مفكرة المهام":
    st.header("📝 المهام اليومية")
    if 'tasks' not in st.session_state: st.session_state.tasks = []
    t = st.text_input("أضف مهمة:")
    if st.button("إضافة"):
        if t: st.session_state.tasks.append(t); st.rerun()
    for task in st.session_state.tasks:
        st.write(f"✅ {task}")

st.divider()
st.caption("📢 مساعدك الرقمي Pro - منصة الأدوات المتكاملة")
