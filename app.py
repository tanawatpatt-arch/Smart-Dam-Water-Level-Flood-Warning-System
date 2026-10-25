import streamlit as st
import pandas as pd
import numpy as np
import datetime

# ตั้งค่าหน้าเว็บให้เต็มจอ (Wide Layout) และใช้ธีมเข้ม
st.set_page_config(page_title="Smart Dam Water Level & Flood Warning System", page_icon="🌊", layout="wide")

# CSS ตกแต่งเพิ่มเติมเพื่อให้ UI มีมิติ โค้งมน และสวยงามระดับโปร
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
        <h2>🌊 แบบจำลองระบบบริหารจัดการและเตือนภัยระดับน้ำเขื่อนอัจฉริยะ</h2>
        <p style="margin: 0; color: #94a3b8;">Smart Dam Water Level & Flood Warning System with Digital Twin & 2D Reservoir Simulation</p>
    </div>
""", unsafe_allow_html=True)

# แผงควบคุมด้านข้าง (Sidebar)
st.sidebar.header("⚙️ ข้อมูลสถาปัตยกรรมระบบ")
st.sidebar.success("MQTT Broker: 🟢 ออนไลน์ (broker.hivemq.com)")
st.sidebar.info("Cloud Brain: Stochastic ML Model (R² = 0.9540)")
st.sidebar.warning("ESP32 State: เชื่อมต่อเซ็นเซอร์ HC-SR04 & รีเลย์ประตูระบายน้ำ")
st.sidebar.markdown("---")
if st.sidebar.button("🧹 ล้างประวัติเหตุการณ์ (Clear Log)"):
    st.sidebar.success("ล้างประวัติสำเร็จ")

# ส่วน Digital Twin และภาพจำลองระดับน้ำ 2 มิติ (Visual Water Tank)
st.subheader("🌐 Digital Twin: 2D Reservoir Simulation & Spillway Control")

col_2d_1, col_2d_2 = st.columns([1, 2])

with col_2d_1:
    # จำลองหลอดระดับน้ำ 2 มิติด้วย HTML/CSS สวยๆ
    water_level_pct = 78.5
    st.markdown(f"""
        <div style="background-color: #1e293b; padding: 15px; border-radius: 10px; border: 1px solid #334155; text-align: center;">
            <b style="color: #38bdf8;">ระดับน้ำจำลอง (2D Tank)</b><br><br>
            <div style="width: 100px; height: 180px; background-color: #0f172a; border: 3px solid #38bdf8; border-radius: 8px; margin: 0 auto; position: relative; overflow: hidden;">
                <div style="position: absolute; bottom: 0; width: 100%; height: {water_level_pct}%; background: linear-gradient(180deg, #38bdf8 0%, #0284c7 100%); transition: height 0.5s;"></div>
                <div style="position: absolute; width: 100%; text-align: center; top: 40%; color: white; font-weight: bold; text-shadow: 1px 1px 2px black;">{water_level_pct}%</div>
            </div>
            <p style="margin-top: 10px; font-size: 14px; color: #94a3b8;">ความจุอ่างเก็บน้ำ</p>
        </div>
    """, unsafe_allow_html=True)

with col_2d_2:
    st.markdown("""
        <div class="card-container">
            <h4 style="color: #38bdf8; margin-top: 0;">📊 สถานะการทำงานระบบเรียลไทม์</h4>
            <p>• <b>เซ็นเซอร์วัดระยะ (HC-SR04):</b> 12.5 ซม. จากผิวน้ำ (สถานะปกติ)</p>
            <p>• <b>อัตราการไหลเข้า (Inflow Rate):</b> 145.2 ลบ.ม./วินาที</p>
            <p>• <b>อัตราการระบายออก (Outflow Rate):</b> 120.0 ลบ.ม./วินาที</p>
            <p>• <b>สถานะประตูระบายน้ำ (Spillway):</b> <span style="background-color: #047857; color: white; padding: 3px 8px; border-radius: 4px;">เปิดระบาย (OPEN) - Relay Active</span></p>
            <p>• <b>โหมดควบคุม:</b> ระบบอัตโนมัติอัจฉริยะ (AI Autonomous Control)</p>
        </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# แผงตัวเลขสถิติสำคัญ
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="ระดับน้ำปัจจุบันในอ่างเก็บน้ำ", value="78.5%", delta="+2.3% (น้ำเพิ่มขึ้น)")
with col2:
    st.metric(label="พื้นที่เสี่ยงภัยท้ายเขื่อน", value="ระดับเฝ้าระวัง (Yellow)", delta="ปลอดภัย", delta_color="normal")
with col3:
    st.metric(label="เวลาที่คาดว่าน้ำจะถึงจุดวิกฤต", value="ในอีก 4 ชั่วโมง", delta="AI Warning")

st.markdown("---")

# กราฟวิเคราะห์ขั้นสูง
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
        'ระบบ': ['ระบบเดิม (Manual)', 'ระบบเขื่อนอัจฉริยะ (AI)'],
        'เวลาหน่วงในการระบายน้ำ (นาที)': [45.2, 12.8]
    })
    st.bar_chart(eff_data.set_index('ระบบ'))

st.markdown("---")

# ตารางแผนงานและ Event Log
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
