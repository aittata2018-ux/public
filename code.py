import streamlit as st
import yfinance as yf
from datetime import date
from hijri_converter import Gregorian

# 1. إعدادات الصفحة - جعل الواجهة "مفتوحة" ومتسعة
st.set_page_config(page_title="مساعدك الرقمي الذكي", page_icon="🤖", layout="wide")

# تنسيق CSS متقدم لفتح الواجهة وزيادة المسافات مريحة
st.markdown("""
    <style>
    /* توسيع الحاوية الرئيسية */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 90%;
    }
    .stApp { background: linear-gradient(to bottom, #0f172a, #1e293b); color: white; }
    
    /* تصميم الأزرار */
    .stButton>button { 
        width: 100%; 
        border-radius: 12px; 
        background: linear-gradient(45deg, #00f2fe, #4facfe); 
        color: white; 
        border: none; 
        font-weight: bold; 
        height: 3.5rem;
        font-size: 18px;
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

# العنوان الرئيسي في المنتصف
st.markdown("<h1 style='text-align: center; font-size: 3rem;'>🤖 مساعدك الرقمي الذكي</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; opacity: 0.7;'>منصتك المتكاملة للأدوات اليومية والخدمات الذكية</p>", unsafe_allow_html=True)
st.write("---")

# القائمة الجانبية
with st.sidebar:
    st.image("https://flaticon.com", width=100)
    st.header("⚙️ لوحة التحكم")
    choice = st.radio("اختر الأداة المطلوبة:", 
        ["📅 محول التاريخ الهجري", "🔢 الحاسبة المتطورة", "💱 بورصة العملات", "📝 مفكرة المهام", "⚖️ الصحة والقياسات"])

# --- 3. محول التاريخ الهجري (النسخة المفتوحة والاحترافية) ---
if choice == "📅 محول التاريخ الهجري":
    st.markdown("<h2 style='text-align: center;'>📅 تحويل التاريخ الميلادي إلى هجري</h2>", unsafe_allow_html=True)
    
    # جعل شريط اختيار التاريخ يتوسط الصفحة بمساحة واسعة
    col_space1, col_input, col_space2 = st.columns([1, 2, 1])
    with col_input:
        d = st.date_input("اختر التاريخ الميلادي:", date.today())
    
    # عملية التحويل
    hijri = Gregorian(d.year, d.month, d.day).to_hijri()
    
    # قاموس الترجمة للفرنسية
    months_fr = {
        "Muharram": "Muharram", "Safar": "Safar", "Rabi' al-Awwal": "Rabi' al-Awwal",
        "Rabi' al-Thani": "Rabi' al-Thani", "Jumada al-Ula": "Jumada al-Ula",
        "Jumada al-Akhira": "Jumada al-Akhira", "Rajab": "Rajab", "Sha'ban": "Sha'ban",
        "Ramadan": "Ramadan", "Shawwal": "Shawwal", "Dhu al-Qi'dah": "Dhu al-Qi'dah",
        "Dhu al-Hijjah": "Dhu al-Hijjah"
    }
    month_name_fr = months_fr.get(hijri.month_name(), hijri.month_name())

    # عرض البطاقة بشكل متسع
    st.markdown(f"""
    <div class="hijri-card">
        <h2 style='color: #4facfe; margin-bottom: 20px; font-size: 2rem;'>التاريخ الهجري | Date Hijri</h2>
        
        <div style='display: flex; justify-content: space-around; align-items: center; flex-wrap: wrap;'>
            <div style='margin: 20px;'>
                <p style='font-size: 40px; font-weight: bold; color: #ffffff; margin: 0;'>
                    {hijri.day} {hijri.month_name()} {hijri.year} هـ
                </p>
                <p style='font-size: 20px; color: #4facfe;'>باللغة العربية</p>
            </div>
            
            <div style='width: 2px; height: 100px; background: rgba(255,255,255,0.1);'></div>
            
            <div style='margin: 20px;'>
                <p style='font-size: 40px; font-weight: bold; color: #ffffff; margin: 0;'>
                    {hijri.day} {month_name_fr} {hijri.year} AH
                </p>
                <p style='font-size: 20px; color: #4facfe;'>En Français</p>
            </div>
        </div>
        
        <hr style='border: 0.5px solid rgba(255,255,255,0.1); width: 80%; margin: 30px auto;'>
        
        <p style='font-size: 22px; opacity: 0.9;'>
            الموافق لـ | Correspond au : <b>{d.day} {d.strftime('%B')} {d.year}</b>
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.success(f"اليوم | Jour : {hijri.day_name()}")

# --- باقي الأقسام تعمل بنفس التنسيق المفتوح ---
elif choice == "🔢 الحاسبة المتطورة":
    st.header("🔢 الحاسبة والنسبة المئوية")
    # تم استخدام أعمدة أوسع
    col1, col2 = st.columns(2)
    n1 = col1.number_input("الرقم الأول", value=0.0)
    n2 = col2.number_input("الرقم الثاني", value=0.0)
    st.write("### اختر العملية:")
    c1, c2, c3, c4, c5 = st.columns(5)
    res = None
    if c1.button("➕"): res = n1 + n2
    if c2.button("➖"): res = n1 - n2
    if c3.button("✖️"): res = n1 * n2
    if c4.button("➗"): res = round(n1/n2, 2) if n2 != 0 else "خطأ"
    if c5.button("%"): res = round((n1 * n2) / 100, 2)
    if res is not None: st.success(f"النتيجة: {res}")

# (بقية الأقسام تتبع نفس منطق التوسعة المريح)
