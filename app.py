import streamlit as st
import pandas as pd
import numpy as np
import time

st.set_page_config(page_title="Smart Dam Dashboard", page_icon="🌊", layout="wide")

st.title("🌊 แบบจำลองระบบบริหารจัดการและเตือนภัยระดับน้ำเขื่อนอัจฉริยะ")
st.markdown("Smart Dam Water Level & Flood Warning System Dashboard")

# แผงควบคุมด้านข้าง (Sidebar)
st.sidebar.header("สถานะระบบ (System Status)")
st.sidebar.success("MQTT Broker: 🟢 ออนไลน์ (broker.hivemq.com)")
st.sidebar.info("Cloud AI Prediction: 🟢 พร้อมทำงาน (Accuracy R² = 0.9540)")

# จำลองค่าระดับน้ำแบบเรียลไทม์
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="ระดับน้ำปัจจุบันในอ่างเก็บน้ำ", value="78.5%", delta="+2.3% (น้ำเพิ่มขึ้น)")

with col2:
    st.metric(label="สถานะประตูระบายน้ำ (Spillway)", value="เปิดระบาย (OPEN)", delta="Relay Active", delta_color="inverse")

with col3:
    st.metric(label="เวลาที่คาดว่าน้ำจะถึงจุดวิกฤต", value="ในอีก 4 ชั่วโมง", delta="AI Warning")

st.markdown("---")

# กราฟแสดงสถิติระดับน้ำย้อนหลัง (Time-series)
st.subheader("📈 กราฟแสดงแนวโน้มระดับน้ำย้อนหลัง (Real-time Sensor Data)")
chart_data = pd.DataFrame(
    np.random.randn(20, 1) * 5 + 75,
    columns=['ระดับน้ำ (%)']
)
st.line_chart(chart_data)

st.markdown("---")
st.subheader("🎛️ ปุ่มควบคุมจำลองระบบ (Manual Override)")
if st.button("🚨 สั่งเปิดประตูระบายน้ำฉุกเฉินทันที"):
    st.warning("ส่งคำสั่งฉุกเฉินไปยัง ESP32 สำเร็จ! ประตูระบายน้ำเปิดแล้ว")
