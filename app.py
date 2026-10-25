<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>INTELLIGENT HYDROPOWER DIGITAL TWIN</title>
    <!-- Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- FontAwesome Icons -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <!-- Google Fonts (Inter & Orbitron) -->
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Orbitron:wght@400;600;800;900&display=swap" rel="stylesheet">
    <!-- Three.js Library & OrbitControls -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>
    <!-- Chart.js -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <!-- Paho MQTT Client -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/paho-mqtt/1.0.1/mqttws31.min.js"></script>

    <script>
        tailwind.config = {
            theme: {
                extend: {
                    colors: {
                        cyber: {
                            bg: '#050b14',
                            panel: 'rgba(10, 20, 38, 0.75)',
                            border: '#1e3a5f',
                            accent: '#00f0ff',
                            neonGreen: '#00ff88',
                            neonAmber: '#ffaa00',
                            neonRed: '#ff2a6d'
                        }
                    },
                    fontFamily: {
                        orbitron: ['Orbitron', 'sans-serif'],
                        inter: ['Inter', 'sans-serif']
                    }
                }
            }
        }
    </script>

    <style>
        body {
            background-color: #030712;
            color: #e2e8f0;
            font-family: 'Inter', sans-serif;
            overflow: hidden;
            user-select: none;
        }

        /* Glassmorphism Panel Styling */
        .glass-panel {
            background: rgba(8, 15, 30, 0.75);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border: 1px solid rgba(0, 240, 255, 0.15);
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.5), inset 0 0 15px rgba(0, 240, 255, 0.05);
        }

        .glass-panel-amber {
            background: rgba(30, 20, 8, 0.75);
            backdrop-filter: blur(16px);
            border: 1px solid rgba(255, 170, 0, 0.3);
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.5), inset 0 0 15px rgba(255, 170, 0, 0.05);
        }

        /* Glowing Effects */
        .glow-text-cyan {
            text-shadow: 0 0 10px rgba(0, 240, 255, 0.7), 0 0 20px rgba(0, 240, 255, 0.4);
        }
        .glow-text-red {
            text-shadow: 0 0 10px rgba(255, 42, 109, 0.8), 0 0 20px rgba(255, 42, 109, 0.5);
        }
        .glow-border {
            box-shadow: 0 0 15px rgba(0, 240, 255, 0.3);
        }

        /* Custom Scrollbar */
        ::-webkit-scrollbar {
            width: 4px;
        }
        ::-webkit-scrollbar-track {
            background: rgba(5, 11, 20, 0.5);
        }
        ::-webkit-scrollbar-thumb {
            background: #1e3a5f;
            border-radius: 2px;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: #00f0ff;
        }

        /* Scanline Overlay for Industrial Monitor Look */
        .scanline {
            background: linear-gradient(
                to bottom,
                rgba(255,255,255,0),
                rgba(255,255,255,0) 50%,
                rgba(0, 0, 0, 0.3) 50%,
                rgba(0, 0, 0, 0.3)
            );
            background-size: 100% 4px;
        }

        /* Pulse Animation */
        @keyframes pulse-fast {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.3; }
        }
        .animate-pulse-fast {
            animation: pulse-fast 1s infinite;
        }
    </style>
</head>
<body class="h-screen w-screen relative font-inter overflow-hidden">

    <!-- 3D Canvas Viewport -->
    <div id="canvas-container" class="absolute inset-0 z-0"></div>

    <!-- UI Overlay (HUD Layout) -->
    <div class="relative z-10 h-full w-full flex flex-col justify-between pointer-events-none p-4">

        <!-- ================= TOP HEADER BAR ================= -->
        <header class="w-full glass-panel rounded-xl p-3 flex flex-wrap items-center justify-between pointer-events-auto border-b-2 border-cyber-accent">
            <!-- Title & System ID -->
            <div class="flex items-center space-x-4">
                <div class="p-2 bg-cyan-950/60 rounded-lg border border-cyber-accent/50 text-cyber-accent">
                    <i class="fa-solid fa-water-waves text-2xl animate-pulse"></i>
                </div>
                <div>
                    <h1 class="font-orbitron font-extrabold text-xl tracking-wider text-white flex items-center gap-2">
                        INTELLIGENT HYDROPOWER <span class="text-cyber-accent glow-text-cyan">DIGITAL TWIN</span>
                    </h1>
                    <p class="text-xs text-slate-400 font-mono tracking-widest flex items-center gap-2">
                        <span>SYS ID: HT-9082-DAM</span> | <span>LOCATION: ADVANCED RESERVOIR SECTOR 4</span>
                    </p>
                </div>
            </div>

            <!-- Emergency Warning Banner (Dynamic) -->
            <div id="alarm-banner" class="hidden md:flex items-center gap-3 px-4 py-1.5 rounded-lg bg-red-950/80 border border-cyber-neonRed animate-pulse-fast">
                <i class="fa-solid fa-triangle-exclamation text-cyber-neonRed text-lg"></i>
                <span class="font-orbitron text-xs text-red-200 tracking-wider font-bold">ALARM: CRITICAL RESERVOIR LEVEL REACHED (80%+)</span>
            </div>

            <!-- Status & Clock -->
            <div class="flex items-center space-x-6 text-right font-mono text-xs">
                <!-- MQTT Status -->
                <div class="flex flex-col items-end">
                    <div class="flex items-center gap-2">
                        <span id="mqtt-status-dot" class="h-2.5 w-2.5 rounded-full bg-amber-400 animate-ping"></span>
                        <span id="mqtt-status-text" class="text-amber-400 font-semibold">CONNECTING BROKER</span>
                    </div>
                    <span class="text-[10px] text-slate-500">broker.hivemq.com : 1883</span>
                </div>

                <!-- Clock -->
                <div class="border-l border-slate-800 pl-4 flex flex-col">
                    <span id="live-clock" class="text-base font-orbitron font-bold text-cyber-accent">00:00:00 UTC</span>
                    <span id="live-date" class="text-[10px] text-slate-400">2026-10-26</span>
                </div>
            </div>
        </header>

        <!-- ================= MAIN CONTENT HUD AREA ================= -->
        <div class="flex-1 grid grid-cols-12 gap-4 my-3 pointer-events-none min-h-0">

            <!-- LEFT SIDEBAR: ESP32 Telemetry & Sensor HUD -->
            <aside class="col-span-12 md:col-span-3 lg:col-span-3 flex flex-col gap-3 pointer-events-auto overflow-y-auto pr-1">
                
                <!-- Telemetry Glass Box -->
                <div class="glass-panel rounded-xl p-4 flex flex-col gap-3">
                    <div class="flex justify-between items-center border-b border-slate-800 pb-2">
                        <h2 class="font-orbitron text-xs font-semibold text-cyber-accent tracking-widest flex items-center gap-2">
                            <i class="fa-solid fa-microchip"></i> ESP32 HARDWARE HUDS
                        </h2>
                        <span class="text-[10px] px-2 py-0.5 rounded bg-cyan-950 text-cyan-400 border border-cyan-800">ONLINE</span>
                    </div>

                    <!-- Water Level Gauge Card -->
                    <div class="bg-slate-950/60 rounded-lg p-3 border border-slate-800 flex items-center justify-between">
                        <div>
                            <span class="text-[11px] text-slate-400 uppercase tracking-wider block">Reservoir Level</span>
                            <span id="val-water-pct" class="font-orbitron text-2xl font-bold text-cyber-accent">50.0%</span>
                            <span id="val-water-dist" class="text-[10px] text-slate-500 block">Sensor Dist: 25.0 cm</span>
                        </div>
                        <div class="w-16 h-16 relative flex items-center justify-center">
                            <!-- SVG Circular Progress Bar -->
                            <svg class="w-full h-full transform -rotate-90" viewBox="0 0 36 36">
                                <path class="text-slate-800" stroke-width="3.5" stroke="currentColor" fill="none" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"/>
                                <path id="water-gauge-circle" class="text-cyber-accent transition-all duration-500" stroke-linecap="round" stroke-dasharray="50, 100" stroke-width="3.5" stroke="currentColor" fill="none" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"/>
                            </svg>
                            <i class="fa-solid fa-water text-xs text-cyber-accent absolute"></i>
                        </div>
                    </div>

                    <!-- Flow Rate Cards -->
                    <div class="grid grid-cols-2 gap-2">
                        <div class="bg-slate-950/60 rounded-lg p-2.5 border border-slate-800">
                            <span class="text-[10px] text-slate-400 block">INFLOW RATE</span>
                            <span id="val-inflow" class="font-orbitron text-lg font-bold text-emerald-400">420 m³/s</span>
                            <div class="w-full bg-slate-800 h-1 rounded mt-1 overflow-hidden">
                                <div id="bar-inflow" class="bg-emerald-400 h-full transition-all duration-300" style="width: 60%"></div>
                            </div>
                        </div>

                        <div class="bg-slate-950/60 rounded-lg p-2.5 border border-slate-800">
                            <span class="text-[10px] text-slate-400 block">DISCHARGE OUTFLOW</span>
                            <span id="val-outflow" class="font-orbitron text-lg font-bold text-cyan-400">180 m³/s</span>
                            <div class="w-full bg-slate-800 h-1 rounded mt-1 overflow-hidden">
                                <div id="bar-outflow" class="bg-cyan-400 h-full transition-all duration-300" style="width: 30%"></div>
                            </div>
                        </div>
                    </div>

                    <!-- Turbine Hydro Metrics -->
                    <div class="bg-slate-950/60 rounded-lg p-3 border border-slate-800 space-y-2">
                        <div class="flex justify-between items-center text-xs">
                            <span class="text-slate-400"><i class="fa-solid fa-bolt text-amber-400 mr-1"></i> Turbine Output Power:</span>
                            <span id="val-power" class="font-orbitron font-bold text-amber-400">142.5 MW</span>
                        </div>
                        <div class="flex justify-between items-center text-xs">
                            <span class="text-slate-400"><i class="fa-solid fa-fan text-blue-400 mr-1"></i> Turbine Generator RPM:</span>
                            <span id="val-rpm" class="font-orbitron font-bold text-white">300 RPM</span>
                        </div>
                        <div class="flex justify-between items-center text-xs">
                            <span class="text-slate-400"><i class="fa-solid fa-toggle-on text-emerald-400 mr-1"></i> Spillway Relay (Pin 19):</span>
                            <span id="val-relay" class="font-mono text-xs px-2 py-0.5 rounded bg-slate-800 text-slate-300 border border-slate-700">OFF (Closed)</span>
                        </div>
                    </div>
                </div>

                <!-- Camera Quick View Preset Buttons -->
                <div class="glass-panel rounded-xl p-3 flex flex-col gap-2">
                    <span class="font-orbitron text-[11px] font-semibold text-slate-300 tracking-wider">CAMERA VIEW PRESETS</span>
                    <div class="grid grid-cols-2 gap-2 text-xs font-semibold">
                        <button onclick="setCameraView('overview')" class="px-2 py-1.5 rounded bg-slate-900 hover:bg-cyber-accent hover:text-black text-slate-300 border border-slate-700 transition flex items-center justify-center gap-1.5">
                            <i class="fa-solid fa-globe"></i> Global
                        </button>
                        <button onclick="setCameraView('spillway')" class="px-2 py-1.5 rounded bg-slate-900 hover:bg-cyber-accent hover:text-black text-slate-300 border border-slate-700 transition flex items-center justify-center gap-1.5">
                            <i class="fa-solid fa-archway"></i> Spillway
                        </button>
                        <button onclick="setCameraView('turbines')" class="px-2 py-1.5 rounded bg-slate-900 hover:bg-cyber-accent hover:text-black text-slate-300 border border-slate-700 transition flex items-center justify-center gap-1.5">
                            <i class="fa-solid fa-industry"></i> Power Station
                        </button>
                        <button onclick="setCameraView('sensor')" class="px-2 py-1.5 rounded bg-slate-900 hover:bg-cyber-accent hover:text-black text-slate-300 border border-slate-700 transition flex items-center justify-center gap-1.5">
                            <i class="fa-solid fa-tower-broadcast"></i> ESP Sensor
                        </button>
                    </div>
                </div>

            </aside>

            <!-- CENTER SPACER (Leaves viewport clear for 3D model interaction) -->
            <div class="hidden md:block md:col-span-6 pointer-events-none"></div>

            <!-- RIGHT SIDEBAR: Charts & Alert Log -->
            <aside class="col-span-12 md:col-span-3 lg:col-span-3 flex flex-col gap-3 pointer-events-auto overflow-y-auto pl-1">
                
                <!-- Analytics Chart Glass Box -->
                <div class="glass-panel rounded-xl p-3 flex flex-col gap-2">
                    <div class="flex justify-between items-center border-b border-slate-800 pb-1.5">
                        <h2 class="font-orbitron text-xs font-semibold text-cyber-accent tracking-widest flex items-center gap-2">
                            <i class="fa-solid fa-chart-line"></i> REAL-TIME METRICS
                        </h2>
                        <span class="text-[10px] text-slate-500">Live Trend</span>
                    </div>
                    <!-- Chart Canvas -->
                    <div class="w-full h-36 relative">
                        <canvas id="telemetryChart"></canvas>
                    </div>
                </div>

                <!-- Event Log & System Alerts -->
                <div class="glass-panel rounded-xl p-3 flex flex-col gap-2 flex-1">
                    <div class="flex justify-between items-center border-b border-slate-800 pb-1.5">
                        <h2 class="font-orbitron text-xs font-semibold text-cyber-accent tracking-widest flex items-center gap-2">
                            <i class="fa-solid fa-list-check"></i> EVENT & ALERT LOGS
                        </h2>
                        <button onclick="clearLogs()" class="text-[10px] text-slate-500 hover:text-cyber-accent">Clear</button>
                    </div>

                    <!-- Scrollable Log Container -->
                    <div id="log-container" class="space-y-1.5 font-mono text-[11px] overflow-y-auto max-h-48 pr-1">
                        <!-- Log Entries appended dynamically -->
                        <div class="p-1.5 rounded bg-slate-950/80 border-l-2 border-cyan-400 text-slate-300">
                            <span class="text-slate-500">[10:00:02]</span> MQTT Subscribed to <span class="text-cyan-400">dam/water_level</span>
                        </div>
                        <div class="p-1.5 rounded bg-slate-950/80 border-l-2 border-emerald-400 text-slate-300">
                            <span class="text-slate-500">[10:00:00]</span> Digital Twin System Initialized OK.
                        </div>
                    </div>
                </div>
            </aside>
        </div>

        <!-- ================= BOTTOM CONTROL PANEL ================= -->
        <footer class="w-full glass-panel rounded-xl p-3 pointer-events-auto flex flex-wrap items-center justify-between gap-4 border-t-2 border-cyber-accent">
            
            <!-- Operating Mode Selector -->
            <div class="flex items-center gap-2">
                <span class="font-orbitron text-xs font-semibold text-slate-300 hidden sm:inline"><i class="fa-solid fa-sliders text-cyber-accent"></i> CONTROL MODE:</span>
                <div class="flex bg-slate-950/80 p-1 rounded-lg border border-slate-800 text-xs">
                    <button id="btn-mode-auto" onclick="setMode('auto')" class="px-3 py-1 rounded-md font-semibold transition bg-cyber-accent text-black">
                        AUTO AI
                    </button>
                    <button id="btn-mode-manual" onclick="setMode('manual')" class="px-3 py-1 rounded-md font-semibold transition text-slate-400 hover:text-white">
                        MANUAL
                    </button>
                    <button id="btn-mode-emergency" onclick="setMode('emergency')" class="px-3 py-1 rounded-md font-semibold transition text-slate-400 hover:text-red-400">
                        EMERGENCY FLUSH
                    </button>
                </div>
            </div>

            <!-- Gate Slider Controls -->
            <div class="flex items-center gap-4 flex-1 max-w-md mx-4">
                <span class="font-orbitron text-xs font-semibold text-slate-300 whitespace-nowrap">SPILLWAY GATE:</span>
                <input id="gate-slider" type="range" min="0" max="100" value="0" class="w-full accent-cyan-400 cursor-pointer" oninput="updateGateSlider(this.value)">
                <span id="gate-angle-val" class="font-orbitron text-xs font-bold text-cyber-accent w-12 text-right">0%</span>
            </div>

            <!-- Weather Simulation Controls -->
            <div class="flex items-center gap-2">
                <span class="font-orbitron text-xs font-semibold text-slate-300 hidden lg:inline"><i class="fa-solid fa-cloud-showers-heavy text-blue-400"></i> WEATHER:</span>
                <button id="btn-rain-toggle" onclick="toggleRain()" class="px-3 py-1 rounded-lg bg-slate-900 border border-slate-700 hover:border-cyan-400 text-xs text-slate-300 font-semibold transition flex items-center gap-1.5">
                    <i class="fa-solid fa-cloud-rain"></i> Rain Simulation: <span id="rain-status-text" class="text-slate-500">OFF</span>
                </button>
            </div>
        </footer>

    </div>

    <!-- ================= THREE.JS 3D SCENE SCRIPT ================= -->
    <script>
        // --- 1. Global Variables & Scene Setup ---
        let scene, camera, renderer, controls;
        let reservoirWaterMesh, spillwayWaterFlow, rainParticles;
        let damGateMesh, turbineMeshes = [];
        let waterUniforms;

        // System State Variables
        let systemState = {
            waterLevel: 50.0,       // 0 to 100%
            gateOpenPct: 0.0,       // 0 to 100%
            inflowRate: 420,        // m3/s
            outflowRate: 180,       // m3/s
            powerOutput: 142.5,     // MW
            turbineRpm: 300,        // RPM
            relayActive: false,
            mode: 'auto',           // 'auto', 'manual', 'emergency'
            isRaining: false,
            sensorDistanceCm: 25.0
        };

        const clock = new THREE.Clock();

        // Initialize 3D Engine
        function init3D() {
            const container = document.getElementById('canvas-container');
            
            // Scene
            scene = new THREE.Scene();
            scene.background = new THREE.Color(0x050b14);
            scene.fog = new THREE.FogExp2(0x050b14, 0.008);

            // Camera
            camera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 0.1, 1000);
            camera.position.set(60, 45, 75);

            // Renderer
            renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
            renderer.setPixelRatio(window.devicePixelRatio);
            renderer.setSize(window.innerWidth, window.innerHeight);
            renderer.shadowMap.enabled = true;
            renderer.shadowMap.type = THREE.PCFSoftShadowMap;
            container.appendChild(renderer.domElement);

            // Controls
            controls = new THREE.OrbitControls(camera, renderer.domElement);
            controls.enableDamping = true;
            controls.dampingFactor = 0.05;
            controls.maxPolarAngle = Math.PI / 2 - 0.02; // Don't go below ground
            controls.minDistance = 15;
            controls.maxDistance = 180;
            controls.target.set(0, 5, 0);

            // Lighting Setup
            setupLighting();

            // Build 3D Dam Environment
            buildEnvironment();

            // Window Resize Listener
            window.addEventListener('resize', onWindowResize);
        }

        // --- 2. Lighting System ---
        function setupLighting() {
            // Ambient Light
            const ambient = new THREE.AmbientLight(0x1e293b, 1.2);
            scene.add(ambient);

            // Main Directional Light (Sunlight/Moonlight)
            const sun = new THREE.DirectionalLight(0x38bdf8, 1.5);
            sun.position.set(50, 80, 40);
            sun.castShadow = true;
            sun.shadow.mapSize.width = 2048;
            sun.shadow.mapSize.height = 2048;
            sun.shadow.camera.near = 0.5;
            sun.shadow.camera.far = 200;
            const d = 60;
            sun.shadow.camera.left = -d;
            sun.shadow.camera.right = d;
            sun.shadow.camera.top = d;
            sun.shadow.camera.bottom = -d;
            scene.add(sun);

            // Sci-Fi Point Lights (Cyan & Amber Accents)
            const damPointLight = new THREE.PointLight(0x00f0ff, 2, 40);
            damPointLight.position.set(0, 18, -2);
            scene.add(damPointLight);

            const powerStationLight = new THREE.PointLight(0xffaa00, 2, 35);
            powerStationLight.position.set(15, 8, 20);
            scene.add(powerStationLight);
        }

        // --- 3. Build 3D World Geometry ---
        function buildEnvironment() {
            // A. Mountains Terrain Base
            const terrainGeo = new THREE.PlaneGeometry(160, 160, 64, 64);
            terrainGeo.rotateX(-Math.PI / 2);

            const pos = terrainGeo.attributes.position;
            for (let i = 0; i < pos.count; i++) {
                const x = pos.getX(i);
                const z = pos.getZ(i);
                // Generate valley and mountain contours
                if (z < -10) {
                    pos.setY(i, Math.sin(x * 0.05) * 8 + Math.cos(z * 0.05) * 12 + 10);
                } else if (z > 10) {
                    pos.setY(i, Math.sin(x * 0.08) * 4 + (z - 10) * 0.2);
                } else {
                    pos.setY(i, Math.sin(x * 0.1) * 2);
                }
            }
            terrainGeo.computeVertexNormals();

            const terrainMat = new THREE.MeshStandardMaterial({
                color: 0x0f172a,
                roughness: 0.9,
                metalness: 0.2,
                flatShading: true
            });
            const terrain = new THREE.Mesh(terrainGeo, terrainMat);
            terrain.receiveShadow = true;
            scene.add(terrain);

            // B. Concrete Dam Structure
            const damGroup = new THREE.Group();

            // Main Dam Wall
            const damWallGeo = new THREE.BoxGeometry(70, 24, 12);
            const concreteMat = new THREE.MeshStandardMaterial({
                color: 0x334155,
                roughness: 0.4,
                metalness: 0.5
            });
            const damWall = new THREE.Mesh(damWallGeo, concreteMat);
            damWall.position.set(0, 12, 0);
            damWall.castShadow = true;
            damWall.receiveShadow = true;
            damGroup.add(damWall);

            // Spillway Cutout Gates (Visual Gate Doors)
            const gateGeo = new THREE.BoxGeometry(16, 12, 2);
            const gateMat = new THREE.MeshStandardMaterial({ color: 0xffaa00, metalness: 0.8, roughness: 0.2 });
            damGateMesh = new THREE.Mesh(gateGeo, gateMat);
            damGateMesh.position.set(0, 14, -5.5);
            damGroup.add(damGateMesh);

            scene.add(damGroup);

            // C. Water Reservoir (Upper Dam)
            const reservoirGeo = new THREE.PlaneGeometry(68, 60, 32, 32);
            reservoirGeo.rotateX(-Math.PI / 2);
            
            waterUniforms = {
                time: { value: 1.0 }
            };

            const waterMat = new THREE.MeshStandardMaterial({
                color: 0x0284c7,
                roughness: 0.1,
                metalness: 0.8,
                transparent: true,
                opacity: 0.85
            });

            reservoirWaterMesh = new THREE.Mesh(reservoirGeo, waterMat);
            reservoirWaterMesh.position.set(0, 12, -32); // Y calculated dynamically
            scene.add(reservoirWaterMesh);

            // D. Spillway Water Discharge Stream (Particle/Mesh Stream)
            const streamGeo = new THREE.PlaneGeometry(16, 25, 16, 16);
            streamGeo.rotateX(-Math.PI / 3);
            const streamMat = new THREE.MeshBasicMaterial({
                color: 0x38bdf8,
                transparent: true,
                opacity: 0.0,
                side: THREE.DoubleSide
            });
            spillwayWaterFlow = new THREE.Mesh(streamGeo, streamMat);
            spillwayWaterFlow.position.set(0, 8, 8);
            scene.add(spillwayWaterFlow);

            // E. Hydropower Station Building & Substation
            const powerStationGeo = new THREE.BoxGeometry(18, 10, 12);
            const powerStationMat = new THREE.MeshStandardMaterial({ color: 0x1e293b, metalness: 0.7, roughness: 0.3 });
            const powerStation = new THREE.Mesh(powerStationGeo, powerStationMat);
            powerStation.position.set(22, 5, 18);
            powerStation.castShadow = true;
            scene.add(powerStation);

            // Turbines Inside Power Station (Visualized as glowing disks)
            for (let i = 0; i < 3; i++) {
                const turbineGeo = new THREE.CylinderGeometry(2, 2, 1, 16);
                const turbineMat = new THREE.MeshStandardMaterial({ color: 0x00f0ff, emissive: 0x00f0ff, emissiveIntensity: 0.5 });
                const turbine = new THREE.Mesh(turbineGeo, turbineMat);
                turbine.position.set(16 + i * 6, 1, 18);
                scene.add(turbine);
                turbineMeshes.push(turbine);
            }

            // F. ESP32 Ultrasonic Sensor Pole (Digital Twin Hotspot)
            const poleGeo = new THREE.CylinderGeometry(0.3, 0.3, 14);
            const poleMat = new THREE.MeshStandardMaterial({ color: 0x94a3b8 });
            const pole = new THREE.Mesh(poleGeo, poleMat);
            pole.position.set(-28, 15, -6);
            scene.add(pole);

            // Sensor Box
            const sensorBoxGeo = new THREE.BoxGeometry(2, 1.5, 2);
            const sensorBoxMat = new THREE.MeshStandardMaterial({ color: 0x00f0ff, emissive: 0x00f0ff, emissiveIntensity: 0.8 });
            const sensorBox = new THREE.Mesh(sensorBoxGeo, sensorBoxMat);
            sensorBox.position.set(-28, 22, -6);
            scene.add(sensorBox);

            // G. Rain Simulation System
            createRainParticleSystem();
        }

        // Particle System for Rain Simulation
        function createRainParticleSystem() {
            const particleCount = 2000;
            const geometry = new THREE.BufferGeometry();
            const positions = new Float32Array(particleCount * 3);

            for (let i = 0; i < particleCount * 3; i += 3) {
                positions[i] = (Math.random() - 0.5) * 160;
                positions[i + 1] = Math.random() * 80;
                positions[i + 2] = (Math.random() - 0.5) * 160;
            }

            geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
            const material = new THREE.PointsMaterial({
                color: 0x38bdf8,
                size: 0.4,
                transparent: true,
                opacity: 0.0
            });

            rainParticles = new THREE.Points(geometry, material);
            scene.add(rainParticles);
        }

        // --- 4. Animation Loop ---
        function animate() {
            requestAnimationFrame(animate);

            const delta = clock.getDelta();
            const time = clock.getElapsedTime();

            // A. Animate Water Surface (Vertical wave oscillation)
            if (reservoirWaterMesh) {
                const pos = reservoirWaterMesh.geometry.attributes.position;
                for (let i = 0; i < pos.count; i++) {
                    const u = pos.getX(i);
                    const v = pos.getZ(i);
                    const z = Math.sin(u * 0.2 + time * 2) * 0.25 + Math.cos(v * 0.2 + time * 1.5) * 0.25;
                    pos.setY(i, z);
                }
                reservoirWaterMesh.geometry.attributes.position.needsUpdate = true;

                // Adjust Reservoir Y height based on water level state (0% = Y: 4, 100% = Y: 21)
                const targetY = 4 + (systemState.waterLevel / 100) * 17;
                reservoirWaterMesh.position.y += (targetY - reservoirWaterMesh.position.y) * 0.05;
            }

            // B. Animate Spillway Water Flow & Gate Height
            if (damGateMesh) {
                const targetGateY = 14 + (systemState.gateOpenPct / 100) * 8;
                damGateMesh.position.y += (targetGateY - damGateMesh.position.y) * 0.05;
            }

            if (spillwayWaterFlow) {
                // Opacity increases as gate opens
                const targetOpacity = (systemState.gateOpenPct / 100) * 0.85;
                spillwayWaterFlow.material.opacity += (targetOpacity - spillwayWaterFlow.material.opacity) * 0.05;
            }

            // C. Rotate Hydro Turbines
            turbineMeshes.forEach(turbine => {
                turbine.rotation.y += (systemState.turbineRpm / 60) * delta * 2;
            });

            // D. Animate Rain Particles
            if (rainParticles && systemState.isRaining) {
                const pos = rainParticles.geometry.attributes.position;
                for (let i = 1; i < pos.count * 3; i += 3) {
                    pos.array[i] -= 2.5;
                    if (pos.array[i] < 0) pos.array[i] = 80;
                }
                pos.needsUpdate = true;
            }

            // Update Controls
            controls.update();

            // Render
            renderer.render(scene, camera);
        }

        // Handle Window Resize
        function onWindowResize() {
            camera.aspect = window.innerWidth / window.innerHeight;
            camera.updateProjectionMatrix();
            renderer.setSize(window.innerWidth, window.innerHeight);
        }

        // Camera Preset Controller
        function setCameraView(preset) {
            switch(preset) {
                case 'overview':
                    animateCamera({ x: 60, y: 45, z: 75 }, { x: 0, y: 5, z: 0 });
                    break;
                case 'spillway':
                    animateCamera({ x: 10, y: 22, z: 30 }, { x: 0, y: 10, z: 0 });
                    break;
                case 'turbines':
                    animateCamera({ x: 45, y: 15, z: 35 }, { x: 20, y: 5, z: 18 });
                    break;
                case 'sensor':
                    animateCamera({ x: -45, y: 28, z: 10 }, { x: -28, y: 18, z: -6 });
                    break;
            }
        }

        function animateCamera(targetPos, targetLookAt) {
            let progress = 0;
            const startPos = { ...camera.position };
            const startTarget = { ...controls.target };

            function step() {
                progress += 0.04;
                if (progress <= 1) {
                    camera.position.x = startPos.x + (targetPos.x - startPos.x) * progress;
                    camera.position.y = startPos.y + (targetPos.y - startPos.y) * progress;
                    camera.position.z = startPos.z + (targetPos.z - startPos.z) * progress;

                    controls.target.x = startTarget.x + (targetLookAt.x - startTarget.x) * progress;
                    controls.target.y = startTarget.y + (targetLookAt.y - startTarget.y) * progress;
                    controls.target.z = startTarget.z + (targetLookAt.z - startTarget.z) * progress;

                    requestAnimationFrame(step);
                }
            }
            step();
        }

        // --- 5. Real-Time Logic & Dashboard Updates ---
        let telemetryChart;

        function initChart() {
            const ctx = document.getElementById('telemetryChart').getContext('2d');
            telemetryChart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: ['10:00', '10:01', '10:02', '10:03', '10:04', '10:05'],
                    datasets: [{
                        label: 'Water Level %',
                        data: [45, 48, 50, 52, 51, 50],
                        borderColor: '#00f0ff',
                        backgroundColor: 'rgba(0, 240, 255, 0.1)',
                        fill: true,
                        tension: 0.4,
                        borderWidth: 2
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: { legend: { display: false } },
                    scales: {
                        x: { grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#64748b', font: { size: 9 } } },
                        y: { min: 0, max: 100, grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#64748b', font: { size: 9 } } }
                    }
                }
            });
        }

        function updateUI() {
            // Water Level & Distance
            document.getElementById('val-water-pct').innerText = `${systemState.waterLevel.toFixed(1)}%`;
            const dist = 50 - (systemState.waterLevel / 100) * 45;
            document.getElementById('val-water-dist').innerText = `Sensor Dist: ${dist.toFixed(1)} cm`;
            document.getElementById('water-gauge-circle').style.strokeDasharray = `${systemState.waterLevel}, 100`;

            // Alarm Banner Check
            const alarmBanner = document.getElementById('alarm-banner');
            if (systemState.waterLevel >= 80) {
                alarmBanner.classList.remove('hidden');
                document.getElementById('val-water-pct').className = "font-orbitron text-2xl font-bold text-red-400 glow-text-red";
            } else {
                alarmBanner.classList.add('hidden');
                document.getElementById('val-water-pct').className = "font-orbitron text-2xl font-bold text-cyber-accent glow-text-cyan";
            }

            // Inflow / Outflow / Power / Relay
            document.getElementById('val-inflow').innerText = `${systemState.inflowRate} m³/s`;
            document.getElementById('val-outflow').innerText = `${systemState.outflowRate} m³/s`;
            document.getElementById('val-power').innerText = `${systemState.powerOutput.toFixed(1)} MW`;
            document.getElementById('val-rpm').innerText = `${systemState.turbineRpm} RPM`;

            const relayElem = document.getElementById('val-relay');
            if (systemState.waterLevel >= 80 || systemState.gateOpenPct > 0) {
                relayElem.innerText = "ON (Active)";
                relayElem.className = "font-mono text-xs px-2 py-0.5 rounded bg-emerald-950 text-emerald-400 border border-emerald-700";
            } else {
                relayElem.innerText = "OFF (Closed)";
                relayElem.className = "font-mono text-xs px-2 py-0.5 rounded bg-slate-800 text-slate-400 border border-slate-700";
            }
        }

        // Control Panel Interactive Functions
        function setMode(mode) {
            systemState.mode = mode;
            ['auto', 'manual', 'emergency'].forEach(m => {
                const btn = document.getElementById(`btn-mode-${m}`);
                if (m === mode) {
                    btn.className = "px-3 py-1 rounded-md font-semibold transition bg-cyber-accent text-black";
                } else {
                    btn.className = "px-3 py-1 rounded-md font-semibold transition text-slate-400 hover:text-white";
                }
            });

            if (mode === 'emergency') {
                updateGateSlider(100);
                addLog("EMERGENCY OVERRIDE: Spillway Gates Opened 100%", "red");
            } else if (mode === 'auto') {
                addLog("System switched to Autonomous AI Control mode", "cyan");
            }
        }

        function updateGateSlider(val) {
            systemState.gateOpenPct = parseFloat(val);
            document.getElementById('gate-angle-val').innerText = `${val}%`;
            document.getElementById('gate-slider').value = val;
            
            // Outflow calculation based on gate %
            systemState.outflowRate = 180 + Math.round((val / 100) * 850);
            updateUI();
        }

        function toggleRain() {
            systemState.isRaining = !systemState.isRaining;
            const btnText = document.getElementById('rain-status-text');
            if (systemState.isRaining) {
                btnText.innerText = "HEAVY RAIN";
                btnText.className = "text-blue-400 font-bold";
                rainParticles.material.opacity = 0.6;
                addLog("Weather event simulated: Heavy Torrential Rain", "cyan");
            } else {
                btnText.innerText = "OFF";
                btnText.className = "text-slate-500";
                rainParticles.material.opacity = 0.0;
                addLog("Weather event cleared: Normal Conditions", "emerald");
            }
        }

        function addLog(msg, color = 'cyan') {
            const container = document.getElementById('log-container');
            const now = new Date().toTimeString().split(' ')[0];
            const borderColors = {
                cyan: 'border-cyan-400',
                emerald: 'border-emerald-400',
                red: 'border-red-500 animate-pulse'
            };

            const logItem = document.createElement('div');
            logItem.className = `p-1.5 rounded bg-slate-950/80 border-l-2 ${borderColors[color] || 'border-cyan-400'} text-slate-300`;
            logItem.innerHTML = `<span class="text-slate-500">[${now}]</span> ${msg}`;
            container.prepend(logItem);
        }

        function clearLogs() {
            document.getElementById('log-container').innerHTML = '';
        }

        // Live Clock
        setInterval(() => {
            const now = new Date();
            document.getElementById('live-clock').innerText = now.toTimeString().split(' ')[0] + " UTC";
            document.getElementById('live-date').innerText = now.toISOString().split('T')[0];

            // Simulation step: Rain increases level, Gate decreases level
            if (systemState.isRaining) {
                systemState.waterLevel = Math.min(100, systemState.waterLevel + 0.3);
            }
            if (systemState.gateOpenPct > 0) {
                systemState.waterLevel = Math.max(10, systemState.waterLevel - (systemState.gateOpenPct / 100) * 0.4);
            }

            // Autonomous Mode Hysteresis logic
            if (systemState.mode === 'auto') {
                if (systemState.waterLevel >= 80 && systemState.gateOpenPct === 0) {
                    updateGateSlider(80);
                    addLog("AUTONOMOUS ACTION: Water >= 80%. Spillway opened automatically!", "red");
                } else if (systemState.waterLevel <= 40 && systemState.gateOpenPct > 0) {
                    updateGateSlider(0);
                    addLog("AUTONOMOUS ACTION: Water <= 40%. Spillway closed.", "emerald");
                }
            }

            // Update Chart Data Stream
            if (telemetryChart) {
                const labels = telemetryChart.data.labels;
                labels.shift();
                labels.push(now.toTimeString().split(' ')[0].substring(0, 5));
                telemetryChart.data.datasets[0].data.shift();
                telemetryChart.data.datasets[0].data.push(systemState.waterLevel);
                telemetryChart.update();
            }

            updateUI();
        }, 1500);

        // --- 6. MQTT Integration ---
        function initMQTT() {
            const clientID = "WebTwinClient_" + Math.random().toString(16).substr(2, 8);
            const client = new Paho.MQTT.Client("broker.hivemq.com", 8000, clientID);

            client.onConnectionLost = onConnectionLost;
            client.onMessageArrived = onMessageArrived;

            client.connect({
                onSuccess: () => {
                    document.getElementById('mqtt-status-dot').className = "h-2.5 w-2.5 rounded-full bg-emerald-400";
                    document.getElementById('mqtt-status-text').innerText = "MQTT ONLINE";
                    document.getElementById('mqtt-status-text').className = "text-emerald-400 font-semibold";
                    client.subscribe("dam/water_level");
                    addLog("MQTT Connected to HiveMQ Broker (dam/water_level)", "emerald");
                },
                onFailure: () => {
                    document.getElementById('mqtt-status-dot').className = "h-2.5 w-2.5 rounded-full bg-red-400";
                    document.getElementById('mqtt-status-text').innerText = "DISCONNECTED";
                    document.getElementById('mqtt-status-text').className = "text-red-400 font-semibold";
                }
            });

            function onConnectionLost(responseObject) {
                if (responseObject.errorCode !== 0) {
                    addLog("MQTT Connection Lost. Retrying...", "red");
                }
            }

            function onMessageArrived(message) {
                try {
                    const payload = JSON.parse(message.payloadString);
                    if (payload.water_level !== undefined) {
                        systemState.waterLevel = parseFloat(payload.water_level);
                        updateUI();
                        addLog(`MQTT Payload Received: Level ${systemState.waterLevel}%`, "cyan");
                    }
                } catch (e) {
                    // Raw number fallback
                    if (!isNaN(message.payloadString)) {
                        systemState.waterLevel = parseFloat(message.payloadString);
                        updateUI();
                    }
                }
            }
        }

        // Window Load Initialization
        window.onload = function () {
            init3D();
            animate();
            initChart();
            updateUI();
            initMQTT();
        };
    </script>
</body>
</html>
