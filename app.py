import streamlit as st
import pandas as pd
import numpy as np
import datetime

# ตั้งค่าหน้าเว็บให้เต็มจอ (Wide Layout)
st.set_page_config(page_title="Smart Dam Flood Warning System", page_icon="🌊", layout="wide")

# ส่วนหัวข้อหลักของโปรเจกต์
st.markdown("""
    <div style="background-color: #1e293b; padding: 20px; border-radius: 10px; color: white; margin-bottom: 20px;">
        <h2>🌊 แบบจำลองระบบบริหารจัดการและเตือนภัยระดับน้ำเขื่อนอัจฉริยะ</h2>
        <p style="margin: 0; color: #94a3b8;">Smart Dam Water Level & Flood Warning System with Automated Spillway Control & AI Forecasting</p>
    </div>
""", unsafe_allow_html=True)

# แผงควบคุมด้านข้าง (Sidebar Architecture Info)
st.sidebar.header("⚙️ ข้อมูลสถาปัตยกรรมระบบ")
st.sidebar.success("MQTT Broker: 🟢 ออนไลน์ (broker.hivemq.com)")
st.sidebar.info("Cloud Brain: Stochastic ML Model (R² = 0.9540)")
st.sidebar.warning("ESP32 State: เชื่อมต่อเซ็นเซอร์ HC-SR04 & รีเลย์ประตูระบายน้ำ")
st.sidebar.markdown("---")
if st.sidebar.button("🧹 ล้างประวัติเหตุการณ์ (Clear Log)"):
    st.sidebar.success("ล้างประวัติสำเร็จ")

# ส่วนแสดงสถานะ Digital Twin จำลองสถานะเขื่อน
st.subheader("🌐 Digital Twin: Dam Water Level & Flood Gate Control")
col_twin1, col_twin2 = st.columns([2, 1])

with col_twin1:
    st.markdown("""
        <div style="background-color: #0f172a; padding: 15px; border-radius: 8px; color: #38bdf8; border: 1px solid #334155;">
            <b>สถานะจำลองอ่างเก็บน้ำ (Reservoir Simulation)</b><br>
            • เซ็นเซอร์วัดระยะ: <b>12.5 ซม. จากผิวน้ำ</b><br>
            • อัตราการไหลเข้า (Inflow): <b>145 ลบ.ม./วินาที</b><br>
            • อัตราการระบายออก (Outflow): <b>120 ลบ.ม./วินาที</b>
        </div>
    """, unsafe_allow_html=True)

with col_twin2:
    st.metric(label="สถานะประตูระบายน้ำหลัก (Spillway)", value="เปิดระบาย (OPEN)", delta="Relay Active", delta_color="inverse")

st.markdown("---")

# แผงแสดงตัวเลขสถิติสำคัญ 3 ช่อง
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="ระดับน้ำปัจจุบันในอ่างเก็บน้ำ", value="78.5%", delta="+2.3% (น้ำเพิ่มขึ้น)")
with col2:
    st.metric(label="พื้นที่เสี่ยงภัยท้ายเขื่อน", value="ระดับเฝ้าระวัง (Yellow)", delta="ปลอดภัย", delta_color="normal")
with col3:
    st.metric(label="เวลาที่คาดว่าน้ำจะถึงจุดวิกฤต", value="ในอีก 4 ชั่วโมง", delta="AI Warning")

st.markdown("---")

# ส่วนกราฟวิเคราะห์เชิงลึก
col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    st.subheader("📈 การสลายตัวของระดับน้ำหลาก (Flood Receding Curve)")
    chart_data = pd.DataFrame(
        np.random.randn(10, 2) * 3 + 75,
        columns=['ระดับน้ำจริง (Sensor)', 'ระดับน้ำคาดการณ์ (AI)']
    )
    st.line_chart(chart_data)

with col_chart2:
    st.subheader("📊 เปรียบเทียบประสิทธิภาพการระบายน้ำ (Efficiency)")
    eff_data = pd.DataFrame({
        'ระบบ': ['ระบบเดิม ( manual )', 'ระบบเขื่อนอัจฉริยะ (AI)'],
        'เวลาหน่วงในการระบายน้ำ (นาที)': [45.2, 12.8]
    })
    st.bar_chart(eff_data.set_index('ระบบ'))

st.markdown("---")

# ตารางแผนการบริหารจัดการน้ำและประวัติเหตุการณ์
col_table1, col_table2 = st.columns(2)

with col_table1:
    st.subheader("📋 ตารางแผนการเปิดปิดประตูระบายน้ำอัตโนมัติ")
    plan_df = pd.DataFrame({
        "รอบเวลา": ["รอบที่ 1 (C1)", "รอบที่ 2 (C2)", "รอบที่ 3 (C3)"],
        "เกณฑ์ระดับน้ำ": ["> 70%", "> 80%", "> 90%"],
        "สถานะประตู": ["เปิด 30%", "เปิด 70%", "เปิด 100% (ฉุกเฉิน)"],
        "เป้าหมายเชิงพื้นที่": ["ควบคุมสมดุล", "เร่งระบาย", "ป้องกันน้ำล้นสปิลเวย์"]
    })
    st.table(plan_df)

with col_table2:
    st.subheader("🕒 ประวัติการเกิดเหตุการณ์ฉุกเฉิน (Event Log)")
    log_df = pd.DataFrame({
        "เวลา": [datetime.datetime.now().strftime("%H:%M:%S")],
        "ระดับน้ำ (%)": ["78.5%"],
        "สถานะรีเลย์": ["HIGH (Active)"],
        "การแจ้งเตือน": ["ส่งสัญญาณเตือนภัยระดับ 2"]
    })
    st.table(log_df)

if st.button("🚨 จำลองกดสั่งเปิดประตูระบายน้ำฉุกเฉินด้วยมือ (Manual Override)"):
    st.warning("ส่งคำสั่งฉุกเฉินผ่าน MQTT ไปยัง ESP32 สำเร็จ! ประตูระบายน้ำถูกเปิดออกแล้ว")
