import streamlit as st

# إعدادات الصفحة
st.set_page_config(page_title="الحاسبة الذكية", page_icon="🧮")

st.title("🧮 حاسبتي الذكية")
st.write("تعمل على الهاتف والحاسوب")

# تصميم المدخلات
num1 = st.number_input("أدخل الرقم الأول", value=0.0)
num2 = st.number_input("أدخل الرقم الثاني", value=0.0)

# أزرار العمليات في أعمدة
col1, col2, col3, col4 = st.columns(4)

res = None

with col1:
    if st.button("➕"):
        res = num1 + num2
with col2:
    if st.button("➖"):
        res = num1 - num2
with col3:
    if st.button("✖️"):
        res = num1 * num2
with col4:
    if st.button("➕"):
        if num2 != 0:
            res = round(num1 / num2, 2)
        else:
            st.error("خطأ: قسمة على 0")

# عرض النتيجة
if res is not None:
    st.success(f"النتيجة النهائية هي: {res}")

# زر للمسح (يعيد تحميل الصفحة)
if st.button("مسح النتيجة"):
    st.rerun()

