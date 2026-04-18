import streamlit as st
import yfinance as yf
from datetime import date, datetime
import pytz
import random
import string
import sqlite3
import requests
from hijri_converter import Gregorian

# ==========================================
# 1. إعدادات الصفحة والتنسيق (UI/UX)
# ==========================================
st.set_page_config(page_title="Assistant Digital Pro", page_icon="🤖", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #f8fafc; }
    .main-card { 
        background: white; padding: 2rem; border-radius: 15px; 
        box-shadow: 0 4px 12px rgba(0,0,0,0.05); border: 1px solid #eef2f6;
        margin-bottom: 20px;
    }
    .stButton>button { width: 100%; border-radius: 8px; font-weight: 600; }
    h1 { color: #1e293b; text-align: center; margin-bottom: 2rem; }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 2. وظائف قاعدة البيانات (SQLite) لادارة المهام
# ==========================================
def init_db():
    conn = sqlite3.connect('pro_assistant_db.sqlite')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS tasks 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, task TEXT)''')
    conn.commit()
    conn.close()

def load_tasks():
    conn = sqlite3.connect('pro_assistant_db.sqlite')
    c = conn.cursor()
    c.execute("SELECT * FROM tasks")
    data = c.fetchall()
    conn.close()
    return data

def add_task_db(task_text):
    if task_text:
        conn = sqlite3.connect('pro_assistant_db.sqlite')
        c = conn.cursor()
        c.execute("INSERT INTO tasks (task) VALUES (?)", (task_text,))
        conn.commit()
        conn.close()

def update_task_db(task_id, new_text):
    conn = sqlite3.connect('pro_assistant_db.sqlite')
    c = conn.cursor()
    c.execute("UPDATE tasks SET task = ? WHERE id = ?", (new_text, task_id))
    conn.commit()
    conn.close()

def delete_task_db(task_id):
    conn = sqlite3.connect('pro_assistant_db.sqlite')
    c = conn.cursor()
    c.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()

# ==========================================
# 3. وظائف جلب البيانات الخارجية (APIs)
# ==========================================
@st.cache_data(ttl=300)  # تحديث كل 5 دقائق
def get_stock_price(symbol):
    try:
        ticker = yf.Ticker(symbol)
        data = ticker.history(period="1d")
        return round(data['Close'].iloc[-1], 2) if not data.empty else None
    except: return None

@st.cache_data(ttl=3600) # تحديث الطقس كل ساعة
def get_weather_data(city):
    try:
        response = requests.get(f"https://wttr.in{city}?format=j1")
        data = response.json()
        temp = data['current_condition'][0]['temp_C']
        desc = data['current_condition'][0]['weatherDesc'][0]['value']
        return f"{temp}°C", desc
    except: return None, None

def generate_secure_password(length):
    chars = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(random.SystemRandom().choice(chars) for _ in range(length))

# ==========================================
# 4. الهيكل الرئيسي للتطبيق
# ==========================================
def main():
    init_db() # تفعيل قاعدة البيانات
    
    st.markdown("<h1>🤖 Assistant Digital Intelligent Pro</h1>", unsafe_allow_html=True)

    # القائمة الجانبية
    with st.sidebar:
        st.header("⚙️ القائمة الرئيسية")
        choice = st.selectbox("اختر الأداة:", 
            ["📅 التقويم الهجري", "🔢 الحاسبة الذكية", "💹 البورصة والعملات", 
             "⏰ الساعة العالمية", "🔐 مولد كلمات السر", "📝 إدارة المهام"])
        
        st.divider()
        st.subheader("🌤️ حالة الطقس")
        city_input = st.text_input("المدينة:", "Casablanca")
        temp, desc = get_weather_data(city_input)
        if temp:
            st.metric(label=city_input, value=temp, delta=desc)
        
        st.divider()
        if st.button("🔄 تحديث البيانات"):
            st.cache_data.clear()
            st.rerun()

    # محتوى الصفحات
    container = st.container()

    with container:
        if choice == "📅 التقويم الهجري":
            st.subheader("📅 تحويل التاريخ الهجري")
            d = st.date_input("اختر التاريخ الميلادي:", date.today())
            h = Gregorian(d.year, d.month, d.day).to_hijri()
            st.info(f"**التاريخ الهجري:** {h.day} {h.month_name()} {h.year} هـ")
            st.write(f"اليوم: {h.day_name()}")

        elif choice == "🔢 الحاسبة الذكية":
            st.subheader("🔢 الحاسبة الاحترافية")
            col1, col2 = st.columns(2)
            n1 = col1.number_input("الرقم الأول", value=0.0)
            n2 = col2.number_input("الرقم الثاني", value=0.0)
            
            c1, c2, c3, c4 = st.columns(4)
            if c1.button("➕"): st.success(f"النتيجة: {n1 + n2}")
            if c2.button("➖"): st.success(f"النتيجة: {n1 - n2}")
            if c3.button("✖️"): st.success(f"النتيجة: {n1 * n2}")
            if c4.button("➗"): 
                st.success(f"النتيجة: {n1 / n2}" if n2 != 0 else "خطأ: القسمة على صفر")

        elif choice == "💹 البورصة والعملات":
            st.subheader("💹 تتبع الأسواق العالمية")
            symbol = st.text_input("أدخل رمز السهم (مثال: AAPL, BTC-USD, GC=F):", "BTC-USD").upper()
            price = get_stock_price(symbol)
            if price:
                st.metric(f"السعر المباشر لـ {symbol}", f"${price:,}")
                # رسم بياني بسيط لآخر 7 أيام
                data = yf.Ticker(symbol).history(period="7d")
                st.line_chart(data['Close'])
            else:
                st.error("الرمز غير صحيح أو لا توجد بيانات.")

        elif choice == "⏰ الساعة العالمية":
            st.subheader("⏰ التوقيت العالمي")
            zones = {'الرباط': 'Africa/Casablanca', 'نيويورك': 'America/New_York', 'لندن': 'Europe/London', 'دبي': 'Asia/Dubai', 'طوكيو': 'Asia/Tokyo'}
            cols = st.columns(len(zones))
            for i, (name, tz) in enumerate(zones.items()):
                time_now = datetime.now(pytz.timezone(tz)).strftime("%I:%M %p")
                cols[i].metric(name, time_now)

        elif choice == "🔐 مولد كلمات السر":
            st.subheader("🔐 حماية الخصوصية")
            length = st.select_slider("طول كلمة السر:", options=range(8, 33), value=16)
            if st.button("توليد كلمة سر قوية"):
                pwd = generate_secure_password(length)
                st.code(pwd, language='text')
                st.info("اضغط على المربع أعلاه لنسخ كلمة السر.")

        elif choice == "📝 إدارة المهام":
            st.subheader("📝 قائمة المهام (حفظ تلقائي)")
            
            # مدخل جديد
            with st.form("task_form", clear_on_submit=True):
                new_task = st.text_input("أضف مهمة جديدة...")
                if st.form_submit_button("إضافة المهمة"):
                    add_task_db(new_task)
                    st.rerun()

            # عرض المهام وتعديلها
            tasks = load_tasks()
            for tid, ttext in tasks:
                col_txt, col_save, col_del = st.columns([0.7, 0.15, 0.15])
                
                # حقل تعديل لكل مهمة
                edited_text = col_txt.text_input(f"edit_{tid}", value=ttext, key=f"t_{tid}", label_visibility="collapsed")
                
                if edited_text != ttext:
                    if col_save.button("💾", key=f"s_{tid}"):
                        update_task_db(tid, edited_text)
                        st.rerun()
                
                if col_del.button("🗑️", key=f"d_{tid}"):
                    delete_task_db(tid)
                    st.rerun()

    st.divider()
    st.caption("📢 Assistant Digital Pro v2.0 - تم التطوير لدعم الإنتاجية اليومية")

if __name__ == "__main__":
    main()
