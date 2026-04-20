import streamlit as st
import pandas as pd
import numpy as np

# ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="เครื่องมือวางแผนเกษียณรวย", layout="wide")

st.title("🎯 เครื่องมือวางแผนเกษียณและดอกเบี้ยทบต้น")
st.write("คำนวณเงินออมเพื่อเป้าหมายเกษียณของคุณอย่างแม่นยำ")

# --- ส่วน Sidebar: ข้อมูลพื้นฐาน ---
st.sidebar.header("👤 ข้อมูลส่วนตัว")
current_age = st.sidebar.number_input("อายุปัจจุบัน", min_value=1, max_value=100, value=30)
retire_age = st.sidebar.number_input("อายุที่ต้องการเกษียณ", min_value=current_age + 1, max_value=100, value=60)
years_to_invest = retire_age - current_age

st.sidebar.header("💰 ข้อมูลการเงิน")
p = st.sidebar.number_input("เงินก้อนตั้งต้น (บาท)", min_value=0.0, value=100000.0, step=1000.0)
monthly_add = st.sidebar.number_input("เงินที่จะออมเพิ่ม (ต่อเดือน)", min_value=0.0, value=5000.0, step=500.0)
annual_rate_pct = st.sidebar.slider("อัตราผลตอบแทนคาดหวังต่อปี (%)", min_value=0.0, max_value=20.0, value=7.0, step=0.1)
target_fund = st.sidebar.number_input("เป้าหมายเงินเกษียณที่ต้องการ (บาท)", min_value=0.0, value=10000000.0, step=100000.0)

# --- ตรรกะการคำนวณ (Logic) ---
r = annual_rate_pct / 100
n = 12  # ทบต้นทุกเดือนเพื่อให้สอดคล้องกับการฝากรายเดือน

def calculate_retirement_plan(principal, monthly_deposit, rate, years):
    data = []
    current_balance = principal
    total_deposit = principal
    
    # คำนวณรายปี
    for year in range(1, years + 1):
        # ใน 1 ปี มี 12 เดือน
        for month in range(1, 13):
            # สูตรดอกเบี้ยทบต้นรายเดือน: Balance = (Balance + Monthly) * (1 + r/12)
            current_balance = (current_balance + monthly_deposit) * (1 + rate/12)
            total_deposit += monthly_deposit
            
        data.append({
            "ปีที่": year,
            "อายุ": current_age + year,
            "เงินต้นสะสม": round(total_deposit, 2),
            "เงินรวม (บวกดอกเบี้ย)": round(current_balance, 2)
        })
        
    return pd.DataFrame(data)

# ประมวลผล
df_result = calculate_retirement_plan(p, monthly_add, r, years_to_invest)
final_amount = df_result.iloc[-1]["เงินรวม (บวกดอกเบี้ย)"]
total_invested = df_result.iloc[-1]["เงินต้นสะสม"]
total_interest = final_amount - total_invested

# --- แสดงผลหน้าจอหลัก ---

# ส่วนวิเคราะห์เป้าหมาย
st.subheader(f"📊 วิเคราะห์แผนเกษียณในอีก {years_to_invest} ปีข้างหน้า")

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("เงินรวมตอนเกษียณ", f"{final_amount:,.2f} ฿")
with col2:
    st.metric("เงินต้นที่คุณลงไป", f"{total_invested:,.2f} ฿")
with col3:
    st.metric("ดอกเบี้ยที่ทำงานให้คุณ", f"{total_interest:,.2f} ฿")

# ตรวจสอบว่าถึงเป้าหมายหรือไม่
st.markdown("---")
if final_amount >= target_fund:
    st.success(f"🎉 ยินดีด้วย! คุณจะบรรลุเป้าหมายเงินเกษียณ {target_fund:,.2f} บาท (เกินเป้ามา {final_amount - target_fund:,.2f} บาท)")
else:
    gap = target_fund - final_amount
    st.error(f"🚩 คุณยังขาดเงินอีก {gap:,.2f} บาท ถึงจะบรรลุเป้าหมาย {target_fund:,.2f} บาท")
    st.info(f"💡 ลองเพิ่มเงินออมรายเดือน หรือยืดอายุเกษียณออกไปอีกนิดเพื่อใช้พลังดอกเบี้ยทบต้นครับ")

# กราฟการเติบโต
st.subheader("📈 กราฟการเติบโตของกองทุนเกษียณ")
st.line_chart(df_result.set_index("อายุ")["เงินรวม (บวกดอกเบี้ย)"])

# แสดงตารางรายปี
with st.expander("ดูตารางรายละเอียดการเติบโตรายปี"):
    st.dataframe(df_result, use_container_width=True)

# คำแนะนำตามหลักการเงิน
st.sidebar.markdown("---")
st.sidebar.write("**คำแนะนำจาก Expert:**")
if annual_rate_pct > 10:
    st.sidebar.warning("การหวังผลตอบแทน > 10% ต่อปี ควรลงทุนในสินทรัพย์เสี่ยง เช่น หุ้น หรือ กองทุนดัชนี")
if years_to_invest < 10:
    st.sidebar.info("ระยะเวลาเหลือน้อย ควรเน้นการออมเงินต้นให้มากขึ้น")