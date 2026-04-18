import streamlit as st
import yfinance as yf
from datetime import date
from hijri_converter import Gregorian

# 1. إعدادات الصفحة والتنسيق الجمالي الاحترافي
st.set_page_config(page_title="مساعدك الرقمي الذكي", page_icon="🤖", layout="centered")

st.markdown("""
    <style>
    .stApp { background: linear-gradient(to bottom, #0f172a, #1e293b); color: white; }
    .stButton>button { width: 100%; border-radius: 12px; background: linear-gradient(45deg, #00f2fe, #4facfe); color: white; border: none; font-weight: bold; transition: 0.3s; }
    .stButton>button:hover { transform: scale(1.02); box-shadow: 0 4px 15px rgba(79, 172, 254, 0.4); }
    .metric-card { background: rgba(255, 255, 255, 0.05); padding: 20px; border-radius: 15px; border: 1px solid rgba(255, 255, 255, 0.1); }
    </style>
    """, unsafe_allow_html=True)

st.title("🤖 مساعدك الرقمي الذكي")
st.write("---")

# القائمة الجانبية المطورة
with st.sidebar:
    st.image("https://flaticon.com", width=100)
    st.header("⚙️ لوحة التحكم")
    choice = st.radio("اختر الأداة:", 
        ["🔢 الحاسبة المتطورة", "💱 بورصة العملات", "📅 محول التاريخ الهجري", "📝 مفكرة المهام", "⚖️ الصحة والقياسات"])

# --- 1. الحاسبة والنسبة ---
if choice == "🔢 الحاسبة المتطورة":
    st.header("🔢 الحاسبة والنسبة المئوية")
    n1 = st.number_input("الرقم الأول", value=0.0)
    n2 = st.number_input("الرقم الثاني", value=0.0)
    c1, c2, c3, c4, c5 = st.columns(5)
    res = None
    if c1.button("➕"): res = n1 + n2
    if c2.button("➖"): res = n1 - n2
    if c3.button("✖️"): res = n1 * n2
    if c4.button("➗"): res = round(n1/n2, 2) if n2 != 0 else "خطأ"
    if c5.button("%"): res = round((n1 * n2) / 100, 2)
    if res is not None: st.success(f"النتيجة: {res}")

# --- 2. محول العملات ---
elif choice == "💱 بورصة العملات":
    st.header("💱 أسعار العملات (مباشر)")
    curr_dict = {"المغرب (MAD)": "USDMAD=X", "مصر (EGP)": "USDEGP=X", "السعودية (SAR)": "USDSAR=X", "أوروبا (EUR)": "USDEUR=X"}
    target = st.selectbox("اختر العملة المستهدفة:", list(curr_dict.keys()))
    
    @st.cache_data(ttl=600)
    def get_rate(sym):
        try: return round(yf.Ticker(sym).history(period="1d")['Close'].iloc[-1], 2)
        except: return 10.0

    rate = get_rate(curr_dict[target])
    usd = st.number_input("المبلغ بالدولار ($)", value=1.0)
    st.metric(label=f"القيمة بـ {target}", value=f"{round(usd*rate, 2)}", delta=f"سعر الصرف: {rate}")

# --- 3. محول التاريخ ---
elif choice == "📅 محول التاريخ الهجري":
    st.header("📅 تحويل التاريخ (ميلادي ↔ هجري)")
    d = st.date_input("اختر التاريخ الميلادي:", date.today())
    hijri = Gregorian(d.year, d.month, d.day).to_hijri()
    st.info(f"التاريخ الهجري المقابل هو: {hijri.day} {hijri.month_name()} {hijri.year} هـ")

# --- 4. مفكرة المهام ---
elif choice == "📝 مفكرة المهام":
    st.header("📝 قائمة المهام اليومية")
    if 'tasks' not in st.session_state: st.session_state.tasks = []
    
    new_task = st.text_input("أضف مهمة جديدة:")
    if st.button("إضافة المهمة"):
        if new_task:
            st.session_state.tasks.append(new_task)
            st.rerun()
            
    for i, task in enumerate(st.session_state.tasks):
        col_t, col_b = st.columns([0.8, 0.2])
        col_t.write(f"✅ {task}")
        if col_b.button("حذف", key=f"del_{i}"):
            st.session_state.tasks.pop(i)
            st.rerun()

# --- 5. الصحة والقياسات ---
elif choice == "⚖️ الصحة والقياسات":
    tab1, tab2 = st.tabs(["⚖️ مؤشر الكتلة (BMI)", "📏 محول الوحدات"])
    with tab1:
        w = st.number_input("الوزن (كجم)", value=70.0)
        h = st.number_input("الطول (سم)", value=170.0) / 100
        if st.button("تحليل"):
            bmi = round(w/(h*h), 1)
            st.metric("مؤشر كتلة جسمك", bmi)
            if bmi < 18.5: st.warning("وزن ناقص")
            elif 18.5 <= bmi < 25: st.success("وزن مثالي")
            else: st.error("وزن زائد")
    with tab2:
        val = st.number_input("أدخل القيمة المراد تحويلها:")
        st.write(f"بالميل: {round(val*0.621, 2)} | بالباوند: {round(val*2.204, 2)}")

st.write("---")
st.caption("📢 **إعلان:** هل تريد ميزة إضافية؟ تواصل معنا عبر واتساب.")
