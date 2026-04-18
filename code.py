import streamlit as st

# عنوان التطبيق
st.title("🧮 الحاسبة الذكية ومحول العملات")

# --- قسم الحاسبة الأساسية ---
st.subheader("🔢 الحاسبة")
num1 = st.number_input("الرقم الأول", value=0.0, key="n1")
num2 = st.number_input("الرقم الثاني", value=0.0, key="n2")

col1, col2, col3, col4 = st.columns(4)
res = None

with col1:
    if st.button("+", key="add"): res = num1 + num2
with col2:
    if st.button("-", key="sub"): res = num1 - num2
with col3:
    if st.button("×", key="mul"): res = num1 * num2
with col4:
    if st.button("÷", key="div"):
        if num2 != 0: res = round(num1 / num2, 2)
        else: st.error("قسمة على 0!")

if res is not None:
    st.success(f"النتيجة: {res}")

st.markdown("---")

# --- قسم محول العملات (مثال: من دولار إلى درهم/جنيه) ---
st.subheader("💱 محول عملات سريع")
usd_amount = st.number_input("أدخل المبلغ بالدولار ($)", value=1.0)

# يمكنك تعديل رقم الصرف بناءً على السعر الحالي في بلدك
exchange_rate = 10.15  # افترضنا هنا سعر الصرف 10.15 (مثلاً للدرهم المغربي)
local_res = round(usd_amount * exchange_rate, 2)

st.info(f"المبلغ المساوي بالعملة المحلية: {local_res}")
st.caption(f"سعر الصرف المستخدم: 1 دولار = {exchange_rate}")

st.markdown("---")
# خانة الإعلان المطورة
st.write("📢 **إعلان:** [أعلن هنا لزيادة مبيعاتك - تواصل معنا](https://wa.me)")


