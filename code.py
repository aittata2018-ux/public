import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة
st.set_page_config(page_title="Assistant Digital Pro", page_icon="🤖", layout="wide")

# تنسيق CSS احترافي لضبط الجدول بدقة (Pixel Perfect)
st.markdown("""
    <style>
    .stApp { background-color: #f8fafc; }
    
    /* تنسيق الجدول الرئيسي */
    .custom-table {
        width: 100%;
        border-collapse: collapse;
        margin-top: 20px;
        background-color: white;
    }
    .custom-table th {
        background-color: #e8eefc;
        color: #1e3a8a;
        border: 1px solid #000;
        padding: 12px;
        text-align: center;
        font-weight: bold;
        font-style: italic;
    }
    .custom-table td {
        border: 1px solid #000;
        padding: 12px;
        text-align: center;
        font-weight: bold;
        color: #333;
    }

    /* تنسيق قسم المجموع (TOTAL) أسفل الجدول */
    .total-container {
        display: flex;
        justify-content: flex-end;
        margin-top: -1px; /* للالتصاق بالجدول */
    }
    .total-label {
        width: 200px;
        border: 1px solid #000;
        padding: 10px;
        text-align: center;
        font-weight: bold;
        background-color: white;
    }
    .total-value {
        width: 200px;
        background-color: #fef08a; /* الأصفر المختار */
        border: 1px solid #000;
        border-left: none;
        padding: 10px;
        text-align: center;
        font-weight: bold;
        font-size: 1.2rem;
        color: #000;
    }
    
    /* تحسين شكل خانات الإدخال */
    .stNumberInput { margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color: #1e3a8a;'>🤖 Assistant Digital Pro</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: left;'>📊 Calcul de Salaire Professionnel</h3>", unsafe_allow_html=True)

# --- واجهة إدخال البيانات المنظمة ---
col1, col2, col3 = st.columns(3)
with col1:
    h_price = st.number_input("Prix Heure (سعر الساعة)", value=17.92, step=0.01)
with col2:
    hours = st.number_input("Heures (ساعات العمل)", value=8)
with col3:
    days = st.number_input("Nombres de jour (عدد الأيام)", value=30)

# الحسابات
daily_salary = round(hours * h_price, 2)
total_product = round(daily_salary * days, 2)

# --- عرض الجدول المنسق بدقة ---
st.markdown(f"""
    <table class="custom-table">
        <thead>
            <tr>
                <th>Heures</th>
                <th>Prix Heures</th>
                <th>Salaire Journalier</th>
                <th>Nombres de jour</th>
                <th>PRODUIT</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>{hours}</td>
                <td>{h_price}</td>
                <td>{daily_salary}</td>
                <td>{days}</td>
                <td>{total_product}</td>
            </tr>
        </tbody>
    </table>
    <div class="total-container">
        <div class="total-label">TOTAL</div>
        <div class="total-value">{total_product:,.2f}</div>
    </div>
    """, unsafe_allow_html=True)

st.write("---")
st.caption("💡 تم ضبط التنسيق ليتطابق مع الشكل المطلوب في الصورة الأصلية.")

# القسم الإضافي للإعلانات أو التواصل
st.sidebar.header("⚙️ الإعدادات")
if st.sidebar.button("🗑️ إعادة تعيين"):
    st.rerun()
