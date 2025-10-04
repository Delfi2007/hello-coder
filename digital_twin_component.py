"""
Three.js Digital Twin Component for SAR Disaster Lens
Advanced 3D visualization of Earth processes using SAR data
"""

import streamlit as st
import streamlit.components.v1 as components

def create_digital_twin_component(width=800, height=600):
    """Create an advanced Three.js digital twin visualization component"""
    
    html_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>SAR Digital Twin</title>
        <style>
            body {{
                margin: 0;
                padding: 0;
                overflow: hidden;
                background: linear-gradient(135deg, #000428 0%, #004e92 100%);
                font-family: 'Arial', sans-serif;
            }}
            
            #container {{
                width: {width}px;
                height: {height}px;
                position: relative;
                border-radius: 15px;
                overflow: hidden;
                box-shadow: 0 20px 50px rgba(0,0,0,0.3);
            }}
            
            #threejs-canvas {{
                width: 100%;
                height: 100%;
                display: block;
            }}
            
            .ui-overlay {{
                position: absolute;
                color: white;
                font-size: 14px;
                z-index: 100;
            }}
            
            .top-left {{
                top: 20px;
                left: 20px;
            }}
            
            .top-right {{
                top: 20px;
                right: 20px;
                text-align: right;
            }}
            
            .bottom-left {{
                bottom: 20px;
                left: 20px;
            }}
            
            .bottom-right {{
                bottom: 20px;
                right: 20px;
                text-align: right;
            }}
            
            .control-panel {{
                background: rgba(0,0,0,0.8);
                padding: 15px;
                border-radius: 10px;
                backdrop-filter: blur(10px);
            }}
            
            .status-indicator {{
                display: inline-block;
                width: 12px;
                height: 12px;
                border-radius: 50%;
                margin-right: 8px;
                animation: pulse 2s infinite;
            }}
            
            .status-active {{ background: #00ff00; }}
            .status-warning {{ background: #ffaa00; }}
            .status-error {{ background: #ff0000; }}
            
            @keyframes pulse {{
                0% {{ opacity: 1; }}
                50% {{ opacity: 0.5; }}
                100% {{ opacity: 1; }}
            }}
            
            .data-stream {{
                font-family: 'Courier New', monospace;
                font-size: 12px;
                line-height: 1.4;
            }}
            
            button {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 5px;
                cursor: pointer;
                margin: 2px;
                font-size: 12px;
            }}
            
            button:hover {{
                opacity: 0.8;
            }}
        </style>
    </head>
    <body>
        <div id="container">
            <canvas id="threejs-canvas"></canvas>
            
            <!-- UI Overlays -->
            <div class="ui-overlay top-left">
                <div class="control-panel">
                    <h3>🛰️ SAR Digital Twin</h3>
                    <p><span class="status-indicator status-active"></span>Sentinel-1 Active</p>
                    <p><span class="status-indicator status-active"></span>Real-time Processing</p>
                    <p><span class="status-indicator status-warning"></span>Data Latency: 6h</p>
                    <div style="margin-top: 10px;">
                        <button onclick="toggleAnimation()">⏯️ Animation</button>
                        <button onclick="resetView()">🔄 Reset View</button>
                        <button onclick="toggleWireframe()">🔳 Wireframe</button>
                    </div>
                </div>
            </div>
            
            <div class="ui-overlay top-right">
                <div class="control-panel">
                    <h4>📊 Live Data Stream</h4>
                    <div class="data-stream" id="dataStream">
                        <div>VV: -12.3 dB ↑</div>
                        <div>VH: -18.7 dB ↓</div>
                        <div>Coherence: 0.78 →</div>
                        <div>Incidence: 38.2° →</div>
                    </div>
                </div>
            </div>
            
            <div class="ui-overlay bottom-left">
                <div class="control-panel">
                    <h4>🎮 Controls</h4>
                    <p>🖱️ Mouse: Rotate & Zoom</p>
                    <p>⌨️ WASD: Navigate</p>
                    <p>🎮 Space: Play/Pause</p>
                    <p>🔢 1-5: Layer Toggle</p>
                </div>
            </div>
            
            <div class="ui-overlay bottom-right">
                <div class="control-panel">
                    <h4>📍 Location Info</h4>
                    <div id="locationInfo">
                        <p>Lat: 23.8563° N</p>
                        <p>Lon: 90.3564° E</p>
                        <p>Elevation: 45m</p>
                        <p>Process: Flood Monitoring</p>
                    </div>
                </div>
            </div>
        </div>
        
        <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/controls/OrbitControls.js"></script>
        <script>
            // Global variables
            let scene, camera, renderer, controls;
            let earth, sarData, atmosphere;
            let animationRunning = true;
            let wireframeMode = false;
            let currentTime = 0;
            
            // Initialize the 3D scene
            function init() {{
                const container = document.getElementById('container');
                const canvas = document.getElementById('threejs-canvas');
                
                // Scene setup
                scene = new THREE.Scene();
                scene.fog = new THREE.Fog(0x000428, 50, 200);
                
                // Camera setup
                camera = new THREE.PerspectiveCamera(
                    60, 
                    container.offsetWidth / container.offsetHeight, 
                    0.1, 
                    1000
                );
                camera.position.set(20, 10, 20);
                
                // Renderer setup
                renderer = new THREE.WebGLRenderer({{ 
                    canvas: canvas, 
                    antialias: true,
                    alpha: true 
                }});
                renderer.setSize(container.offsetWidth, container.offsetHeight);
                renderer.setClearColor(0x000428, 1);
                renderer.shadowMap.enabled = true;
                renderer.shadowMap.type = THREE.PCFSoftShadowMap;
                
                // Controls
                controls = new THREE.OrbitControls(camera, renderer.domElement);
                controls.enableDamping = true;
                controls.dampingFactor = 0.05;
                controls.minDistance = 10;
                controls.maxDistance = 100;
                
                // Create Earth
                createEarth();
                
                // Create SAR data visualization
                createSARData();
                
                // Create atmosphere effect
                createAtmosphere();
                
                // Lighting
                setupLighting();
                
                // Start animation
                animate();
                
                // Start data streaming simulation
                startDataStream();
            }}
            
            function createEarth() {{
                // Earth geometry
                const earthGeometry = new THREE.SphereGeometry(8, 64, 32);
                
                // Earth material with height-based coloring
                const earthMaterial = new THREE.ShaderMaterial({{
                    uniforms: {{
                        time: {{ value: 0.0 }},
                        colorLow: {{ value: new THREE.Color(0x2E7D32) }}, // Dark green
                        colorMid: {{ value: new THREE.Color(0x8BC34A) }}, // Light green  
                        colorHigh: {{ value: new THREE.Color(0x795548) }}, // Brown
                        colorWater: {{ value: new THREE.Color(0x1976D2) }} // Blue
                    }},
                    vertexShader: `
                        varying vec3 vPosition;
                        varying vec3 vNormal;
                        varying vec2 vUv;
                        
                        void main() {{
                            vPosition = position;
                            vNormal = normal;
                            vUv = uv;
                            gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
                        }}
                    `,
                    fragmentShader: `
                        uniform float time;
                        uniform vec3 colorLow;
                        uniform vec3 colorMid;
                        uniform vec3 colorHigh;
                        uniform vec3 colorWater;
                        
                        varying vec3 vPosition;
                        varying vec3 vNormal;
                        varying vec2 vUv;
                        
                        // Simple noise function
                        float noise(vec2 st) {{
                            return fract(sin(dot(st.xy, vec2(12.9898,78.233))) * 43758.5453123);
                        }}
                        
                        void main() {{
                            // Create terrain-like patterns
                            float height = noise(vUv * 10.0 + time * 0.1);
                            float water = step(0.3, height);
                            
                            vec3 color;
                            if (water > 0.5) {{
                                // Land areas
                                if (height < 0.5) {{
                                    color = mix(colorLow, colorMid, (height - 0.3) / 0.2);
                                }} else {{
                                    color = mix(colorMid, colorHigh, (height - 0.5) / 0.5);
                                }}
                            }} else {{
                                // Water areas
                                color = colorWater;
                            }}
                            
                            // Add some atmospheric scattering effect
                            float fresnel = pow(1.0 - dot(vNormal, vec3(0, 0, 1)), 2.0);
                            color = mix(color, vec3(0.5, 0.8, 1.0), fresnel * 0.1);
                            
                            gl_FragColor = vec4(color, 1.0);
                        }}
                    `
                }});
                
                earth = new THREE.Mesh(earthGeometry, earthMaterial);
                earth.receiveShadow = true;
                scene.add(earth);
            }}
            
            function createSARData() {{
                // Create SAR data points
                const sarGeometry = new THREE.BufferGeometry();
                const positions = [];
                const colors = [];
                const sizes = [];
                
                // Generate SAR data points on Earth surface
                for (let i = 0; i < 2000; i++) {{
                    // Spherical coordinates
                    const phi = Math.acos(2 * Math.random() - 1);
                    const theta = 2 * Math.PI * Math.random();
                    const radius = 8.2; // Slightly above Earth surface
                    
                    const x = radius * Math.sin(phi) * Math.cos(theta);
                    const y = radius * Math.sin(phi) * Math.sin(theta);
                    const z = radius * Math.cos(phi);
                    
                    positions.push(x, y, z);
                    
                    // Color based on SAR intensity (simulated)
                    const intensity = Math.random();
                    if (intensity > 0.8) {{
                        // High intensity - red (potential disaster)
                        colors.push(1, 0.2, 0.2);
                    }} else if (intensity > 0.6) {{
                        // Medium intensity - yellow (monitoring)
                        colors.push(1, 1, 0.2);
                    }} else {{
                        // Low intensity - green (normal)
                        colors.push(0.2, 1, 0.2);
                    }}
                    
                    sizes.push(Math.random() * 3 + 1);
                }}
                
                sarGeometry.setAttribute('position', new THREE.Float32BufferAttribute(positions, 3));
                sarGeometry.setAttribute('color', new THREE.Float32BufferAttribute(colors, 3));
                sarGeometry.setAttribute('size', new THREE.Float32BufferAttribute(sizes, 1));
                
                const sarMaterial = new THREE.ShaderMaterial({{
                    uniforms: {{
                        time: {{ value: 0.0 }},
                        pointSize: {{ value: 2.0 }}
                    }},
                    vertexShader: `
                        attribute float size;
                        varying vec3 vColor;
                        uniform float time;
                        uniform float pointSize;
                        
                        void main() {{
                            vColor = color;
                            vec4 mvPosition = modelViewMatrix * vec4(position, 1.0);
                            gl_PointSize = size * pointSize * (300.0 / -mvPosition.z);
                            gl_Position = projectionMatrix * mvPosition;
                        }}
                    `,
                    fragmentShader: `
                        varying vec3 vColor;
                        uniform float time;
                        
                        void main() {{
                            vec2 center = gl_PointCoord - vec2(0.5);
                            float dist = length(center);
                            
                            if (dist > 0.5) discard;
                            
                            float alpha = 1.0 - smoothstep(0.3, 0.5, dist);
                            alpha *= 0.8 + 0.2 * sin(time * 3.0);
                            
                            gl_FragColor = vec4(vColor, alpha);
                        }}
                    `,
                    transparent: true,
                    vertexColors: true
                }});
                
                sarData = new THREE.Points(sarGeometry, sarMaterial);
                scene.add(sarData);
            }}
            
            function createAtmosphere() {{
                const atmosphereGeometry = new THREE.SphereGeometry(9, 32, 16);
                const atmosphereMaterial = new THREE.ShaderMaterial({{
                    uniforms: {{
                        time: {{ value: 0.0 }}
                    }},
                    vertexShader: `
                        varying vec3 vNormal;
                        void main() {{
                            vNormal = normalize(normalMatrix * normal);
                            gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
                        }}
                    `,
                    fragmentShader: `
                        varying vec3 vNormal;
                        uniform float time;
                        
                        void main() {{
                            float intensity = pow(0.6 - dot(vNormal, vec3(0, 0, 1.0)), 2.0);
                            vec3 atmosphere = vec3(0.3, 0.6, 1.0) * intensity;
                            gl_FragColor = vec4(atmosphere, intensity * 0.3);
                        }}
                    `,
                    side: THREE.BackSide,
                    transparent: true,
                    blending: THREE.AdditiveBlending
                }});
                
                atmosphere = new THREE.Mesh(atmosphereGeometry, atmosphereMaterial);
                scene.add(atmosphere);
            }}
            
            function setupLighting() {{
                // Ambient light
                const ambientLight = new THREE.AmbientLight(0x404040, 0.3);
                scene.add(ambientLight);
                
                // Directional light (sun)
                const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);
                directionalLight.position.set(50, 50, 25);
                directionalLight.castShadow = true;
                directionalLight.shadow.mapSize.width = 2048;
                directionalLight.shadow.mapSize.height = 2048;
                scene.add(directionalLight);
                
                // Point light for dramatic effect
                const pointLight = new THREE.PointLight(0x4488ff, 0.5, 100);
                pointLight.position.set(15, 15, 15);
                scene.add(pointLight);
            }}
            
            function animate() {{
                requestAnimationFrame(animate);
                
                if (animationRunning) {{
                    currentTime += 0.01;
                    
                    // Update shader uniforms
                    if (earth.material.uniforms) {{
                        earth.material.uniforms.time.value = currentTime;
                    }}
                    
                    if (sarData.material.uniforms) {{
                        sarData.material.uniforms.time.value = currentTime;
                    }}
                    
                    if (atmosphere.material.uniforms) {{
                        atmosphere.material.uniforms.time.value = currentTime;
                    }}
                    
                    // Rotate Earth slowly
                    earth.rotation.y += 0.002;
                    sarData.rotation.y += 0.002;
                    
                    // Animate SAR data points
                    const positions = sarData.geometry.attributes.position.array;
                    for (let i = 0; i < positions.length; i += 3) {{
                        const pulse = Math.sin(currentTime * 2 + i * 0.01) * 0.1;
                        const originalRadius = 8.2;
                        const newRadius = originalRadius + pulse;
                        
                        const x = positions[i];
                        const y = positions[i + 1];
                        const z = positions[i + 2];
                        const length = Math.sqrt(x*x + y*y + z*z);
                        
                        positions[i] = (x / length) * newRadius;
                        positions[i + 1] = (y / length) * newRadius;
                        positions[i + 2] = (z / length) * newRadius;
                    }}
                    sarData.geometry.attributes.position.needsUpdate = true;
                }}
                
                // Update controls
                controls.update();
                
                // Render
                renderer.render(scene, camera);
            }}
            
            function startDataStream() {{
                setInterval(() => {{
                    const dataStream = document.getElementById('dataStream');
                    const vv = (-15 + Math.random() * 6).toFixed(1);
                    const vh = (-20 + Math.random() * 8).toFixed(1);
                    const coherence = (0.3 + Math.random() * 0.5).toFixed(2);
                    const incidence = (30 + Math.random() * 20).toFixed(1);
                    
                    dataStream.innerHTML = `
                        <div>VV: ${{vv}} dB ${{Math.random() > 0.5 ? '↑' : '↓'}}</div>
                        <div>VH: ${{vh}} dB ${{Math.random() > 0.5 ? '↑' : '↓'}}</div>
                        <div>Coherence: ${{coherence}} ${{Math.random() > 0.5 ? '→' : '↔'}}</div>
                        <div>Incidence: ${{incidence}}° →</div>
                    `;
                }}, 2000);
            }}
            
            // Control functions
            function toggleAnimation() {{
                animationRunning = !animationRunning;
            }}
            
            function resetView() {{
                camera.position.set(20, 10, 20);
                controls.reset();
            }}
            
            function toggleWireframe() {{
                wireframeMode = !wireframeMode;
                earth.material.wireframe = wireframeMode;
            }}
            
            // Handle window resize
            function handleResize() {{
                const container = document.getElementById('container');
                camera.aspect = container.offsetWidth / container.offsetHeight;
                camera.updateProjectionMatrix();
                renderer.setSize(container.offsetWidth, container.offsetHeight);
            }}
            
            // Keyboard controls
            document.addEventListener('keydown', (event) => {{
                switch(event.key) {{
                    case ' ':
                        event.preventDefault();
                        toggleAnimation();
                        break;
                    case '1':
                        sarData.visible = !sarData.visible;
                        break;
                    case '2':
                        atmosphere.visible = !atmosphere.visible;
                        break;
                    case 'r':
                    case 'R':
                        resetView();
                        break;
                    case 'w':
                    case 'W':
                        toggleWireframe();
                        break;
                }}
            }});
            
            // Initialize when page loads
            window.addEventListener('load', init);
            window.addEventListener('resize', handleResize);
        </script>
    </body>
    </html>
    """
    
    return html_code

def render_digital_twin(width=800, height=600):
    """Render the digital twin component in Streamlit"""
    html_code = create_digital_twin_component(width, height)
    components.html(html_code, width=width, height=height)

# Additional utility functions for the digital twin
def create_sar_data_layers():
    """Create different SAR data layer configurations"""
    return {
        'flood_monitoring': {
            'colors': {'low': [0.2, 1.0, 0.2], 'medium': [1.0, 1.0, 0.2], 'high': [1.0, 0.2, 0.2]},
            'thresholds': {'low': -20, 'medium': -15, 'high': -10},
            'description': 'Water surface detection using VV polarization'
        },
        'fire_detection': {
            'colors': {'normal': [0.2, 1.0, 0.2], 'smoke': [0.8, 0.8, 0.2], 'fire': [1.0, 0.2, 0.2]},
            'thresholds': {'normal': -12, 'smoke': -8, 'fire': -5},
            'description': 'Burn scar mapping through temporal analysis'
        },
        'forest_monitoring': {
            'colors': {'dense': [0.1, 0.8, 0.1], 'sparse': [0.5, 1.0, 0.3], 'cleared': [0.8, 0.4, 0.2]},
            'thresholds': {'dense': -8, 'sparse': -12, 'cleared': -16},
            'description': 'Forest biomass estimation using cross-polarization'
        },
        'ice_dynamics': {
            'colors': {'solid': [0.7, 0.9, 1.0], 'moving': [0.3, 0.6, 1.0], 'water': [0.1, 0.3, 0.8]},
            'thresholds': {'solid': -6, 'moving': -10, 'water': -18},
            'description': 'Ice sheet and glacier monitoring'
        }
    }

def get_visualization_modes():
    """Get available visualization modes for the digital twin"""
    return {
        'backscatter_intensity': 'SAR Backscatter Intensity (dB)',
        'coherence_map': 'Interferometric Coherence',
        'phase_data': 'Interferometric Phase',
        'rgb_composite': 'False Color Composite (VV/VH/Ratio)',
        'polarimetric': 'Polarimetric Decomposition',
        'change_detection': 'Temporal Change Detection',
        'physical_parameters': 'Derived Physical Parameters'
    }

# Example usage in Streamlit app
if __name__ == "__main__":
    st.title("SAR Digital Twin Test")
    render_digital_twin(800, 600)