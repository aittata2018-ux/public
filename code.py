import streamlit as st
import yfinance as yf
from datetime import date
from hijri_converter import Gregorian

# 1. إعدادات الصفحة والتنسيق الجمالي
st.set_page_config(page_title="مساعدك الرقمي الذكي", page_icon="🤖", layout="centered")

st.markdown("""
    <style>
    .stApp { background: linear-gradient(to bottom, #0f172a, #1e293b); color: white; }
    .stButton>button { width: 100%; border-radius: 12px; background: linear-gradient(45deg, #00f2fe, #4facfe); color: white; border: none; font-weight: bold; }
    .hijri-card { background: rgba(255, 255, 255, 0.1); padding: 20px; border-radius: 15px; text-align: center; border: 1px solid #4facfe; }
    </style>
    """, unsafe_allow_html=True)

st.title("🤖 مساعدك الرقمي الذكي")

# القائمة الجانبية
with st.sidebar:
    st.header("⚙️ لوحة التحكم")
    choice = st.radio("اختر الأداة:", 
        ["🔢 الحاسبة المتطورة", "💱 بورصة العملات", "📅 محول التاريخ الهجري", "📝 مفكرة المهام", "⚖️ الصحة والقياسات"])

# --- 3. محول التاريخ الهجري (المعدل حسب طلبك) ---
if choice == "📅 محول التاريخ الهجري":
    st.header("📅 تحويل التاريخ الميلادي إلى هجري")
    st.write("اختر التاريخ الميلادي لمعرفة ما يقابله بالهجري بالتفصيل:")
    
    # مدخل التاريخ الميلادي
    d = st.date_input("اختر التاريخ:", date.today())
    
    # عملية التحويل
    hijri = Gregorian(d.year, d.month, d.day).to_hijri()
    
    # عرض النتيجة بشكل مفصل وجميل
    st.markdown(f"""
    <div class="hijri-card">
        <h2 style='color: #4facfe; margin-bottom: 0;'>التاريخ الهجري</h2>
        <p style='font-size: 24px; font-weight: bold; margin-top: 10px;'>
            {hijri.day} {hijri.month_name()} {hijri.year} هـ
        </p>
        <p style='font-size: 16px; opacity: 0.8;'>
            الموافق لـ: {d.day} {d.strftime('%B')} {d.year} م
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.success(f"تم التحويل بنجاح: اليوم هو {hijri.day_name()} في التقويم الهجري.")

# --- بقية الأقسام (بقيت كما هي لضمان عمل التطبيق بالكامل) ---
elif choice == "🔢 الحاسبة المتطورة":
    st.header("🔢 الحاسبة والنسبة المئوية")
    n1 = st.number_input("الرقم الأول", value=0.0); n2 = st.number_input("الرقم الثاني", value=0.0)
    c1, c2, c3, c4, c5 = st.columns(5)
    res = None
    if c1.button("➕"): res = n1 + n2
    if c2.button("➖"): res = n1 - n2
    if c3.button("✖️"): res = n1 * n2
    if c4.button("➗"): res = round(n1/n2, 2) if n2 != 0 else "خطأ"
    if c5.button("%"): res = round((n1 * n2) / 100, 2)
    if res is not None: st.success(f"النتيجة: {res}")

elif choice == "💱 بورصة العملات":
    st.header("💱 أسعار العملات")
    curr_dict = {"المغرب (MAD)": "USDMAD=X", "مصر (EGP)": "USDEGP=X", "السعودية (SAR)": "USDSAR=X"}
    target = st.selectbox("اختر العملة:", list(curr_dict.keys()))
    @st.cache_data(ttl=600)
    def get_rate(sym):
        try: return round(yf.Ticker(sym).history(period="1d")['Close'].iloc[-1], 2)
        except: return 10.0
    rate = get_rate(curr_dict[target])
    usd = st.number_input("المبلغ بالدولار ($)", value=1.0)
    st.metric(label=f"القيمة بـ {target}", value=f"{round(usd*rate, 2)}", delta=f"سعر الصرف: {rate}")

elif choice == "📝 مفكرة المهام":
    st.header("📝 قائمة المهام")
    if 'tasks' not in st.session_state: st.session_state.tasks = []
    new_task = st.text_input("أضف مهمة:")
    if st.button("إضافة"):
        if new_task: st.session_state.tasks.append(new_task); st.rerun()
    for i, task in enumerate(st.session_state.tasks):
        col_t, col_b = st.columns([0.8, 0.2])
        col_t.write(f"✅ {task}")
        if col_b.button("حذف", key=f"del_{i}"): st.session_state.tasks.pop(i); st.rerun()

elif choice == "⚖️ الصحة والقياسات":
    w = st.number_input("الوزن (كجم)", value=70.0); h = st.number_input("الطول (سم)", value=170.0) / 100
    if st.button("تحليل BMI"):
        bmi = round(w/(h*h), 1); st.metric("مؤشر كتلة جسمك", bmi)
