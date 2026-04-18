import streamlit as st
import yfinance as yf
from datetime import date
from hijri_converter import Gregorian

# 1. إعدادات الصفحة - الواجهة الواسعة والمنفتحة
st.set_page_config(page_title="مساعدك الرقمي الذكي", page_icon="🤖", layout="wide")

# تنسيق CSS احترافي وتوسيع الواجهة
    # عرض البطاقة - النسخة الفرنسية فقط (كود مصحح)
    st.markdown(f"""
    <div style="background: rgba(255, 255, 255, 0.05); padding: 40px; border-radius: 20px; text-align: center; border: 2px solid rgba(79, 172, 254, 0.3); margin: 20px 0; box-shadow: 0 10px 30px rgba(0,0,0,0.3);">
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

    <style>
    .block-container { padding-top: 2rem; max-width: 92%; }
    .stApp { background: linear-gradient(to bottom, #0f172a, #1e293b); color: white; }
    .stButton>button { 
        width: 100%; border-radius: 12px; 
        background: linear-gradient(45deg, #00f2fe, #4facfe); 
        color: white; border: none; font-weight: bold; 
        height: 3.5rem; font-size: 18px; 
    }
    /* تصميم بطاقة التاريخ "المفتوحة" */
    .hijri-card { 
        background: rgba(255, 255, 255, 0.05); 
        padding: 40px; 
        border-radius: 20px; 
        text-align: center; 
        border: 2px solid rgba(79, 172, 254, 0.3);
        margin: 20px 0;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; font-size: 3rem;'>🤖 مساعدك الرقمي الذكي</h1>", unsafe_allow_html=True)
st.write("---")

# القائمة الجانبية
with st.sidebar:
    st.header("⚙️ لوحة التحكم")
    choice = st.radio("اختر الأداة المطلوبة:", 
        ["📅 محول التاريخ الهجري", "🔢 الحاسبة المتطورة", "💱 بورصة العملات", "📝 مفكرة المهام", "⚖️ الصحة والقياسات"])

# --- 1. محول التاريخ الهجري (بالفرنسية فقط بناءً على طلبك) ---
if choice == "📅 محول التاريخ الهجري":
    st.markdown("<h2 style='text-align: center;'>📅 تحويل التاريخ الميلادي إلى هجري (Fr)</h2>", unsafe_allow_html=True)
    
    col_sp1, col_in, col_sp2 = st.columns([1, 2, 1])
    with col_in:
        d = st.date_input("Choisir la date Grégorienne :", date.today())
    
    # عملية التحويل
    hijri = Gregorian(d.year, d.month, d.day).to_hijri()
    m_fr = hijri.month_name() # اسم الشهر بالفرنسية/الإنجليزية الدولية

    # عرض البطاقة - النسخة الفرنسية فقط
    st.markdown(f"""
    <div class="hijri-card">
        <h2 style='color: #4facfe; margin-bottom: 20px; font-size: 2.2rem;'>Date Hijri</h2>
        
        <div style='margin: 30px 0;'>
            <p style='font-size: 50px; font-weight: bold; color: #ffffff; margin: 0;'>
                {hijri.day} {m_fr} {hijri.year} AH
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

# --- باقي الأقسام (الحاسبة، العملات، المهام) ---
elif choice == "🔢 الحاسبة المتطورة":
    st.header("🔢 الحاسبة")
    n1 = st.number_input("الرقم الأول", value=0.0); n2 = st.number_input("الرقم الثاني", value=0.0)
    if st.button("➕ احسب"): st.success(f"النتيجة: {n1 + n2}")

elif choice == "💱 بورصة العملات":
    st.header("💱 العملات")
    st.info("جاري جلب بيانات البورصة...")

elif choice == "📝 مفكرة المهام":
    st.header("📝 المهام")
    st.write("سجل مهامك اليومية هنا.")

st.divider()
st.caption("📢 مساعدك الرقمي - منصة الأدوات الذكية")
