import streamlit as st
import yfinance as yf
from datetime import date

# 1. إعدادات الصفحة والتصميم
st.set_page_config(page_title="الحقيبة الذكية الشاملة", page_icon="🛠️", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stButton>button { width: 100%; border-radius: 8px; background-color: #225566; color: white; height: 3em; font-weight: bold; }
    .stMetric { background-color: #161b22; padding: 15px; border-radius: 10px; border: 1px solid #30363d; }
    </style>
    """, unsafe_allow_html=True)

st.title("🛠️ الحقيبة الذكية الشاملة")
st.write("كل ما تحتاجه من أدوات في مكان واحد")

# القائمة الجانبية للتنقل بين الأدوات
menu = ["🔢 الحاسبة المتطورة", "💱 محول العملات", "⚖️ حاسبة الوزن (BMI)", "📅 حاسبة العمر", "📏 محول القياسات"]
choice = st.sidebar.selectbox("اختر الأداة:", menu)

# --- 1. الحاسبة المتطورة ---
if choice == "🔢 الحاسبة المتطورة":
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
elif choice == "💱 محول العملات":
    st.header("💱 أسعار العملات مباشر")
    curr_dict = {"الدرهم المغربي": "USDMAD=X", "الجنيه المصري": "USDEGP=X", "الريال السعودي": "USDSAR=X", "اليورو": "USDEUR=X"}
    target = st.selectbox("حول من الدولار ($) إلى:", list(curr_dict.keys()))
    
    @st.cache_data(ttl=600)
    def get_rate(sym):
        try: return round(yf.Ticker(sym).history(period="1d")['Close'].iloc[-1], 2)
        except: return 10.0

    rate = get_rate(curr_dict[target])
    amount = st.number_input("المبلغ بالدولار ($)", value=1.0)
    st.metric(label=f"القيمة بـ {target}", value=f"{round(amount*rate, 2)}", delta=f"السعر: {rate}")

# --- 3. حاسبة الوزن المثالي ---
elif choice == "⚖️ حاسبة الوزن (BMI)":
    st.header("⚖️ احسب وزنك المثالي")
    w = st.number_input("الوزن (كجم)", value=70.0)
    h = st.number_input("الطول (سم)", value=170.0) / 100
    if st.button("احسب مؤشر الكتلة"):
        bmi = round(w / (h*h), 1)
        st.info(f"مؤشر كتلة جسمك هو: {bmi}")
        if bmi < 18.5: st.warning("وزن ناقص")
        elif 18.5 <= bmi < 25: st.success("وزن مثالي ✅")
        else: st.error("وزن زائد")

# --- 4. حاسبة العمر ---
elif choice == "📅 حاسبة العمر":
    st.header("📅 احسب عمرك بدقة")
    dob = st.date_input("تاريخ ميلادك", date(2000, 1, 1))
    today = date.today()
    age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
    st.success(f"عمرك الآن هو: {age} سنة")
    st.balloons()

# --- 5. محول القياسات ---
elif choice == "📏 محول القياسات":
    st.header("📏 محول الوحدات")
    sub_choice = st.selectbox("نوع التحويل:", ["المسافة (كم إلى ميل)", "الحرارة (مئوي إلى فهرنهايت)"])
    val = st.number_input("أدخل القيمة:")
    if sub_choice == "المسافة (كم إلى ميل)":
        st.write(f"النتيجة: {round(val * 0.621, 2)} ميل")
    else:
        st.write(f"النتيجة: {round((val * 9/5) + 32, 2)} فهرنهايت")

st.divider()
st.write("📢 **إعلان:** [تواصل معنا لتصميم تطبيقك الخاص](https://wa.me)")
