import streamlit as st

# التأكد من تعريف المكتبة والعناوين
st.title("🧮 حاسبتي الذكية")

# تعريف المدخلات
num1 = st.number_input("أدخل الرقم الأول", value=0.0)
num2 = st.number_input("أدخل الرقم الثاني", value=0.0)

# أزرار العمليات
col1, col2, col3, col4 = st.columns(4)
res = None

with col1:
    if st.button("➕", key="add"):
        res = num1 + num2
with col2:
    if st.button("➖", key="sub"):
        res = num1 - num2
with col3:
    if st.button("✖️", key="mul"):
        res = num1 * num2
with col4:
    if st.button("÷", key="div"):
        if num2 != 0:
            res = round(num1 / num2, 2)
        else:
            st.error("لا يمكن القسمة على صفر")

# عرض النتيجة
if res is not None:
    st.success(f"النتيجة: {res}")
