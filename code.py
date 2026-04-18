# أزرار العمليات في أعمدة
col1, col2, col3, col4 = st.columns(4)

res = None

with col1:
    if st.button("➕", key="btn_add"):
        res = num1 + num2
with col2:
    if st.button("➖", key="btn_sub"):
        res = num1 - num2
with col3:
    if st.button("✖️", key="btn_mul"):
        res = num1 * num2
with col4:
    if st.button("÷", key="btn_div"):  # هنا كان الخطأ، قمنا بتمييزه بالـ key
        if num2 != 0:
            res = round(num1 / num2, 2)
        else:
            st.error("خطأ: قسمة على 0")
