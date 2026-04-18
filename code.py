import streamlit as st
import yfinance as yf
from datetime import date

# 1. إعدادات الصفحة بالعنوان الجديد
st.set_page_config(page_title="مساعدك الرقمي", page_icon="🤖", layout="centered")

# لمسات جمالية احترافية
st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 8px; background-color: #225566; color: white; height: 3em; font-weight: bold; }
    .stMetric { background-color: #161b22; padding: 15px; border-radius: 10px; border: 1px solid #30363d; }
    h1 { color: #4facfe; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# العنوان الرئيسي الجديد
st.title("🤖 مساعدك الرقمي")
st.write("<p style='text-align: center;'>خبيرك الذكي في الحسابات، العملات، والصحة</p>", unsafe_allow_html=True)

# القائمة الجانبية
st.sidebar.header("🗂️ قائمة الأدوات")
menu = ["🔢 الحاسبة والنسبة", "💱 أسعار العملات", "⚖️ الصحة والوزن", "📅 حساب العمر", "📏 محول الوحدات"]
choice = st.sidebar.radio("اختر المهمة التي تريدها:", menu)

# --- 1. الحاسبة المتطورة ---
if choice == "🔢 الحاسبة والنسبة":
    st.header("🔢 الحاسبة والنسبة المئوية")
    col1, col2 = st.columns(2)
    n1 = col1.number_input("الرقم الأول", value=0.0)
    n2 = col2.number_input("الرقم الثاني", value=0.0)
    
    c1, c2, c3, c4, c5 = st.columns(5)
    res = None
    if c1.button("➕"): res = n1 + n2
    if c2.button("➖"): res = n1 - n2
    if c3.button("✖️"): res = n1 * n2
    if c4.button("➗"): res = round(n1/n2, 2) if n2 != 0 else "خطأ"
    if c5.button("%"): res = round((n1 * n2) / 100, 2)
    
    if res is not None:
        st.success(f"النتيجة النهائية: {res}")

# --- 2. محول العملات ---
elif choice == "💱 أسعار العملات":
    st.header("💱 محول العملات العالمي")
    curr_dict = {
        "الدرهم المغربي (MAD)": "USDMAD=X", 
        "الجنيه المصري (EGP)": "USDEGP=X", 
        "الريال السعودي (SAR)": "USDSAR=X", 
        "اليورو (EUR)": "USDEUR=X",
        "الدرهم الإماراتي (AED)": "USDAED=X"
    }
    target = st.selectbox("حول من الدولار ($) إلى:", list(curr_dict.keys()))
    
    @st.cache_data(ttl=600)
    def get_rate(sym):
        try: return round(yf.Ticker(sym).history(period="1d")['Close'].iloc[-1], 2)
        except: return 10.0

    rate = get_rate(curr_dict[target])
    amount = st.number_input("المبلغ بالدولار ($)", value=1.0)
    st.metric(label=f"القيمة بـ {target}", value=f"{round(amount*rate, 2)}", delta=f"سعر الصرف: {rate}")

# --- 3. حاسبة الوزن المثالي ---
elif choice == "⚖️ الصحة والوزن":
    st.header("⚖️ حاسبة الوزن والكتلة (BMI)")
    w = st.number_input("الوزن (كجم)", value=70.0)
    h = st.number_input("الطول (سم)", value=170.0) / 100
    if st.button("تحليل حالة الجسم"):
        bmi = round(w / (h*h), 1)
        st.info(f"مؤشر كتلة جسمك هو: {bmi}")
        if bmi < 18.5: st.warning("الحالة: وزن ناقص")
        elif 18.5 <= bmi < 25: st.success("الحالة: وزن مثالي ✅")
        elif 25 <= bmi < 30: st.warning("الحالة: زيادة في الوزن")
        else: st.error("الحالة: سمنة مفرطة")

# --- 4. حاسبة العمر ---
elif choice == "📅 حساب العمر":
    st.header("📅 حاسبة العمر بالتفصيل")
    dob = st.date_input("تاريخ ميلادك", date(2000, 1, 1))
    today = date.today()
    age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
    st.success(f"عمرك الآن هو: {age} سنة")
    st.balloons()

# --- 5. محول القياسات ---
elif choice == "📏 محول الوحدات":
    st.header("📏 تحويل القياسات")
    sub_choice = st.selectbox("نوع التحويل:", ["المسافة (كم إلى ميل)", "الحرارة (مئوي إلى فهرنهايت)", "الوزن (كجم إلى باوند)"])
    val = st.number_input("أدخل القيمة:", value=1.0)
    if sub_choice == "المسافة (كم إلى ميل)":
        st.write(f"النتيجة: {round(val * 0.621, 2)} ميل")
    elif sub_choice == "الحرارة (مئوي إلى فهرنهايت)":
        st.write(f"النتيجة: {round((val * 9/5) + 32, 2)} فهرنهايت")
    else:
        st.write(f"النتيجة: {round(val * 2.204, 2)} باوند")

st.divider()
st.write("📢 **مساحة إعلانية:** [تواصل مع مساعدك الرقمي للإعلان هنا](https://wa.me)")
