import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import numpy as np
import datetime

# Page Configuration
st.set_page_config(
    page_title="Smart Dam Water Level & Flood Warning Digital Twin",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling for Streamlit Shell
st.markdown("""
<style>
    .stApp {
        background-color: #0b0f19;
        color: #e2e8f0;
    }
    .css-1d3b38 lines, [data-testid="stSidebar"] {
        background-color: #0f172a !important;
        border-right: 1px solid #1e293b;
    }
    .header-card {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #334155;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.5);
        margin-bottom: 20px;
    }
    .metric-card {
        background-color: #1e293b;
        border: 1px solid #334155;
        border-radius: 10px;
        padding: 15px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3);
    }
</style>
""", unsafe_allow_html=True)

# Main Title Header
st.markdown("""
<div class="header-card">
    <div style="display: flex; align-items: center; justify-content: space-between;">
        <div>
            <h2 style="margin:0; color: #f8fafc; font-weight: 700; font-size: 1.6rem;">
                🚦 แบบจำลองระบบควบคุมและปรับสมดุลระดับน้ำเขื่อนอัจฉริยะหลังวิกฤตฝนตกหนัก
            </h2>
            <p style="margin:5px 0 0 0; color: #94a3b8; font-size: 0.95rem;">
                Intelligent Reservoir Rebalancing and Flood Warning Simulation Post-Extreme Inflow Emergency
            </p>
        </div>
        <div style="background: rgba(16, 185, 129, 0.1); border: 1px solid #10b981; padding: 6px 14px; border-radius: 20px; color: #10b981; font-weight: 600; font-size: 0.85rem;">
            🟢 MULTI-STAGE RECOVERY (C3 | แผน [75%, 50%, 25%])
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Sidebar System Architecture
st.sidebar.markdown("### ⚙️ สถาปัตยกรรมระบบ (System Architecture)")
st.sidebar.success("MQTT Broker: 🟢 ออนไลน์\n(broker.hivemq.com)")
st.sidebar.info("Cloud AI (Colab): 🧠 พร้อมทำงาน\nความแม่นยำ R² = 0.9629")
st.sidebar.warning("ESP32 State: กำลังฟื้นฟูระดับน้ำ\nคาดการณ์ 3 รอบ...")
st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 ข้อมูลสถาปัตยกรรม")
st.sidebar.caption("• Node: ESP32 + HC-SR04 + Relay Actuator\n• Cloud Brain: Multi-Stage Control Loop\n• Control Loop: Feedback & Dynamic Termination")

if st.sidebar.button("🧹 ล้างประวัติเหตุการณ์", use_container_width=True):
    st.sidebar.success("ล้างข้อมูลเรียบร้อย")

# Interactive 2D Digital Twin HTML Canvas Component
digital_twin_html = """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * { box-sizing: border-box; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; user-select: none; }
  body { margin: 0; padding: 0; background-color: #0b0f19; color: #e2e8f0; overflow: hidden; }
  
  .container {
    width: 100%;
    background-color: #0f172a;
    border: 1px solid #334155;
    border-radius: 12px;
    padding: 16px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.5);
  }

  /* Control Top Bar */
  .top-controls {
    display: flex;
    gap: 10px;
    margin-bottom: 12px;
    align-items: center;
    flex-wrap: wrap;
  }
  .btn {
    background: #1e293b;
    border: 1px solid #475569;
    color: #f8fafc;
    padding: 6px 14px;
    border-radius: 6px;
    cursor: pointer;
    font-size: 13px;
    font-weight: 600;
    display: flex;
    align-items: center;
    gap: 6px;
    transition: all 0.2s ease;
  }
  .btn:hover { background: #334155; border-color: #06b6d4; }
  .btn.active { background: #0284c7; border-color: #38bdf8; color: white; }
  .btn-danger { background: #991b1b; border-color: #ef4444; }
  .btn-danger:hover { background: #dc2626; }

  /* Canvas Container */
  .canvas-relative {
    position: relative;
    width: 100%;
    height: 380px;
    border-radius: 8px;
    overflow: hidden;
    background: #090d16;
    border: 1px solid #1e293b;
  }
  canvas {
    width: 100%;
    height: 100%;
    display: block;
  }

  /* HUD Overlays */
  .hud-badge {
    position: absolute;
    padding: 8px 12px;
    border-radius: 6px;
    font-size: 11px;
    font-weight: 600;
    backdrop-filter: blur(8px);
    box-shadow: 0 4px 12px rgba(0,0,0,0.4);
    z-index: 10;
  }
  
  .cloud-ai-hud {
    top: 14px; left: 14px;
    background: rgba(15, 23, 42, 0.85);
    border: 1px solid #0284c7;
    color: #38bdf8;
  }

  .lcd-hud {
    top: 14px; right: 14px;
    background: #4d7c0f;
    border: 2px solid #3f6212;
    color: #0f172a;
    font-family: 'Courier New', Courier, monospace;
    padding: 8px 14px;
    border-radius: 4px;
    box-shadow: inset 0 0 10px rgba(0,0,0,0.3);
  }

  .sensor-hud {
    bottom: 80px; left: 180px;
    background: rgba(15, 23, 42, 0.85);
    border: 1px solid #06b6d4;
    color: #67e8f9;
  }

  .comparison-hud {
    bottom: 70px; right: 14px;
    background: rgba(15, 23, 42, 0.9);
    border: 1px solid #334155;
    color: #e2e8f0;
    width: 280px;
  }

  .progress-bar-bg {
    width: 100%;
    height: 8px;
    background: #1e293b;
    border-radius: 4px;
    overflow: hidden;
    margin-top: 4px;
  }
  .progress-bar-fill {
    height: 100%;
    transition: width 0.3s ease;
  }

  /* Bottom Step Timeline */
  .timeline-bar {
    display: grid;
    grid-template-columns: repeat(6, 1fr);
    gap: 8px;
    margin-top: 12px;
  }
  .step-btn {
    background: #1e293b;
    border: 1px solid #334155;
    padding: 8px 10px;
    border-radius: 6px;
    font-size: 11px;
    color: #94a3b8;
    text-align: center;
    cursor: pointer;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    transition: all 0.2s;
  }
  .step-btn:hover { border-color: #38bdf8; color: #f8fafc; }
  .step-btn.active {
    background: rgba(6, 182, 212, 0.15);
    border: 1px solid #06b6d4;
    color: #38bdf8;
    font-weight: 700;
    box-shadow: 0 0 10px rgba(6, 182, 212, 0.2);
  }

  .status-strip {
    margin-top: 12px;
    background: rgba(15, 23, 42, 0.8);
    border: 1px solid #0284c7;
    padding: 10px 16px;
    border-radius: 8px;
    font-size: 12px;
    color: #e2e8f0;
    display: flex;
    align-items: center;
    gap: 10px;
  }
</style>
</head>
<body>

<div class="container">
  <!-- Top Action Controls -->
  <div class="top-controls">
    <button class="btn active" id="btnSync">🔴 ซิงค์ตามบอร์ด ESP32 / Wokwi</button>
    <button class="btn btn-danger" id="btnRain">🌧️ จำลองฝนตกหนัก (Simulate Rain)</button>
    <button class="btn" id="btnGate">🚪 เปิด/ปิด ประตูระบายน้ำ (Spillway)</button>
    <button class="btn" id="btnPause">⏸️ หยุด / เล่นต่อ</button>
  </div>

  <!-- Main Canvas Area -->
  <div class="canvas-relative">
    <canvas id="damCanvas"></canvas>

    <!-- Overlay Badges -->
    <div class="hud-badge cloud-ai-hud">
      ☁️ Cloud AI & MQTT Platform (Colab)<br>
      <span style="font-size:10px; color:#94a3b8;">Model: Dam-RL-Agent (R² = 0.9629)</span><br>
      <span style="color:#06b6d4;">Recovery Plan: C1=75% | C2=50% | C3=25%</span>
    </div>

    <div class="hud-badge lcd-hud">
      📟 Wokwi ESP32 LCD1602 (I2C 0x27)<br>
      <span id="lcdLine1">Dam Level: 8.5m</span><br>
      <span id="lcdLine2">Gate Open: 70%</span>
    </div>

    <div class="hud-badge sensor-hud">
      📡 HC-SR04 Sensor<br>
      Water Dist: <span id="sensorVal">3.8 m</span>
    </div>

    <div class="hud-badge comparison-hud">
      📊 เปรียบเทียบระดับน้ำในอ่าง (Real-Time)<br>
      <div style="font-size:10px; color:#38bdf8; margin-top:4px;">
        ระบบ AI ฟื้นฟู 3 รอบ: <span id="aiVal">3.75 m</span>
      </div>
      <div class="progress-bar-bg">
        <div class="progress-bar-fill" id="aiBar" style="width: 40%; background: #06b6d4;"></div>
      </div>

      <div style="font-size:10px; color:#ef4444; margin-top:6px;">
        ระบบปกติ (ระบายคงที่): <span id="normalVal">7.80 m</span>
      </div>
      <div class="progress-bar-bg">
        <div class="progress-bar-fill" id="normalBar" style="width: 80%; background: #ef4444;"></div>
      </div>
    </div>
  </div>

  <!-- Status Notification Strip -->
  <div class="status-strip" id="statusStrip">
    💡 <b>สถานะปัจจุบัน:</b> <span id="statusText">รอบที่ 3 (สปิลเวย์เปิด 70%): ระดับน้ำลดลงจาก 8.50m → 3.75m (ระบบเดิมเหลือ 7.80m)</span>
  </div>

  <!-- Interactive Timeline Steps -->
  <div class="timeline-bar">
    <div class="step-btn" onclick="setStep(1)">1. ฝนตกหนักน้ำล้นอ่าง</div>
    <div class="step-btn" onclick="setStep(2)">2. AI ประมวลผลระบายน้ำ</div>
    <div class="step-btn" onclick="setStep(3)">3. ฟื้นฟูรอบ C1 (75%)</div>
    <div class="step-btn" onclick="setStep(4)">4. ฟื้นฟูรอบ C2 (50%)</div>
    <div class="step-btn active" onclick="setStep(5)">5. ฟื้นฟูรอบ C3 (25%)</div>
    <div class="step-btn" onclick="setStep(6)">6. สภาวะสมดุลปกติ</div>
  </div>
</div>

<script>
  const canvas = document.getElementById('damCanvas');
  const ctx = canvas.getContext('2d');

  function resize() {
    canvas.width = canvas.parentElement.clientWidth;
    canvas.height = canvas.parentElement.clientHeight;
  }
  window.addEventListener('resize', resize);
  resize();

  // Animation State
  let isRunning = true;
  let isRaining = true;
  let gateOpenPercent = 0.7; // 70% open
  let waterLevelHeight = 0.65; // Percentage of reservoir height
  let waveOffset = 0;
  let currentStep = 5;

  // Rain Particles
  const rainDrops = [];
  for(let i=0; i<80; i++) {
    rainDrops.push({
      x: Math.random() * canvas.width,
      y: Math.random() * canvas.height,
      l: Math.random() * 15 + 10,
      v: Math.random() * 8 + 6
    });
  }

  // Water Discharge Particles
  const waterFlowParticles = [];

  function drawGrid() {
    ctx.strokeStyle = '#1e293b';
    ctx.lineWidth = 1;
    const size = 30;
    for(let x = 0; x < canvas.width; x += size) {
      ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, canvas.height); ctx.stroke();
    }
    for(let y = 0; y < canvas.height; y += size) {
      ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(canvas.width, y); ctx.stroke();
    }
  }

  function drawDamStructure() {
    const w = canvas.width;
    const h = canvas.height;

    // Mountain Background Left
    ctx.fillStyle = '#111827';
    ctx.beginPath();
    ctx.moveTo(0, h);
    ctx.lineTo(0, h * 0.4);
    ctx.lineTo(w * 0.25, h * 0.5);
    ctx.lineTo(w * 0.25, h);
    ctx.fill();

    // Dam Main Body (Concrete structure)
    ctx.fillStyle = '#334155';
    ctx.strokeStyle = '#475569';
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.moveTo(w * 0.45, h * 0.25); // Top reservoir edge
    ctx.lineTo(w * 0.55, h * 0.25); // Top crest width
    ctx.lineTo(w * 0.72, h * 0.95); // Sloped spillway face
    ctx.lineTo(w * 0.45, h * 0.95); // Bottom base
    ctx.closePath();
    ctx.fill();
    ctx.stroke();

    // Spillway Gate Metallic Frame
    ctx.fillStyle = '#64748b';
    ctx.fillRect(w * 0.52, h * 0.25, 14, h * 0.35);

    // Dynamic Gate Door
    const gateY = (h * 0.25) + (1 - gateOpenPercent) * (h * 0.25);
    ctx.fillStyle = '#ef4444';
    ctx.fillRect(w * 0.51, gateY, 16, 20);

    // Sensor HC-SR04 Visual Bracket
    ctx.fillStyle = '#06b6d4';
    ctx.fillRect(w * 0.32, h * 0.18, 45, 14);
    ctx.fillStyle = '#0891b2';
    ctx.beginPath();
    ctx.arc(w * 0.35, h * 0.23, 5, 0, Math.PI * 2);
    ctx.arc(w * 0.41, h * 0.23, 5, 0, Math.PI * 2);
    ctx.fill();

    // Dotted ultrasonic beam down to water
    ctx.setLineDash([4, 4]);
    ctx.strokeStyle = '#22d3ee';
    ctx.lineWidth = 1.5;
    ctx.beginPath();
    const currentWaterY = h - (waterLevelHeight * (h * 0.75));
    ctx.moveTo(w * 0.38, h * 0.23);
    ctx.lineTo(w * 0.38, currentWaterY);
    ctx.stroke();
    ctx.setLineDash([]);
  }

  function drawWater() {
    const w = canvas.width;
    const h = canvas.height;
    const currentWaterY = h - (waterLevelHeight * (h * 0.75));

    // Reservoir Water Mass (Left Side)
    ctx.fillStyle = 'rgba(6, 182, 212, 0.75)';
    ctx.beginPath();
    ctx.moveTo(0, currentWaterY);

    // Animated Waves on Water Surface
    for(let x = 0; x <= w * 0.48; x += 10) {
      const y = currentWaterY + Math.sin((x * 0.03) + waveOffset) * 4;
      ctx.lineTo(x, y);
    }

    ctx.lineTo(w * 0.48, h);
    ctx.lineTo(0, h);
    ctx.closePath();
    ctx.fill();

    // Water Water Outflow over Spillway (If Gate is Open)
    if (gateOpenPercent > 0.05 && currentWaterY <= h * 0.45) {
      ctx.fillStyle = 'rgba(56, 189, 248, 0.85)';
      ctx.beginPath();
      ctx.moveTo(w * 0.53, h * 0.32);
      ctx.quadraticCurveTo(w * 0.62, h * 0.45, w * 0.73, h * 0.92);
      ctx.lineTo(w * 0.85, h * 0.95);
      ctx.lineTo(w * 0.85, h);
      ctx.lineTo(w * 0.45, h);
      ctx.closePath();
      ctx.fill();

      // Spawn Splash Particles
      if (Math.random() < 0.6) {
        waterFlowParticles.push({
          x: w * 0.53 + Math.random() * 10,
          y: h * 0.32,
          vx: Math.random() * 4 + 2,
          vy: Math.random() * 2 + 1,
          size: Math.random() * 4 + 2,
          life: 1.0
        });
      }
    }

    // Render Splash Particles
    for(let i = waterFlowParticles.length - 1; i >= 0; i--) {
      const p = waterFlowParticles[i];
      p.x += p.vx;
      p.y += p.vy;
      p.vy += 0.2; // Gravity effect down slope
      p.life -= 0.03;

      ctx.fillStyle = `rgba(224, 242, 254, ${p.life})`;
      ctx.beginPath();
      ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
      ctx.fill();

      if(p.life <= 0) waterFlowParticles.splice(i, 1);
    }
  }

  function drawRain() {
    if (!isRaining) return;
    ctx.strokeStyle = 'rgba(148, 163, 184, 0.4)';
    ctx.lineWidth = 1.2;
    for(let i = 0; i < rainDrops.length; i++) {
      const d = rainDrops[i];
      ctx.beginPath();
      ctx.moveTo(d.x, d.y);
      ctx.lineTo(d.x - 2, d.y + d.l);
      ctx.stroke();

      d.y += d.v;
      d.x -= 0.5;
      if (d.y > canvas.height) {
        d.y = -20;
        d.x = Math.random() * canvas.width;
      }
    }
  }

  function animate() {
    if (isRunning) {
      waveOffset += 0.05;
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      drawGrid();
      drawWater();
      drawDamStructure();
      drawRain();
    }
    requestAnimationFrame(animate);
  }

  // Interactive Buttons Functionality
  document.getElementById('btnPause').onclick = function() {
    isRunning = !isRunning;
    this.classList.toggle('active');
    this.innerText = isRunning ? '⏸️ หยุด / เล่นต่อ' : '▶️ เล่นต่อ';
  };

  document.getElementById('btnRain').onclick = function() {
    isRaining = !isRaining;
    this.classList.toggle('active');
  };

  document.getElementById('btnGate').onclick = function() {
    gateOpenPercent = gateOpenPercent > 0.1 ? 0 : 0.8;
    updateUI();
  };

  function setStep(step) {
    currentStep = step;
    document.querySelectorAll('.step-btn').forEach((b, idx) => {
      b.classList.toggle('active', (idx + 1) === step);
    });

    switch(step) {
      case 1:
        waterLevelHeight = 0.92;
        gateOpenPercent = 0.1;
        isRaining = true;
        updateText("ฝนตกหนักวิกฤต! ระดับน้ำสูงเกิน 90% (8.95m) เซ็นเซอร์เตือนภัยสีแดง", "8.95 m", "10%", "8.95 m", "8.95 m", 95, 95);
        break;
      case 2:
        waterLevelHeight = 0.88;
        gateOpenPercent = 0.4;
        isRaining = true;
        updateText("Cloud AI สั่งการเปิดประตูสปิลเวย์แบบขั้นบันได C1 เพื่อเตรียมเร่งระบาย", "8.50 m", "40%", "7.20 m", "8.80 m", 75, 90);
        break;
      case 3:
        waterLevelHeight = 0.75;
        gateOpenPercent = 0.8;
        isRaining = false;
        updateText("ฟื้นฟูรอบ C1: สปิลเวย์เปิด 80% ระบายน้ำมวลใหญ่ลงสู่ลำน้ำท้ายเขื่อน", "6.40 m", "80%", "5.40 m", "8.20 m", 58, 85);
        break;
      case 4:
        waterLevelHeight = 0.60;
        gateOpenPercent = 0.6;
        isRaining = false;
        updateText("ฟื้นฟูรอบ C2: ลดระดับน้ำต่อเนื่อง ปรับสมดุลการไหลเพื่อไม่ให้พื้นที่ท้ายเขื่อนท่วม", "5.10 m", "60%", "4.30 m", "7.95 m", 45, 82);
        break;
      case 5:
        waterLevelHeight = 0.48;
        gateOpenPercent = 0.7;
        isRaining = false;
        updateText("รอบที่ 3 (สปิลเวย์เปิด 70%): ระดับน้ำลดลงจาก 8.50m → 3.75m (ระบบเดิมเหลือ 7.80m)", "3.75 m", "70%", "3.75 m", "7.80 m", 40, 80);
        break;
      case 6:
        waterLevelHeight = 0.35;
        gateOpenPercent = 0.2;
        isRaining = false;
        updateText("ระดับน้ำกลับเข้าสู่ภาวะสมดุลปลอดภัย (Normal Level 3.20m) ประตูสปิลเวย์ปิดพักการทำงาน", "3.20 m", "20%", "3.20 m", "7.50 m", 30, 75);
        break;
    }
  }

  function updateText(status, level, gate, aiVal, normVal, aiBarW, normBarW) {
    document.getElementById('statusText').innerText = status;
    document.getElementById('lcdLine1').innerText = "Dam Level: " + level;
    document.getElementById('lcdLine2').innerText = "Gate Open: " + gate;
    document.getElementById('sensorVal').innerText = level;
    document.getElementById('aiVal').innerText = aiVal;
    document.getElementById('normalVal').innerText = normVal;
    document.getElementById('aiBar').style.width = aiBarW + "%";
    document.getElementById('normalBar').style.width = normBarW + "%";
  }

  function updateUI() {
    const gateTxt = Math.round(gateOpenPercent * 100) + "%";
    document.getElementById('lcdLine2').innerText = "Gate Open: " + gateTxt;
  }

  // Start Animation
  animate();
</script>
</body>
</html>
"""

# Render Component
components.html(digital_twin_html, height=560)

st.markdown("---")

# Analytical Charts Section
col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    st.subheader("📈 การสลายตัวของระดับน้ำหลาก (Queue Dissipation Curve)")
    chart_data = pd.DataFrame({
        "ไฟปกติ (ไม่มี AI)": [14.0, 13.2, 12.8, 12.0],
        "แผน AI (75%, 50%, 25%)": [14.0, 9.1, 5.7, 3.75]
    }, index=["หลังฝนหยุด", "จบรอบ 1 (C1)", "จบรอบ 2 (C2)", "จบรอบ 3 (C3)"])
    st.line_chart(chart_data)

with col_chart2:
    st.subheader("📊 ความล่าช้าสะสม & ประสิทธิภาพการลดน้ำท่วม")
    eff_col1, eff_col2 = st.columns([2, 1])
    with eff_col1:
        delay_df = pd.DataFrame({
            "ระยะเวลาวิกฤต (นาที)": [74.39, 53.76]
        }, index=["ระบบเดิม", "ระบบ AI"])
        st.bar_chart(delay_df)
    with eff_col2:
        st.metric("🎯 ประสิทธิภาพการลดน้ำท่วม", "27.7%", delta="เร็วกว่าระบบปกติ")

st.markdown("---")

# Analytical Logs & Action Tables
col_table1, col_table2 = st.columns(2)

with col_table1:
    st.subheader("📋 ตารางแผนการฟื้นฟู 3 รอบสัญญาณประตูน้ำ (AI Multi-Cycle Plan)")
    plan_df = pd.DataFrame({
        "รอบสัญญาณประตู": ["รอบที่ 1 (C1)", "รอบที่ 2 (C2)", "รอบที่ 3 (C3)"],
        "เปิดระบายสปิลเวย์": ["75%", "50%", "25%"],
        "คาดการณ์ระดับน้ำ (AI)": ["8.95 m", "5.70 m", "3.75 m"],
        "ระดับน้ำจริง (Sensor)": ["รอผล...", "รอผล...", "รอผล..."],
        "เป้าหมายเชิงพื้นที่": ["ตัดยอดวิกฤต", "ปรับเกลี่ยสมดุล", "เก็บตกและฟื้นฟู"]
    })
    st.table(plan_df)

with col_table2:
    st.subheader("🕒 ประวัติการเกิดเหตุการณ์ฉุกเฉิน (Event Log)")
    log_df = pd.DataFrame({
        "เวลา": ["23:40:34", "00:15:10", "01:05:22"],
        "ระดับน้ำล้น (m)": ["8.95 m", "6.40 m", "3.75 m"],
        "แผน AI (C1,C2,C3)": ["75%, 50%, 25%", "50%, 25%, 10%", "เสร็จสิ้น"],
        "สถานะรีเลย์": ["ACTIVE", "ACTIVE", "NORMAL"]
    })
    st.table(log_df)
