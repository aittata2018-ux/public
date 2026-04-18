import streamlit as st
import yfinance as yf

# 1. إعدادات الصفحة واللمسات الجمالية (CSS)
st.set_page_config(page_title="المنصة الذكية الشاملة", page_icon="🚀", layout="centered")

# إضافة لمسة جمالية للأزرار والألوان باستخدام CSS
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        height: 3em;
        background-color: #225566;
        color: white;
    }
    .stMetric {
        background-color: #1e1e1e;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #333;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🚀 المنصة الذكية الشاملة")
st.caption("حاسبة متطورة • أسعار عملات لايف • أدوات تجارية")

# --- القسم الأول: الحاسبة المتطورة ---
with st.expander("🔢 الحاسبة السريعة والنسبة المئوية", expanded=True):
    col_n1, col_n2 = st.columns(2)
    n1 = col_n1.number_input("الرقم الأول", value=0.0, key="main_n1")
    n2 = col_n2.number_input("الرقم الثاني", value=0.0, key="main_n2")

    c1, c2, c3, c4, c5 = st.columns(5)
    res = None
    
    if c1.button("➕"): res = n1 + n2
    if c2.button("➖"): res = n1 - n2
    if c3.button("✖️"): res = n1 * n2
    if c4.button("➗"): res = round(n1 / n2, 2) if n2 != 0 else "خطأ"
    if c5.button(" % "): res = round((n1 * n2) / 100, 2) # حاسبة النسبة المئوية

    if res is not None:
        st.success(f"النتيجة النهائية: {res}")

st.divider()

# --- القسم الثاني: محول العملات العالمي المباشر ---
st.subheader("💱 محول العملات العالمي (Live)")

# قائمة العملات المدعومة
currency_dict = {
    "الدرهم المغربي (MAD)": "USDMAD=X",
    "الجنيه المصري (EGP)": "USDEGP=X",
    "الريال السعودي (SAR)": "USDSAR=X",
    "الدرهم الإماراتي (AED)": "USDAED=X",
    "اليورو (EUR)": "USDEUR=X",
    "الجنيه الإسترليني (GBP)": "USDGBP=X"
}

selected_curr = st.selectbox("اختر العملة التي تريد التحويل إليها:", list(currency_dict.keys()))

@st.cache_data(ttl=600) # تحديث كل 10 دقائق لضمان الدقة العالية
def get_rate(symbol):
    try:
        ticker = yf.Ticker(symbol)
        return round(ticker.history(period="1d")['Close'].iloc[-1], 2)
    except:
        return 1.0

live_rate = get_rate(currency_dict[selected_curr])

col_usd, col_res = st.columns(2)
usd_val = col_usd.number_input("المبلغ بالدولار ($)", value=1.0)
converted_val = round(usd_val * live_rate, 2)

with col_res:
    st.metric(label=f"المبلغ بـ {selected_curr.split()[-1]}", value=f"{converted_val}", delta=f"سعر الصرف: {live_rate}")

st.divider()

# --- القسم الثالث: مساحة الإعلانات والتواصل ---
st.subheader("📢 خدماتنا وإعلاناتنا")
col_ad1, col_ad2 = st.columns(2)

with col_ad1:
    st.info("💻 **برمج تطبيقك الخاص**\nنصمم لك تطبيقات احترافية.")
    st.link_button("تواصل معنا واتساب", "https://wa.me")

with col_ad2:
    st.warning("📊 **إعلان تجاري**\nمساحة محجوزة لأفضل العروض اليومية.")

# زر دعم المطور بشكل أنيق
st.markdown("---")
st.write("🙏 إذا أعجبك التطبيق لا تنسى دعمه بمشاركة الرابط!")
