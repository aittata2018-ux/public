import streamlit as st
import yfinance as yf

# 1. إعدادات الصفحة (لضمان مظهر احترافي على الهواتف)
st.set_page_config(page_title="حاسبتي الذكية والعملات", page_icon="💰", layout="centered")

# عنوان التطبيق
st.title("💰 الحاسبة الذكية وسعر الصرف المباشر")

# --- قسم الحاسبة ---
st.subheader("🔢 الحاسبة السريعة")

# مدخلات الأرقام
n1 = st.number_input("الرقم الأول", value=0.0, key="num1")
n2 = st.number_input("الرقم الثاني", value=0.0, key="num2")

# إنشاء 4 أعمدة متساوية تماماً للأزرار لضمان التناسق البصري
c1, c2, c3, c4 = st.columns(4)
res = None

# استخدام رموز Emoji موحدة لجميع العمليات لضمان نفس الحجم والشكل
if c1.button("➕", use_container_width=True, key="add"): 
    res = n1 + n2
if c2.button("➖", use_container_width=True, key="sub"): 
    res = n1 - n2
if c3.button("✖️", use_container_width=True, key="mul"): 
    res = n1 * n2
if c4.button("➗", use_container_width=True, key="div"): # علامة القسمة الموحدة
    if n2 != 0:
        res = round(n1 / n2, 2)
    else:
        st.error("خطأ: قسمة على 0")

# عرض النتيجة في إطار أخضر جذاب
if res is not None:
    st.success(f"النتيجة النهائية هي: {res}")

st.divider()

# --- قسم محول العملات التلقائي (يجلب السعر من البورصة) ---
st.subheader("💱 أسعار العملات العالمية")

@st.cache_data(ttl=3600) # تحديث السعر كل ساعة لتوفير البيانات وضمان السرعة
def get_live_rate():
    try:
        # يمكنك تغيير USDMAD=X حسب عملة بلدك (مثلاً USDEGP=X للجنيه المصري)
        ticker = yf.Ticker("USDMAD=X") 
        data = ticker.history(period="1d")
        return round(data['Close'].iloc[-1], 2)
    except:
        return 10.0 # سعر احتياطي في حال انقطاع الإنترنت

current_rate = get_live_rate()

usd_amt = st.number_input("المبلغ بالدولار ($)", value=1.0, key="usd_val")
local_val = round(usd_amt * current_rate, 2)

# عرض سعر الصرف بشكل احترافي
st.metric(label="المبلغ بالعملة المحلية", value=f"{local_val}", delta=f"سعر الصرف اليوم: {current_rate}")
st.caption("ℹ️ يتم تحديث الأسعار تلقائياً من الأسواق العالمية.")

st.divider()

# --- قسم الإعلانات والربح ---
st.info("📢 **مساحة إعلانية:** [أعلن هنا واجعل مشروعك يظهر للآلاف](https://wa.me)")

# زر دعم المطور (يمكنك تغييره برابط حسابك)
st.markdown('[![دعم المطور](https://shields.io)](https://buymeacoffee.com)')
