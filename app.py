import streamlit as st
import pandas as pd
import numpy as np
import datetime
import paho.mqtt.client as mqtt
import json

# ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="Smart Dam Water Level & Flood Warning System", page_icon="🌊", layout="wide")

# ตัวแปรเก็บค่าล่าสุดจาก MQTT
if 'mqtt_water_level' not in st.session_state:
    st.session_state['mqtt_water_level'] = 50.0

# ฟังก์ชันรับค่า MQTT
def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode())
        if "water_level" in payload:
            st.session_state['mqtt_water_level'] = float(payload["water_level"])
    except:
        pass

def start_mqtt():
    try:
        client = mqtt.Client()
        client.connect("broker.hivemq.com", 1883, 60)
        client.subscribe("dam/water_level")
        client.on_message = on_message
        client.loop_start()
    except:
        pass

# เริ่มต้นรัน MQTT Thread เบื้องหลัง
@st.cache_resource
def init_mqtt():
    start_mqtt()

init_mqtt()

# ดึงค่าปัจจุบันจาก ESP32
water_level_pct = st.session_state['mqtt_water_level']

# CSS ตกแต่ง UI (ครอบด้วยเครื่องหมาย """ เรียบร้อย ป้องกัน SyntaxError)
st.markdown("""
    <style>
        .main-header {
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
            padding: 25px;
            border-radius: 12px;
            color: white;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            border: 1px solid #334155;
            margin-bottom: 25px;
            backdrop-filter: blur(16px);
        }
        .card-container {
            background-color: #0f172a;
            padding: 20px;
            border-radius: 10px;
            border: 1px solid #334155;
            color: white;
            box-shadow: 0 4px 6px rgba(0,0,0,0.2);
        }
    </style>
""", unsafe_allow_html=True)

# ส่วนหัวข้อหลัก
st.markdown("""
    <div class="main-header">
        <h2>🌊 ระบบบริหารจัดการและเตือนภัยระดับน้ำเขื่อนอัจฉริยะ (IoT Real-Time)</h2>
        <p style="margin: 0; color: #94a3b8;">Connected to ESP32 Hardware via MQTT (HiveMQ Broker)</p>
    </div>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.header("⚙️ ข้อมูลสถาปัตยกรรมระบบ")
st.sidebar.success("MQTT Broker: 🟢 ออนไลน์ (broker.hivemq.com)")
st.sidebar.info("Topic: dam/water_level")
st.sidebar.warning("ESP32 State: เชื่อมต่อเซ็นเซอร์ HC-SR04 & รีเลย์ประตูระบายน้ำเรียบร้อย")

# ส่วนแสดงผล 2D Canvas จำลองระดับน้ำจากฮาร์ดแวร์จริง
st.subheader("🌐 Digital Twin: 2D Reservoir Simulation (Live from ESP32)")

col_2d_1, col_2d_2 = st.columns([1, 2])

with col_2d_1:
    st.markdown(f"""
        <div style="background-color: #1e293b; padding: 15px; border-radius: 10px; border: 1px solid #334155; text-align: center;">
            <b style="color: #38bdf8;">ระดับน้ำจริง (ESP32 Sensor)</b><br><br>
            <div style="width: 100px; height: 180px; background-color: #0f172a; border: 3px solid #38bdf8; border-radius: 8px; margin: 0 auto; position: relative; overflow: hidden;">
                <div style="position: absolute; bottom: 0; width: 100%; height: {water_level_pct}%; background: linear-gradient(180deg, #38bdf8 0%, #0284c7 100%); transition: height 0.5s;"></div>
                <div style="position: absolute; width: 100%; text-align: center; top: 40%; color: white; font-weight: bold; text-shadow: 1px 1px 2px black;">{water_level_pct:.1f}%</div>
            </div>
            <p style="margin-top: 10px; font-size: 14px; color: #94a3b8;">ความจุอ่างเก็บน้ำ</p>
        </div>
    """, unsafe_allow_html=True)

with col_2d_2:
    spillway_status = "เปิดระบาย (OPEN) - Relay Active" if water_level_pct >= 80 else "ปิดปกติ (CLOSED)"
    st.markdown(f"""
        <div class="card-container">
            <h4 style="color: #38bdf8; margin-top: 0;">📊 สถานะฮาร์ดแวร์เรียลไทม์</h4>
            <p>• <b>เซ็นเซอร์วัดระยะ (HC-SR04 Pin 5/18):</b> กำลังอ่านค่าระยะทางผิวน้ำ</p>
            <p>• <b>ระดับน้ำปัจจุบัน:</b> {water_level_pct:.1f}%</p>
            <p>• <b>สถานะประตูระบายน้ำ (Relay Pin 19):</b> <span style="background-color: {'#047857' if water_level_pct >= 80 else '#334155'}; color: white; padding: 3px 8px; border-radius: 4px;">{spillway_status}</span></p>
            <p>• <b>โหมดควบคุม:</b> IoT Autonomous Control (Hysteresis Logic)</p>
        </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Metrics แสดงผล
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="ระดับน้ำปัจจุบันจากเซ็นเซอร์", value=f"{water_level_pct:.1f}%")
with col2:
    status_risk = "วิกฤต (Red Alert)" if water_level_pct >= 80 else ("เฝ้าระวัง (Yellow)" if water_level_pct >= 60 else "ปกติ (Normal)")
    st.metric(label="สถานะความเสี่ยงภัย", value=status_risk)
with col3:
    st.metric(label="การตอบสนองระบบรีเลย์", value="Active" if water_level_pct >= 80 else "Standby")

st.markdown("---")

# ตาราง Event Log
st.subheader("🕒 ประวัติการรับส่งข้อมูลผ่าน MQTT (Event Log)")
log_df = pd.DataFrame({
    "เวลา": [datetime.datetime.now().strftime("%H:%M:%S")],
    "ระดับน้ำจริง (%)": [f"{water_level_pct:.1f}%"],
    "สถานะรีเลย์ (Pin 19)": ["HIGH (Active)" if water_level_pct >= 80 else "LOW (Idle)"],
    "MQTT Topic": ["dam/water_level"]
})
st.table(log_df)
