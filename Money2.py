import streamlit as st
import pandas as pd
import numpy as np

# ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="เครื่องมือวางแผนดอกเบี้ยทบต้น", layout="wide")

# หัวข้อแอป
st.title("💰 เครื่องมือวางแผนดอกเบี้ยทบต้น (Compound Interest Planner)")
st.write("ออกแบบโดย Financial Math Expert เพื่อช่วยให้คุณบรรลุเป้าหมายทางการเงิน")

# --- ส่วน Sidebar สำหรับกรอกข้อมูล ---
st.sidebar.header("📝 ปรับแต่งข้อมูลของคุณ")

p = st.sidebar.number_input("เงินต้นเริ่มต้น (บาท)", min_value=0.0, value=100000.0, step=1000.0)
annual_rate_pct = st.sidebar.slider("อัตราดอกเบี้ยต่อปี (%)", min_value=0.0, max_value=50.0, value=5.0, step=0.1)
t = st.sidebar.number_input("ระยะเวลาออม (ปี)", min_value=1, max_value=50, value=10)

compounding_options = {
    "ทบต้นทุกปี (Yearly)": 1,
    "ทบต้นทุกรายไตรมาส (Quarterly)": 4,
    "ทบต้นทุกเดือน (Monthly)": 12,
    "ทบต้นทุกวัน (Daily)": 365
}
n_choice = st.sidebar.selectbox("ความถี่ในการทบต้น", list(compounding_options.keys()))
n = compounding_options[n_choice]

# แปลงอัตราดอกเบี้ยเป็นทศนิยม
r = annual_rate_pct / 100

# --- การตรวจจับตัวเลขที่ไม่สมจริง (Error Handling/Advice) ---
if annual_rate_pct > 15.0:
    st.warning("⚠️ คุณตั้งอัตราดอกเบี้ยไว้สูงกว่าค่าเฉลี่ยตลาด (ปกติหุ้นอยู่ที่ 7-10%) โปรดระมัดระวังความเสี่ยงที่อาจเกิดขึ้น")
elif annual_rate_pct < 1.0:
    st.info("💡 นี่คืออัตราผลตอบแทนระดับเงินฝากออมทรัพย์ทั่วไป")

# --- ตรรกะการคำนวณ ---
def calculate_growth(principal, rate, n_freq, years):
    data = []
    current_balance = principal
    
    for year in range(1, years + 1):
        # สูตร A = P(1 + r/n)^(nt)
        final_amount = principal * (1 + rate/n_freq)**(n_freq * year)
        interest_this_year = final_amount - current_balance
        
        data.append({
            "ปีที่": year,
            "เงินต้นเริ่มปี": round(current_balance, 2),
            "ดอกเบี้ยที่ได้รับในปีนั้น": round(interest_this_year, 2),
            "เงินรวมปลายปี": round(final_amount, 2)
        })
        current_balance = final_amount
        
    return pd.DataFrame(data)

# คำนวณผลลัพธ์
df_result = calculate_growth(p, r, n, t)
final_total = df_result.iloc[-1]["เงินรวมปลายปี"]
total_interest = final_total - p

# --- แสดงผลหน้าจอหลัก ---
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("เงินรวมสุทธิ (A)", f"{final_total:,.2f} บาท")
with col2:
    st.metric("เงินต้นทั้งหมด (P)", f"{p:,.2f} บาท")
with col3:
    st.metric("ดอกเบี้ยสะสมทั้งหมด", f"{total_interest:,.2f} บาท", delta_color="normal")

# กราฟแสดงการเติบโต
st.subheader("📈 กราฟการเติบโตของเงินทุน")
st.line_chart(df_result.set_index("ปีที่")["เงินรวมปลายปี"])

# ตารางข้อมูล
st.subheader("📊 ตารางรายละเอียดรายปี")
st.dataframe(df_result, use_container_width=True)

# คำแนะนำเพิ่มเติม
st.markdown("---")
st.write("**คำแนะนำจากผู้เชี่ยวชาญ:**")
st.write(f"- หากคุณเพิ่มระยะเวลาจาก {t} ปี เป็น {t+5} ปี เงินรวมของคุณจะเพิ่มขึ้นอย่างมหาศาลจากพลังของดอกเบี้ยทบต้น")
st.write("- วินัยในการออมสำคัญพอๆ กับอัตราดอกเบี้ย")