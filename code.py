import streamlit as st
import yfinance as yf
from datetime import date
from hijri_converter import Gregorian

# 1. إعدادات الصفحة - الواجهة المفتوحة (Wide Layout)
st.set_page_config(page_title="مساعدك الرقمي الذكي", page_icon="🤖", layout="wide")

# تنسيق CSS متطور للواجهة المفتوحة والألوان المتدرجة
st.markdown("""
    <style>
    .block-container { padding-top: 2rem; max-width: 90%; }
    .stApp { background: linear-gradient(to bottom, #0f172a, #1e293b); color: white; }
    
    /* تنسيق الأزرار */
    .stButton>button { 
        width: 100%; border-radius: 12px; 
        background: linear-gradient(45deg, #00f2fe, #4facfe); 
        color: white; border: none; font-weight: bold; 
        height: 3.5rem; font-size: 18px; transition: 0.3s;
    }
    .stButton>button:hover { transform: scale(1.02); box-shadow: 0 4px 15px rgba(79, 172, 254, 0.4); }
    
    /* تصميم بطاقة التاريخ المتسعة */
    .hijri-card { 
        background: rgba(255, 255, 255, 0.05); 
        padding: 40px; border-radius: 20px; 
        text-align: center; border: 2px solid rgba(79, 172, 254, 0.3); 
        margin: 20px 0; box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    }
    </style>
    """, unsafe_allow_html=True)

# العنوان الرئيسي
st.markdown("<h1 style='text-align: center; font-size: 3rem;'>🤖 مساعدك الرقمي الذكي</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; opacity: 0.7;'>منصتك المتكاملة للأدوات اليومية والخدمات الذكية</p>", unsafe_allow_html=True)
st.write("---")

# القائمة الجانبية
with st.sidebar:
    st.image("https://flaticon.com", width=100)
    st.header("⚙️ لوحة التحكم")
    choice = st.radio("اختر الأداة المطلوبة:", 
        ["📅 محول التاريخ الهجري", "🔢 الحاسبة المتطورة", "💱 بورصة العملات", "📝 مفكرة المهام", "⚖️ الصحة والقياسات"])

# --- 1. محول التاريخ الهجري (عربي + فرنسي + واجهة مفتوحة) ---
if choice == "📅 محول التاريخ الهجري":
    st.markdown("<h2 style='text-align: center;'>📅 تحويل التاريخ الميلادي إلى هجري</h2>", unsafe_allow_html=True)
    
    col_space1, col_input, col_space2 = st.columns([1, 2, 1])
    with col_input:
        d = st.date_input("اختر التاريخ الميلادي:", date.today())
    
    # عملية التحويل
    hijri = Gregorian(d.year, d.month, d.day).to_hijri()
    
    # قواميس لأسماء الشهور (عربي وفرنسي)
    months_ar = {
        "Muharram": "محرم", "Safar": "صفر", "Rabi' al-Awwal": "ربيع الأول",
        "Rabi' al-Thani": "ربيع الثاني", "Jumada al-Ula": "جمادى الأولى",
        "Jumada al-Akhira": "جمادى الآخرة", "Rajab": "رجب", "Sha'ban": "شعبان",
        "Ramadan": "رمضان", "Shawwal": "شوال", "Dhu al-Qi'dah": "ذو القعدة",
        "Dhu al-Hijjah": "ذو الحجة"
    }
    months_fr = {
        "Muharram": "Muharram", "Safar": "Safar", "Rabi' al-Awwal": "Rabi' al-Awwal",
        "Rabi' al-Thani": "Rabi' al-Thani", "Jumada al-Ula": "Jumada al-Ula",
        "Jumada al-Akhira": "Jumada al-Akhira", "Rajab": "Rajab", "Sha'ban": "Sha'ban",
        "Ramadan": "Ramadan", "Shawwal": "Shawwal", "Dhu al-Qi'dah": "Dhu al-Qi'dah",
        "Dhu al-Hijjah": "Dhu al-Hijjah"
    }

    m_ar = months_ar.get(hijri.month_name())
    m_fr = months_fr.get(hijri.month_name())

    # عرض البطاقة بالتصميم المفتوح والمزدوج
    st.markdown(f"""
    <div class="hijri-card">
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
            الموافق لـ | Correspond au : <b>{d.day}/{d.month}/{d.year}</b>
        </p>
    </div>
    """, unsafe_allow_html=True)
    st.success(f"اليوم | Jour : {hijri.day_name()}")

# --- 2. الحاسبة المتطورة ---
elif choice == "🔢 الحاسبة المتطورة":
    st.header("🔢 الحاسبة والنسبة المئوية")
    col1, col2 = st.columns(2)
    n1 = col1.number_input("الرقم الأول", value=0.0)
    n2 = col2.number_input("الرقم الثاني", value=0.0)
    
    st.write("### اختر العملية الحسابية:")
    c1, c2, c3, c4, c5 = st.columns(5)
    res = None
    if c1.button("➕"): res = n1 + n2
    if c2.button("➖"): res = n1 - n2
    if c3.button("✖️"): res = n1 * n2
    if c4.button("➗"): res = round(n1/n2, 2) if n2 != 0 else "خطأ"
    if c5.button("%"): res = round((n1 * n2) / 100, 2)
    
    if res is not None:
        st.success(f"النتيجة النهائية هي: {res}")

# --- 3. بورصة العملات ---
elif choice == "💱 بورصة العملات":
    st.header("💱 أسعار العملات المباشرة")
    curr_dict = {"المغرب (MAD)": "USDMAD=X", "مصر (EGP)": "USDEGP=X", "السعودية (SAR)": "USDSAR=X", "أوروبا (EUR)": "USDEUR=X"}
    target = st.selectbox("اختر العملة:", list(curr_dict.keys()))
    
    @st.cache_data(ttl=600)
    def get_rate(sym):
        try: return round(yf.Ticker(sym).history(period="1d")['Close'].iloc[-1], 2)
        except: return 10.0

    rate = get_rate(curr_dict[target])
    usd = st.number_input("المبلغ بالدولار ($)", value=1.0)
    st.metric(label=f"القيمة بـ {target}", value=f"{round(usd*rate, 2)}", delta=f"سعر الصرف اليوم: {rate}")

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
        col_t, col_b = st.columns([0.85, 0.15])
        col_t.write(f"✅ {task}")
        if col_b.button("حذف", key=f"del_{i}"):
            st.session_state.tasks.pop(i)
            st.rerun()

# --- 5. الصحة والقياسات ---
elif choice == "⚖️ الصحة والقياسات":
    st.header("⚖️ حاسبة مؤشر كتلة الجسم (BMI)")
    w = st.number_input("الوزن (كجم)", value=70.0)
    h = st.number_input("الطول (سم)", value=170.0) / 100
    if st.button("تحليل حالة الجسم"):
        bmi = round(w/(h*h), 1)
        st.metric("مؤشر كتلة جسمك", bmi)
        if bmi < 18.5: st.warning("وزن ناقص")
        elif 18.5 <= bmi < 25: st.success("وزن مثالي ✅")
        else: st.error("وزن زائد")

st.divider()
st.write("📢 **مساحة إعلانية:** [تواصل معنا للإعلان هنا](https://wa.me)")
