import streamlit as st
import yfinance as yf
from datetime import date, datetime
import pytz
import random
import string
from hijri_converter import Gregorian

# 1. إعدادات الصفحة وتحسين الأداء البصري
st.set_page_config(page_title="Assistant Digital Pro", page_icon="🤖", layout="wide")

# استخدام CSS خارجي لتحسين سرعة التحميل وفصل التنسيق عن المنطق
st.markdown("""
    <style>
    .stApp { background-color: #f8fafc; }
    .main-card { 
        background: white; padding: 2rem; border-radius: 15px; 
        box-shadow: 0 4px 12px rgba(0,0,0,0.05); border: 1px solid #eef2f6;
    }
    .stMetric { background: #f1f5f9; padding: 15px; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# 2. وظائف ذكية مع التخزين المؤقت (Caching) لتسريع الأداء
@st.cache_data(ttl=300)  # يتم تحديث البيانات كل 5 دقائق فقط بدلاً من كل تحديث للصفحة
def get_stock_data(symbol):
    try:
        ticker = yf.Ticker(symbol)
        data = ticker.history(period="1d")
        if data.empty: return None
        return round(data['Close'].iloc[-1], 2)
    except:
        return None

def generate_password(length):
    chars = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(random.SystemRandom().choice(chars) for _ in range(length))

# 3. الهيكل الرئيسي للتطبيق
def main():
    st.markdown("<h1 style='text-align: center; color: #1e293b;'>🤖 Assistant Digital Intelligent Pro</h1>", unsafe_allow_html=True)
    
    with st.sidebar:
        st.header("⚙️ القائمة الرئيسية")
        # استخدام icons لجعل الواجهة أجمل
        choice = st.selectbox("اختر الأداة:", 
            ["📅 التقويم الهجري", "🔢 الحاسبة الذكية", "💹 البورصة والعملات", "⏰ الساعة العالمية", "🔐 مولد كلمات السر", "📝 إدارة المهام"])
        st.divider()
        if st.button("Clear Cache"): # إضافة خيار لمسح التخزين المؤقت
            st.cache_data.clear()

    # استخدام الحاويات (Containers) لتنظيم العرض
    container = st.container()

    with container:
        if choice == "📅 التقويم الهجري":
            st.subheader("تحويل التاريخ إلى هجري")
            d = st.date_input("اختر التاريخ الميلادي:", date.today())
            h = Gregorian(d.year, d.month, d.day).to_hijri()
            st.info(f"📅 التاريخ الهجري: {h.day} {h.month_name()} {h.year} هـ")

        elif choice == "🔢 الحاسبة الذكية":
            st.subheader("الحاسبة السريعة")
            col1, col2 = st.columns(2)
            n1 = col1.number_input("الرقم الأول", value=0.0)
            n2 = col2.number_input("الرقم الثاني", value=0.0)
            
            # استخدام الأزرار في سطر واحد
            cols = st.columns(5)
            ops = [("+", "➕"), ("-", "➖"), ("*", "✖️"), ("/", "➗"), ("%", "٪")]
            for i, (op_name, op_icon) in enumerate(ops):
                if cols[i].button(op_icon, key=op_name):
                    if op_name == "+": st.success(f"النتيجة: {n1 + n2}")
                    elif op_name == "-": st.success(f"النتيجة: {n1 - n2}")
                    elif op_name == "*": st.success(f"النتيجة: {n1 * n2}")
                    elif op_name == "/": 
                        st.success(f"النتيجة: {n1 / n2}" if n2 != 0 else "خطأ: القسمة على صفر")

        elif choice == "💹 البورصة والعملات":
            st.subheader("أسعار السوق المباشرة")
            symbol = st.text_input("أدخل رمز السهم أو العملة (مثل BTC-USD أو AAPL):", "BTC-USD").upper()
            price = get_stock_data(symbol)
            if price:
                st.metric(f"السعر الحالي لـ {symbol}", f"${price:,}")
            else:
                st.error("تعذر جلب البيانات. تأكد من الرمز.")

        elif choice == "⏰ الساعة العالمية":
            st.subheader("التوقيت العالمي المباشر")
            zones = {'الرباط': 'Africa/Casablanca', 'نيويورك': 'America/New_York', 'لندن': 'Europe/London', 'دبي': 'Asia/Dubai'}
            cols = st.columns(len(zones))
            for i, (city, tz) in enumerate(zones.items()):
                time_now = datetime.now(pytz.timezone(tz)).strftime("%I:%M %p")
                cols[i].metric(city, time_now)

        elif choice == "🔐 مولد كلمات السر":
            st.subheader("إنشاء كلمة سر آمنة")
            length = st.select_slider("طول كلمة السر:", options=range(8, 33), value=16)
            if st.button("توليد كلمة السر"):
                pwd = generate_password(length)
                st.code(pwd, language='text')
                st.warning("تنبيه: لا تشارك كلمة السر مع أحد.")

        elif choice == "📝 إدارة المهام":
            st.subheader("قائمة المهام اليومية")
            if 'tasks' not in st.session_state: st.session_state.tasks = []
            
            col_in, col_btn = st.columns([0.8, 0.2])
            new_task = col_in.text_input("أضف مهمة جديدة...", placeholder="مثلاً: مراجعة التقارير")
            if col_btn.button("إضافة"):
                if new_task:
                    st.session_state.tasks.append(new_task)
                    st.rerun()

            for i, task in enumerate(st.session_state.tasks):
                t_col, b_col = st.columns([0.9, 0.1])
                t_col.write(f"🔹 {task}")
                if b_col.button("❌", key=f"del_{i}"):
                    st.session_state.tasks.pop(i)
                    st.rerun()

if __name__ == "__main__":
    main()
