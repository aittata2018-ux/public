import streamlit as st
import yfinance as yf
from datetime import date
from hijri_converter import Gregorian

# 1. إعدادات الصفحة
st.set_page_config(page_title="مساعدك الرقمي الذكي", page_icon="🤖", layout="wide")

# تنسيق CSS
st.markdown("""
    <style>
    .block-container { padding-top: 2rem; max-width: 90%; }
    .stApp { background: linear-gradient(to bottom, #0f172a, #1e293b); color: white; }
    .stButton>button { width: 100%; border-radius: 12px; background: linear-gradient(45deg, #00f2fe, #4facfe); color: white; border: none; font-weight: bold; height: 3.5rem; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center;'>🤖 مساعدك الرقمي الذكي</h1>", unsafe_allow_html=True)

# القائمة الجانبية
with st.sidebar:
    st.header("⚙️ لوحة التحكم")
    choice = st.radio("اختر الأداة:", ["📅 محول التاريخ الهجري", "🔢 الحاسبة المتطورة", "💱 بورصة العملات", "📝 مفكرة المهام"])

# --- 1. محول التاريخ الهجري ---
if choice == "📅 محول التاريخ الهجري":
    st.markdown("<h2 style='text-align: center;'>📅 تحويل التاريخ الميلادي إلى هجري</h2>", unsafe_allow_html=True)
    
    col_space1, col_input, col_space2 = st.columns([1,2,1])
    with col_input:
        d = st.date_input("اختر التاريخ الميلادي:", date.today())
    
    hijri = Gregorian(d.year, d.month, d.day).to_hijri()
    
    months_fr = {
        "Muharram": "Muharram", "Safar": "Safar", "Rabi' al-Awwal": "Rabi' al-Awwal",
        "Rabi' al-Thani": "Rabi' al-Thani", "Jumada al-Ula": "Jumada al-Ula",
        "Jumada al-Akhira": "Jumada al-Akhira", "Rajab": "Rajab", "Sha'ban": "Sha'ban",
        "Ramadan": "Ramadan", "Shawwal": "Shawwal", "Dhu al-Qi'dah": "Dhu al-Qi'dah",
        "Dhu al-Hijjah": "Dhu al-Hijjah"
    }
    month_name_fr = months_fr.get(hijri.month_name(), hijri.month_name())

    # عرض البطاقة (تأكد من نسخ هذا الجزء بالكامل)
    st.markdown(f"""
    <div style="background: rgba(255, 255, 255, 0.05); padding: 40px; border-radius: 20px; text-align: center; border: 2px solid rgba(79, 172, 254, 0.3); margin: 20px 0;">
        <h2 style='color: #4facfe; margin-bottom: 20px; font-size: 2rem;'>التاريخ الهجري | Date Hijri</h2>
        <div style='display: flex; justify-content: space-around; align-items: center; flex-wrap: wrap;'>
            <div style='margin: 20px;'>
                <p style='font-size: 35px; font-weight: bold; color: #ffffff; margin: 0;'>{hijri.day} {hijri.month_name()} {hijri.year} هـ</p>
                <p style='font-size: 18px; color: #4facfe;'>باللغة العربية</p>
            </div>
            <div style='width: 2px; height: 80px; background: rgba(255,255,255,0.1);'></div>
            <div style='margin: 20px;'>
                <p style='font-size: 35px; font-weight: bold; color: #ffffff; margin: 0;'>{hijri.day} {month_name_fr} {hijri.year} AH</p>
                <p style='font-size: 18px; color: #4facfe;'>En Français</p>
            </div>
        </div>
        <hr style='border: 0.5px solid rgba(255,255,255,0.1); width: 80%; margin: 30px auto;'>
        <p style='font-size: 20px; opacity: 0.9;'>الموافق لـ | Correspond au : <b>{d.day} {d.strftime('%B')} {d.year}</b></p>
    </div>
    """, unsafe_allow_html=True)

# --- 2. الحاسبة المتطورة ---
elif choice == "🔢 الحاسبة المتطورة":
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
    if res is not None: st.success(f"النتيجة: {res}")

# --- 3. بورصة العملات ---
elif choice == "💱 بورصة العملات":
    st.header("💱 أسعار العملات")
    curr_dict = {"المغرب (MAD)": "USDMAD=X", "مصر (EGP)": "USDEGP=X"}
    target = st.selectbox("اختر العملة:", list(curr_dict.keys()))
    @st.cache_data(ttl=600)
    def get_rate(sym):
        try: return round(yf.Ticker(sym).history(period="1d")['Close'].iloc[-1], 2)
        except: return 10.0
    rate = get_rate(curr_dict[target])
    usd = st.number_input("المبلغ بالدولار ($)", value=1.0)
    st.metric(label=f"القيمة بـ {target}", value=f"{round(usd*rate, 2)}", delta=f"سعر الصرف: {rate}")

# --- 4. مفكرة المهام ---
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
