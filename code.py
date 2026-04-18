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
    .stButton>button { width: 100%; border-radius: 12px; background: linear-gradient(45deg, #00f2fe, #4facfe); color: white; border: none; font-weight: bold; height: 3.5rem; font-size: 18px; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; font-size: 3rem;'>🤖 مساعدك الرقمي الذكي</h1>", unsafe_allow_html=True)
st.write("---")

# القائمة الجانبية
with st.sidebar:
    st.header("⚙️ لوحة التحكم")
    choice = st.radio("اختر الأداة:", ["📅 محول التاريخ الهجري", "🔢 الحاسبة المتطورة", "💱 بورصة العملات", "📝 مفكرة المهام"])

# --- 1. محول التاريخ الهجري (النسخة النهائية المعربة) ---
if choice == "📅 محول التاريخ الهجري":
    st.markdown("<h2 style='text-align: center;'>📅 تحويل التاريخ الميلادي إلى هجري</h2>", unsafe_allow_html=True)
    
    col_input_space, col_input_main, col_input_space2 = st.columns([1, 2, 1])
    with col_input_main:
        d = st.date_input("اختر التاريخ الميلادي:", date.today())
    
    # عملية التحويل
    hijri = Gregorian(d.year, d.month, d.day).to_hijri()
    m_name_raw = hijri.month_name()
    
    # قاموس التعريب
    months_ar = {
        "Muharram": "محرم", "Safar": "صفر", "Rabi' al-Awwal": "ربيع الأول",
        "Rabi' al-Thani": "ربيع الثاني", "Jumada al-Ula": "جمادى الأولى",
        "Jumada al-Akhira": "جمادى الآخرة", "Rajab": "رجب", "Sha'ban": "شعبان",
        "Ramadan": "رمضان", "Shawwal": "شوال", "Dhu al-Qi'dah": "ذو القعدة",
        "Dhu al-Hijjah": "ذو الحجة"
    }
    
    m_ar = months_ar.get(m_name_raw, m_name_raw)
    m_fr = m_name_raw

    # عرض البطاقة بالتصميم المفتوح (HTML المصحح)
    st.markdown(f"""
    <div style="background: rgba(255, 255, 255, 0.05); padding: 40px; border-radius: 20px; text-align: center; border: 2px solid rgba(79, 172, 254, 0.3); margin: 20px 0; box-shadow: 0 10px 30px rgba(0,0,0,0.3);">
        <h2 style='color: #4facfe; margin-bottom: 30px; font-size: 2.2rem;'>التاريخ الهجري | Date Hijri</h2>
        
        <div style='display: flex; justify-content: space-around; align-items: center; flex-wrap: wrap;'>
            <div style='margin: 20px;'>
                <p style='font-size: 42px; font-weight: bold; color: #ffffff; margin: 0;'>
                    {hijri.day} {m_ar} {hijri.year} هـ
                </p>
                <p style='font-size: 20px; color: #4facfe;'>باللغة العربية</p>
            </div>
            
            <div style='width: 2px; height: 100px; background: rgba(255,255,255,0.1);'></div>
            
            <div style='margin: 20px;'>
                <p style='font-size: 42px; font-weight: bold; color: #ffffff; margin: 0;'>
                    {hijri.day} {m_fr} {hijri.year} AH
                </p>
                <p style='font-size: 20px; color: #4facfe;'>En Français</p>
            </div>
        </div>
        
        <hr style='border: 0.5px solid rgba(255,255,255,0.1); width: 80%; margin: 30px auto;'>
        
        <p style='font-size: 22px; opacity: 0.9;'>
            الموافق لـ : <b>{d.day}/{d.month}/{d.year}</b>
        </p>
    </div>
    """, unsafe_allow_html=True)
    st.success(f"اليوم | Jour : {hijri.day_name()}")

# --- الأقسام الأخرى لضمان عدم حدوث أخطاء ---
elif choice == "🔢 الحاسبة المتطورة":
    st.header("🔢 الحاسبة")
    n1 = st.number_input("الرقم الأول", value=0.0)
    n2 = st.number_input("الرقم الثاني", value=0.0)
    if st.button("➕ احسب المجموع"): st.success(f"النتيجة: {n1 + n2}")

elif choice == "💱 بورصة العملات":
    st.header("💱 العملات")
    st.info("سيتم عرض أسعار الصرف هنا.")

elif choice == "📝 مفكرة المهام":
    st.header("📝 المهام")
    st.write("أضف مهامك هنا.")
