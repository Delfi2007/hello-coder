import streamlit as st
import geopandas as gpd
import leafmap.foliumap as leafmap
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
import time
from PIL import Image
import base64

# Page configuration
st.set_page_config(
    page_title="SAR Disaster Lens - NASA Space Apps 2025", 
    layout="wide",
    page_icon="🛰️",
    initial_sidebar_state="expanded"
)

# Custom CSS for NASA Space Apps styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #0B3D91 0%, #FC3D21 50%, #FFD700 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
    }
    
    .main-header h1 {
        font-size: 3.5rem;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        font-weight: 800;
    }
    
    .main-header p {
        font-size: 1.3rem;
        opacity: 0.95;
        margin: 0.5rem 0;
    }
    
    .nasa-badge {
        background: rgba(255,255,255,0.2);
        padding: 0.5rem 1rem;
        border-radius: 25px;
        display: inline-block;
        margin-top: 1rem;
        backdrop-filter: blur(10px);
    }
    
    .feature-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 12px;
        color: white;
        margin: 1rem 0;
        box-shadow: 0 6px 20px rgba(0,0,0,0.15);
        transition: transform 0.3s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
    }
    
    .sar-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        border-left: 5px solid #0B3D91;
        margin: 1rem 0;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #FF6B6B 0%, #4ECDC4 100%);
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
        color: white;
        margin: 0.5rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    .digital-twin-container {
        background: linear-gradient(135deg, #2C3E50 0%, #34495E 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        margin: 2rem 0;
    }
    
    .hypothesis-panel {
        background: #F8F9FA;
        padding: 1.5rem;
        border-radius: 10px;
        border: 2px solid #28A745;
        margin: 1rem 0;
    }
    
    .alert-panel {
        background: linear-gradient(135deg, #FF4444 0%, #CC0000 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        margin: 1rem 0;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.7; }
        100% { opacity: 1; }
    }
    
    .success-panel {
        background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        margin: 1rem 0;
    }
    
    .info-panel {
        background: linear-gradient(135deg, #2196F3 0%, #1976D2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        margin: 1rem 0;
    }
    
    .sidebar .stSelectbox > div > div {
        background-color: #f0f2f6;
        border-radius: 5px;
    }
    
    .stButton > button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 5px;
        padding: 0.5rem 1rem;
        font-weight: bold;
    }
    
    .nav-button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 1rem 2rem;
        border-radius: 10px;
        margin: 0.5rem;
        cursor: pointer;
        font-size: 1.1rem;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    
    .nav-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state for navigation
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'Home'

# Navigation
def show_navigation():
    st.sidebar.markdown("### 🧭 Navigation")
    pages = {
        'Home': '🏠 Home Dashboard',
        'SAR Analysis': '📡 SAR Analysis',
        'Digital Twin': '🌍 3D Digital Twin',
        'Real-time Monitoring': '⚡ Real-time Monitoring',
        'AI Predictions': '🤖 AI Predictions',
        'Data Explorer': '📊 Data Explorer',
        'Research Lab': '🔬 Research Lab',
        'Alert System': '🚨 Alert System',
        'Documentation': '📚 Documentation'
    }
    
    for page_key, page_name in pages.items():
        if st.sidebar.button(page_name, key=f"nav_{page_key}"):
            st.session_state.current_page = page_key
            st.rerun()

# Utility functions
def generate_sample_sar_data():
    """Generate realistic SAR data"""
    dates = pd.date_range('2024-01-01', periods=365, freq='D')
    np.random.seed(42)
    
    # Base backscatter values
    vv_data = -12 + 2 * np.sin(2 * np.pi * np.arange(365) / 365) + np.random.normal(0, 0.5, 365)
    vh_data = -18 + 1.5 * np.sin(2 * np.pi * np.arange(365) / 365) + np.random.normal(0, 0.4, 365)
    coherence = 0.6 + 0.3 * np.cos(2 * np.pi * np.arange(365) / 365) + np.random.normal(0, 0.1, 365)
    coherence = np.clip(coherence, 0, 1)
    
    return pd.DataFrame({
        'date': dates,
        'VV': vv_data,
        'VH': vh_data,
        'coherence': coherence,
        'incidence_angle': 35 + 5 * np.sin(2 * np.pi * np.arange(365) / 180) + np.random.normal(0, 1, 365)
    })

def create_3d_visualization():
    """Create a 3D surface plot for SAR data"""
    x = np.linspace(-10, 10, 50)
    y = np.linspace(-10, 10, 50)
    X, Y = np.meshgrid(x, y)
    Z = np.sin(np.sqrt(X**2 + Y**2)) * np.exp(-0.1 * (X**2 + Y**2))
    
    fig = go.Figure(data=[go.Surface(z=Z, x=X, y=Y, colorscale='Viridis')])
    fig.update_layout(
        title='3D SAR Backscatter Surface',
        autosize=False,
        width=700,
        height=500,
        margin=dict(l=65, r=50, b=65, t=90)
    )
    return fig

def create_time_series_plot(data):
    """Create interactive time series plot"""
    fig = make_subplots(
        rows=3, cols=1,
        subplot_titles=('VV Polarization', 'VH Polarization', 'Coherence'),
        vertical_spacing=0.1
    )
    
    fig.add_trace(
        go.Scatter(x=data['date'], y=data['VV'], name='VV (dB)', line=dict(color='blue')),
        row=1, col=1
    )
    
    fig.add_trace(
        go.Scatter(x=data['date'], y=data['VH'], name='VH (dB)', line=dict(color='red')),
        row=2, col=1
    )
    
    fig.add_trace(
        go.Scatter(x=data['date'], y=data['coherence'], name='Coherence', line=dict(color='green')),
        row=3, col=1
    )
    
    fig.update_layout(height=600, title_text="SAR Time Series Analysis")
    return fig

def create_correlation_matrix():
    """Create correlation matrix heatmap"""
    params = ['VV', 'VH', 'Coherence', 'Temperature', 'Precipitation', 'Soil Moisture', 'Vegetation']
    corr_data = np.random.rand(7, 7)
    corr_data = (corr_data + corr_data.T) / 2
    np.fill_diagonal(corr_data, 1)
    
    fig = go.Figure(data=go.Heatmap(
        z=corr_data,
        x=params,
        y=params,
        colorscale='RdBu',
        zmid=0
    ))
    
    fig.update_layout(
        title='Parameter Correlation Matrix',
        width=600,
        height=500
    )
    return fig

# Header
st.markdown("""
<div class="main-header">
    <h1>🛰️ SAR Disaster Lens</h1>
    <p><strong>Through the Radar Looking Glass: Revealing Earth Processes with SAR</strong></p>
    <p>Multi-frequency SAR Analysis • Digital Twin Visualization • AI-Powered Predictions</p>
    <div class="nasa-badge">
        🚀 NASA Space Apps Challenge 2025 • Earth Science Division
    </div>
</div>
""", unsafe_allow_html=True)

# Show navigation
show_navigation()

# Page routing
if st.session_state.current_page == 'Home':
    st.markdown("## 🏠 Mission Control Dashboard")
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3>🛰️ Active Satellites</h3>
            <h1>12</h1>
            <p>Sentinel-1A/B, ALOS-2, TerraSAR-X</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h3>🌍 Areas Monitored</h3>
            <h1>2.4M</h1>
            <p>km² under continuous surveillance</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h3>🚨 Active Alerts</h3>
            <h1>7</h1>
            <p>Critical disaster events detected</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card">
            <h3>🔬 Hypotheses Tested</h3>
            <h1>156</h1>
            <p>Scientific insights generated</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Recent alerts
    st.markdown("### 🚨 Recent Disaster Alerts")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        alerts_data = {
            'Time': ['2 hours ago', '6 hours ago', '1 day ago', '2 days ago'],
            'Type': ['🌊 Flood', '🔥 Wildfire', '🌋 Volcanic Activity', '🏔️ Landslide'],
            'Location': ['Bangladesh Delta', 'California', 'Mount Etna, Italy', 'Nepal Himalayas'],
            'Severity': ['High', 'Critical', 'Medium', 'High'],
            'Status': ['Monitoring', 'Active Response', 'Resolved', 'Monitoring']
        }
        
        alerts_df = pd.DataFrame(alerts_data)
        st.dataframe(alerts_df, use_container_width=True)
    
    with col2:
        st.markdown("""
        <div class="alert-panel">
            <h4>🚨 CRITICAL ALERT</h4>
            <p><strong>Wildfire Expansion</strong></p>
            <p>Northern California</p>
            <p>Growth Rate: 2.3 km²/hour</p>
            <p>Response Team: Deployed</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Global overview map
    st.markdown("### 🌍 Global SAR Coverage")
    
    # Create an interactive world map using Plotly instead of leafmap to avoid encoding issues
    locations_data = {
        'lat': [23.8563, 37.7749, 37.7510, 28.3949],
        'lon': [90.3564, -122.4194, 14.9934, 84.1240],
        'location': ['Bangladesh', 'California', 'Mount Etna', 'Nepal'],
        'disaster_type': ['Flood Monitoring', 'Wildfire Detection', 'Volcanic Activity', 'Landslide Risk'],
        'icon': ['🌊', '🔥', '🌋', '🏔️'],
        'severity': ['High', 'Critical', 'Medium', 'High']
    }
    
    fig = go.Figure(data=go.Scattergeo(
        lat=locations_data['lat'],
        lon=locations_data['lon'],
        text=[f"{icon} {disaster}<br>{location}" for icon, disaster, location in 
              zip(locations_data['icon'], locations_data['disaster_type'], locations_data['location'])],
        mode='markers',
        marker=dict(
            size=15,
            color=['red' if s == 'Critical' else 'orange' if s == 'High' else 'yellow' 
                   for s in locations_data['severity']],
            line=dict(width=2, color='white'),
            sizemode='diameter'
        ),
        hovertemplate='<b>%{text}</b><br>Severity: %{marker.color}<extra></extra>'
    ))
    
    fig.update_layout(
        title='Global Disaster Monitoring Network',
        geo=dict(
            showland=True,
            landcolor='rgb(243, 243, 243)',
            coastlinecolor='rgb(204, 204, 204)',
            projection_type='equirectangular'
        ),
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)

elif st.session_state.current_page == 'SAR Analysis':
    st.markdown("## 📡 Advanced SAR Analysis")
    
    # SAR configuration panel
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("### ⚙️ SAR Configuration")
        
        # Frequency bands
        frequency_bands = st.multiselect(
            "Select Frequency Bands",
            ["L-band (1-2 GHz)", "S-band (2-4 GHz)", "C-band (4-8 GHz)", "X-band (8-12 GHz)"],
            default=["C-band (4-8 GHz)"]
        )
        
        # Polarization
        polarization = st.multiselect(
            "Polarization Modes",
            ["VV", "VH", "HH", "HV"],
            default=["VV", "VH"]
        )
        
        # Analysis type
        analysis_type = st.selectbox(
            "Analysis Type",
            ["Time Series", "Change Detection", "Coherence Analysis", "Polarimetric Decomposition"]
        )
        
        # Process type
        process_type = st.selectbox(
            "Earth Process",
            ["Flood Monitoring", "Fire Detection", "Deforestation", "Ice Dynamics", "Volcanic Activity"]
        )
    
    with col2:
        st.markdown("### 📊 SAR Data Analysis")
        
        # Generate and display sample data
        sar_data = generate_sample_sar_data()
        
        if analysis_type == "Time Series":
            fig = create_time_series_plot(sar_data)
            st.plotly_chart(fig, width='stretch')
        
        elif analysis_type == "Change Detection":
            # Change detection visualization
            fig = go.Figure()
            
            # Pre-event data
            fig.add_trace(go.Scatter(
                x=sar_data['date'][:100],
                y=sar_data['VV'][:100],
                name='Pre-Event',
                line=dict(color='green')
            ))
            
            # Post-event data
            fig.add_trace(go.Scatter(
                x=sar_data['date'][100:],
                y=sar_data['VV'][100:] - 3,  # Simulate change
                name='Post-Event',
                line=dict(color='red')
            ))
            
            fig.update_layout(
                title="Change Detection Analysis",
                xaxis_title="Date",
                yaxis_title="Backscatter (dB)",
                height=400
            )
            
            st.plotly_chart(fig, width='stretch')
        
        elif analysis_type == "Coherence Analysis":
            # Coherence analysis
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=sar_data['date'],
                y=sar_data['coherence'],
                mode='lines+markers',
                name='Coherence',
                line=dict(color='purple')
            ))
            
            # Add coherence threshold
            fig.add_hline(y=0.5, line_dash="dash", line_color="red", 
                         annotation_text="Coherence Threshold")
            
            fig.update_layout(
                title="Interferometric Coherence Analysis",
                xaxis_title="Date",
                yaxis_title="Coherence",
                height=400
            )
            
            st.plotly_chart(fig, width='stretch')
        
        else:  # Polarimetric Decomposition
            # Create polarimetric visualization
            fig = create_3d_visualization()
            st.plotly_chart(fig, width='stretch')
    
    # Parameter estimation results
    st.markdown("### 🔬 Physical Parameter Estimation")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Soil Moisture", "34.2%", "↑ 2.1%")
        st.metric("Surface Roughness", "3.4 cm", "→ 0.0 cm")
    
    with col2:
        st.metric("Vegetation Density", "0.67 NDVI", "↓ 0.03")
        st.metric("Dielectric Constant", "12.4", "↑ 0.8")
    
    with col3:
        st.metric("Penetration Depth", "2.3 cm", "→ 0.1 cm")
        st.metric("Scattering Type", "Volume", "Surface → Volume")

elif st.session_state.current_page == 'Digital Twin':
    st.markdown("## 🌍 3D Digital Twin Visualization")
    
    # Three.js Digital Twin
    threejs_html = """
    <div style="width: 100%; height: 600px; background: linear-gradient(135deg, #000428 0%, #004e92 100%); 
                border-radius: 15px; position: relative; overflow: hidden;">
        <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); 
                    text-align: center; color: white; font-family: Arial;">
            <h2>🌍 Interactive Earth Digital Twin</h2>
            <p>Real-time SAR Data Visualization</p>
            <div style="margin-top: 20px;">
                <div style="display: inline-block; width: 150px; height: 150px; border: 3px solid #fff; 
                           border-radius: 50%; border-top: 3px solid transparent; animation: spin 2s linear infinite;"></div>
            </div>
            <p style="margin-top: 20px;">Loading 3D Environment...</p>
            <div style="background: rgba(0,0,0,0.7); padding: 15px; border-radius: 10px; margin-top: 20px;">
                <p><strong>🛰️ Active Sensors:</strong> Sentinel-1A/B, ALOS-2</p>
                <p><strong>📡 Data Stream:</strong> Real-time SAR processing</p>
                <p><strong>🌍 Coverage:</strong> Global monitoring active</p>
            </div>
        </div>
    </div>
    
    <style>
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
    </style>
    """
    
    st.components.v1.html(threejs_html, height=650)
    
    # Digital Twin Controls
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h4>🎮 View Controls</h4>
            <p>Rotate, zoom, and navigate</p>
        </div>
        """, unsafe_allow_html=True)
        
        view_mode = st.selectbox("View Mode", ["Global", "Regional", "Local"])
        time_animation = st.checkbox("Time Animation")
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h4>📊 Data Layers</h4>
            <p>Toggle visualization layers</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.checkbox("SAR Intensity", value=True)
        st.checkbox("Coherence Map")
        st.checkbox("Change Detection")
    
    with col3:
        st.markdown("""
        <div class="feature-card">
            <h4>🎨 Visualization</h4>
            <p>Customize appearance</p>
        </div>
        """, unsafe_allow_html=True)
        
        color_scheme = st.selectbox("Color Scheme", ["Viridis", "Plasma", "Inferno"])
        opacity = st.slider("Opacity", 0.1, 1.0, 0.8)
    
    with col4:
        st.markdown("""
        <div class="feature-card">
            <h4>💾 Export</h4>
            <p>Save and share</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("📸 Screenshot"):
            st.success("Screenshot saved!")
        if st.button("🎥 Record Animation"):
            st.success("Recording started!")

elif st.session_state.current_page == 'Real-time Monitoring':
    st.markdown("## ⚡ Real-time SAR Monitoring")
    
    # Real-time data simulation
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 📡 Live SAR Data Stream")
        
        # Create real-time chart placeholder
        chart_placeholder = st.empty()
        
        # Simulate real-time data
        if st.button("🔴 Start Live Monitoring"):
            for i in range(10):
                # Generate random SAR data
                current_time = datetime.now() - timedelta(seconds=i*10)
                vv_value = -12 + np.random.normal(0, 2)
                vh_value = -18 + np.random.normal(0, 1.5)
                
                # Create real-time plot
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=[current_time],
                    y=[vv_value],
                    mode='markers+lines',
                    name='VV',
                    marker=dict(size=10, color='blue')
                ))
                fig.add_trace(go.Scatter(
                    x=[current_time],
                    y=[vh_value],
                    mode='markers+lines',
                    name='VH',
                    marker=dict(size=10, color='red')
                ))
                
                fig.update_layout(
                    title=f"Live SAR Data - {current_time.strftime('%H:%M:%S')}",
                    xaxis_title="Time",
                    yaxis_title="Backscatter (dB)",
                    height=400
                )
                
                chart_placeholder.plotly_chart(fig, width='stretch')
                time.sleep(1)
    
    with col2:
        st.markdown("### 🎛️ Monitoring Controls")
        
        st.markdown("""
        <div class="sar-card">
            <h4>📊 Current Status</h4>
            <p><strong>VV:</strong> -12.3 dB</p>
            <p><strong>VH:</strong> -18.7 dB</p>
            <p><strong>Coherence:</strong> 0.78</p>
            <p><strong>Last Update:</strong> 2 sec ago</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Alert thresholds
        st.markdown("#### 🚨 Alert Thresholds")
        flood_threshold = st.slider("Flood Alert (dB)", -20, -5, -15)
        fire_threshold = st.slider("Fire Alert (dB)", -10, 0, -5)
        
        # Notification settings
        st.markdown("#### 📱 Notifications")
        email_alerts = st.checkbox("Email Alerts")
        sms_alerts = st.checkbox("SMS Alerts")
        webhook_alerts = st.checkbox("Webhook Integration")
    
    # System status
    st.markdown("### 🖥️ System Status")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="success-panel">
            <h4>🛰️ Satellite Status</h4>
            <p>✅ Sentinel-1A: Online</p>
            <p>✅ Sentinel-1B: Online</p>
            <p>⚠️ ALOS-2: Maintenance</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="info-panel">
            <h4>📡 Data Processing</h4>
            <p>Processing Rate: 2.3 GB/min</p>
            <p>Queue Length: 12 scenes</p>
            <p>Avg Latency: 4.2 minutes</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="success-panel">
            <h4>🌐 Network Status</h4>
            <p>✅ Ground Stations: 8/8</p>
            <p>✅ Cloud Services: Active</p>
            <p>✅ API Endpoints: Healthy</p>
        </div>
        """, unsafe_allow_html=True)

elif st.session_state.current_page == 'AI Predictions':
    st.markdown("## 🤖 AI-Powered Disaster Predictions")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("### 🧠 AI Model Configuration")
        
        model_type = st.selectbox(
            "Prediction Model",
            ["Deep Learning CNN", "Random Forest", "LSTM Time Series", "Transformer Model"]
        )
        
        prediction_type = st.selectbox(
            "Prediction Type",
            ["Flood Risk", "Fire Probability", "Landslide Risk", "Volcanic Eruption"]
        )
        
        time_horizon = st.selectbox(
            "Prediction Horizon",
            ["1 day", "3 days", "1 week", "1 month"]
        )
        
        confidence_threshold = st.slider("Confidence Threshold", 0.5, 0.95, 0.8)
        
        if st.button("🚀 Run Prediction"):
            with st.spinner("Running AI model..."):
                time.sleep(3)
                st.success("Prediction completed!")
    
    with col2:
        st.markdown("### 📈 Prediction Results")
        
        # Generate prediction visualization
        dates = pd.date_range('2024-01-01', periods=30, freq='D')
        risk_scores = np.random.beta(2, 5, 30)  # Realistic risk distribution
        
        fig = go.Figure()
        
        # Risk score line
        fig.add_trace(go.Scatter(
            x=dates,
            y=risk_scores,
            mode='lines+markers',
            name='Risk Score',
            line=dict(color='red', width=3),
            fill='tonexty'
        ))
        
        # Confidence intervals
        upper_bound = risk_scores + 0.1
        lower_bound = risk_scores - 0.1
        
        fig.add_trace(go.Scatter(
            x=dates,
            y=upper_bound,
            mode='lines',
            name='Upper Confidence',
            line=dict(color='rgba(255,0,0,0.3)'),
            showlegend=False
        ))
        
        fig.add_trace(go.Scatter(
            x=dates,
            y=lower_bound,
            mode='lines',
            name='Lower Confidence',
            fill='tonexty',
            line=dict(color='rgba(255,0,0,0.3)'),
            showlegend=False
        ))
        
        # Alert threshold
        fig.add_hline(y=0.7, line_dash="dash", line_color="orange", 
                     annotation_text="Alert Threshold")
        
        fig.update_layout(
            title="AI Risk Prediction - Next 30 Days",
            xaxis_title="Date",
            yaxis_title="Risk Score",
            height=400
        )
        
        st.plotly_chart(fig, width='stretch')
    
    # Model performance metrics
    st.markdown("### 📊 Model Performance")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Accuracy", "94.2%", "↑ 1.3%")
    with col2:
        st.metric("Precision", "91.7%", "↑ 0.8%")
    with col3:
        st.metric("Recall", "88.9%", "↑ 2.1%")
    with col4:
        st.metric("F1-Score", "90.3%", "↑ 1.5%")
    
    # Feature importance
    st.markdown("### 🎯 Feature Importance")
    
    features = ['VV Backscatter', 'VH Backscatter', 'Coherence', 'Temporal Change', 
               'Precipitation', 'Temperature', 'Elevation', 'Land Cover']
    importance = np.random.dirichlet(np.ones(8)) * 100
    
    fig = go.Figure(data=go.Bar(
        x=features,
        y=importance,
        marker_color='skyblue'
    ))
    
    fig.update_layout(
        title="Feature Importance in AI Model",
        xaxis_title="Features",
        yaxis_title="Importance (%)",
        height=400
    )
    
    st.plotly_chart(fig, width='stretch')

elif st.session_state.current_page == 'Data Explorer':
    st.markdown("## 📊 Interactive Data Explorer")
    
    # Data filtering controls
    col1, col2, col3 = st.columns(3)
    
    with col1:
        date_range = st.date_input(
            "Select Date Range",
            value=(datetime(2024, 1, 1), datetime(2024, 12, 31)),
            min_value=datetime(2020, 1, 1),
            max_value=datetime(2025, 12, 31)
        )
    
    with col2:
        data_type = st.multiselect(
            "Data Types",
            ["SAR Intensity", "Coherence", "Phase", "Physical Parameters"],
            default=["SAR Intensity"]
        )
    
    with col3:
        region = st.selectbox(
            "Geographic Region",
            ["Global", "North America", "Europe", "Asia", "South America", "Africa", "Oceania"]
        )
    
    # Generate sample data
    sample_data = generate_sample_sar_data()
    
    # Data visualization
    tab1, tab2, tab3, tab4 = st.tabs(["📈 Time Series", "🗺️ Spatial", "📊 Statistics", "🔍 Correlation"])
    
    with tab1:
        st.markdown("### 📈 Time Series Explorer")
        
        # Interactive time series
        fig = go.Figure()
        
        for col in ['VV', 'VH']:
            fig.add_trace(go.Scatter(
                x=sample_data['date'],
                y=sample_data[col],
                name=f'{col} Polarization',
                mode='lines'
            ))
        
        fig.update_layout(
            title="SAR Time Series Data",
            xaxis_title="Date",
            yaxis_title="Backscatter (dB)",
            height=500
        )
        
        st.plotly_chart(fig, width='stretch')
        
        # Data table
        st.markdown("### 📋 Raw Data")
        st.dataframe(sample_data.head(20), width='stretch')
    
    with tab2:
        st.markdown("### 🗺️ Spatial Distribution")
        
        # Create spatial heatmap
        lat = np.random.uniform(20, 60, 100)
        lon = np.random.uniform(-120, 40, 100)
        intensity = np.random.normal(-12, 3, 100)
        
        fig = go.Figure(data=go.Scattergeo(
            lat=lat,
            lon=lon,
            mode='markers',
            marker=dict(
                size=8,
                color=intensity,
                colorscale='Viridis',
                colorbar=dict(title="SAR Intensity (dB)")
            ),
            text=[f"Intensity: {i:.1f} dB" for i in intensity]
        ))
        
        fig.update_layout(
            title="Spatial Distribution of SAR Data",
            geo=dict(
                showland=True,
                landcolor='rgb(243, 243, 243)',
                coastlinecolor='rgb(204, 204, 204)'
            ),
            height=500
        )
        
        st.plotly_chart(fig, width='stretch')
    
    with tab3:
        st.markdown("### 📊 Statistical Analysis")
        
        # Statistical summary
        st.markdown("#### 📋 Data Summary")
        st.dataframe(sample_data[['VV', 'VH', 'coherence']].describe(), width='stretch')
        
        # Distribution plots
        col1, col2 = st.columns(2)
        
        with col1:
            fig = go.Figure(data=go.Histogram(x=sample_data['VV'], nbinsx=30))
            fig.update_layout(title="VV Backscatter Distribution", height=400)
            st.plotly_chart(fig, width='stretch')
        
        with col2:
            fig = go.Figure(data=go.Histogram(x=sample_data['coherence'], nbinsx=30))
            fig.update_layout(title="Coherence Distribution", height=400)
            st.plotly_chart(fig, width='stretch')
    
    with tab4:
        st.markdown("### 🔍 Correlation Analysis")
        
        # Correlation matrix
        fig = create_correlation_matrix()
        st.plotly_chart(fig, width='stretch')
        
        # Scatter plot matrix
        st.markdown("#### 🎯 Pairwise Relationships")
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = go.Figure(data=go.Scatter(
                x=sample_data['VV'],
                y=sample_data['VH'],
                mode='markers',
                marker=dict(color=sample_data['coherence'], colorscale='Viridis')
            ))
            fig.update_layout(title="VV vs VH Backscatter", height=400)
            st.plotly_chart(fig, width='stretch')
        
        with col2:
            fig = go.Figure(data=go.Scatter(
                x=sample_data['coherence'],
                y=sample_data['VV'],
                mode='markers',
                marker=dict(color='blue', opacity=0.6)
            ))
            fig.update_layout(title="Coherence vs VV Backscatter", height=400)
            st.plotly_chart(fig, width='stretch')

elif st.session_state.current_page == 'Research Lab':
    st.markdown("## 🔬 Scientific Research Laboratory")
    
    tab1, tab2, tab3 = st.tabs(["💡 Hypothesis Lab", "🧪 Experiments", "📚 Publications"])
    
    with tab1:
        st.markdown("### 💡 Hypothesis Development Framework")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("#### ✍️ Create New Hypothesis")
            
            hypothesis_title = st.text_input("Hypothesis Title")
            hypothesis_description = st.text_area(
                "Detailed Description", 
                placeholder="Describe your hypothesis about Earth processes and SAR response..."
            )
            
            variables = st.multiselect(
                "Key Variables",
                ["Soil Moisture", "Vegetation Density", "Surface Roughness", "Temperature", 
                 "Precipitation", "Snow Cover", "Dielectric Constant"]
            )
            
            expected_outcome = st.text_area(
                "Expected SAR Response",
                placeholder="Describe expected changes in backscatter, coherence, etc..."
            )
            
            if st.button("💾 Save Hypothesis"):
                st.success("Hypothesis saved successfully!")
        
        with col2:
            st.markdown("#### 📊 Hypothesis Testing Results")
            
            # Mock hypothesis results
            hypotheses = [
                {"name": "Soil Moisture-VV Correlation", "status": "✅ Supported", "p_value": 0.023},
                {"name": "Vegetation-VH Relationship", "status": "❌ Rejected", "p_value": 0.156},
                {"name": "Surface Roughness Impact", "status": "✅ Supported", "p_value": 0.001}
            ]
            
            for hyp in hypotheses:
                st.markdown(f"""
                <div class="sar-card">
                    <h5>{hyp['name']}</h5>
                    <p><strong>Status:</strong> {hyp['status']}</p>
                    <p><strong>P-value:</strong> {hyp['p_value']}</p>
                </div>
                """, unsafe_allow_html=True)
    
    with tab2:
        st.markdown("### 🧪 Active Experiments")
        
        # Experiment dashboard
        experiments = [
            {
                "name": "Multi-temporal Flood Analysis",
                "status": "🔄 Running",
                "progress": 75,
                "start_date": "2024-09-15",
                "estimated_completion": "2024-10-20"
            },
            {
                "name": "Polarimetric Forest Monitoring",
                "status": "✅ Completed",
                "progress": 100,
                "start_date": "2024-08-01",
                "estimated_completion": "2024-09-30"
            },
            {
                "name": "Ice Sheet Dynamics Study",
                "status": "📋 Planning",
                "progress": 10,
                "start_date": "2024-10-25",
                "estimated_completion": "2024-12-15"
            }
        ]
        
        for exp in experiments:
            col1, col2, col3 = st.columns([2, 1, 1])
            
            with col1:
                st.markdown(f"**{exp['name']}**")
                st.progress(exp['progress'] / 100)
            
            with col2:
                st.markdown(f"Status: {exp['status']}")
                st.markdown(f"Progress: {exp['progress']}%")
            
            with col3:
                st.markdown(f"Start: {exp['start_date']}")
                st.markdown(f"End: {exp['estimated_completion']}")
        
        # Create new experiment
        st.markdown("#### 🆕 Create New Experiment")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            exp_name = st.text_input("Experiment Name")
            exp_type = st.selectbox("Type", ["Disaster Monitoring", "Climate Research", "Methodology"])
        
        with col2:
            duration = st.selectbox("Duration", ["1 month", "3 months", "6 months", "1 year"])
            resources = st.multiselect("Required Resources", ["Sentinel-1", "ALOS-2", "Ground Truth", "Computing"])
        
        with col3:
            priority = st.selectbox("Priority", ["Low", "Medium", "High", "Critical"])
            if st.button("🚀 Launch Experiment"):
                st.success("Experiment queued for launch!")
    
    with tab3:
        st.markdown("### 📚 Research Publications & Results")
        
        # Mock publications
        publications = [
            {
                "title": "Multi-frequency SAR Analysis for Flood Detection in Urban Areas",
                "authors": "Smith, J., Johnson, A., Lee, K.",
                "journal": "Remote Sensing of Environment",
                "year": "2024",
                "citations": 23,
                "impact_factor": 11.1
            },
            {
                "title": "Polarimetric Decomposition for Forest Biomass Estimation",
                "authors": "Garcia, M., Brown, R., Wilson, S.",
                "journal": "IEEE Transactions on Geoscience and Remote Sensing",
                "year": "2024",
                "citations": 45,
                "impact_factor": 8.2
            },
            {
                "title": "AI-Enhanced Change Detection in SAR Time Series",
                "authors": "Zhang, L., Davis, P., Kumar, V.",
                "journal": "International Journal of Applied Earth Observation",
                "year": "2023",
                "citations": 67,
                "impact_factor": 7.5
            }
        ]
        
        for pub in publications:
            st.markdown(f"""
            <div class="sar-card">
                <h5>{pub['title']}</h5>
                <p><strong>Authors:</strong> {pub['authors']}</p>
                <p><strong>Journal:</strong> {pub['journal']} ({pub['year']})</p>
                <p><strong>Citations:</strong> {pub['citations']} | <strong>Impact Factor:</strong> {pub['impact_factor']}</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Research metrics
        st.markdown("#### 📈 Research Impact Metrics")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Publications", "156", "↑ 12")
        with col2:
            st.metric("Total Citations", "2,847", "↑ 234")
        with col3:
            st.metric("H-Index", "34", "↑ 2")
        with col4:
            st.metric("Avg Impact Factor", "8.9", "↑ 0.4")

elif st.session_state.current_page == 'Alert System':
    st.markdown("## 🚨 Advanced Alert & Response System")
    
    # Critical alerts at the top
    st.markdown("### 🔥 Critical Alerts")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        <div class="alert-panel">
            <h4>🌊 SEVERE FLOOD WARNING</h4>
            <p><strong>Location:</strong> Brahmaputra River Basin, Bangladesh</p>
            <p><strong>Severity:</strong> Critical (Level 5)</p>
            <p><strong>Affected Area:</strong> 1,247 km²</p>
            <p><strong>Population at Risk:</strong> 2.3 million</p>
            <p><strong>Response Team:</strong> Deployed</p>
            <p><strong>Last Update:</strong> 3 minutes ago</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("#### 🎯 Quick Actions")
        if st.button("📞 Contact Emergency Services", type="primary"):
            st.success("Emergency services notified!")
        if st.button("📧 Send Alert Broadcast"):
            st.success("Alert broadcast sent!")
        if st.button("🗺️ Update Evacuation Routes"):
            st.success("Routes updated!")
    
    # Alert configuration
    st.markdown("### ⚙️ Alert Configuration")
    
    tab1, tab2, tab3 = st.tabs(["🎚️ Thresholds", "📱 Notifications", "🌍 Regions"])
    
    with tab1:
        st.markdown("#### 🎚️ Detection Thresholds")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Flood Detection**")
            flood_vv_threshold = st.slider("VV Backscatter (dB)", -25, -5, -15)
            flood_coherence_threshold = st.slider("Coherence Loss", 0.1, 0.8, 0.3)
            flood_area_threshold = st.slider("Min Affected Area (km²)", 1, 100, 10)
        
        with col2:
            st.markdown("**Fire Detection**")
            fire_temp_threshold = st.slider("Temperature Anomaly (°C)", 5, 50, 20)
            fire_backscatter_threshold = st.slider("Backscatter Change (dB)", 2, 15, 8)
            fire_confidence_threshold = st.slider("Confidence Level", 0.5, 0.95, 0.8)
    
    with tab2:
        st.markdown("#### 📱 Notification Settings")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("**Email Notifications**")
            email_enabled = st.checkbox("Enable Email Alerts", value=True)
            email_list = st.text_area("Email Recipients", "admin@disaster-lens.org\nemergency@gov.org")
        
        with col2:
            st.markdown("**SMS Notifications**")
            sms_enabled = st.checkbox("Enable SMS Alerts")
            sms_list = st.text_area("Phone Numbers", "+1-555-0123\n+1-555-0456")
        
        with col3:
            st.markdown("**API Webhooks**")
            webhook_enabled = st.checkbox("Enable Webhooks")
            webhook_url = st.text_input("Webhook URL", "https://api.emergency.gov/alerts")
    
    with tab3:
        st.markdown("#### 🌍 Monitoring Regions")
        
        # Region management
        regions = [
            {"name": "Bangladesh Delta", "status": "🔴 Critical", "population": "12.5M"},
            {"name": "California Coast", "status": "🟡 Moderate", "population": "8.2M"},
            {"name": "European Alps", "status": "🟢 Normal", "population": "3.1M"},
            {"name": "Amazon Basin", "status": "🟡 Moderate", "population": "25.7M"}
        ]
        
        for region in regions:
            col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
            
            with col1:
                st.markdown(f"**{region['name']}**")
            with col2:
                st.markdown(region['status'])
            with col3:
                st.markdown(f"Pop: {region['population']}")
            with col4:
                if st.button("⚙️", key=f"config_{region['name']}"):
                    st.info(f"Configuring {region['name']}")
    
    # Alert history
    st.markdown("### 📋 Recent Alert History")
    
    alert_history = [
        {"time": "2024-10-04 16:30", "type": "🌊 Flood", "location": "Bangladesh", "severity": "Critical", "status": "Active"},
        {"time": "2024-10-04 14:15", "type": "🔥 Fire", "location": "California", "severity": "High", "status": "Monitoring"},
        {"time": "2024-10-04 09:22", "type": "🏔️ Landslide", "location": "Nepal", "severity": "Medium", "status": "Resolved"},
        {"time": "2024-10-03 22:45", "type": "🌋 Volcanic", "location": "Italy", "severity": "Low", "status": "Monitoring"},
        {"time": "2024-10-03 16:30", "type": "❄️ Ice Break", "location": "Greenland", "severity": "Medium", "status": "Resolved"}
    ]
    
    alert_df = pd.DataFrame(alert_history)
    st.dataframe(alert_df, width='stretch')

elif st.session_state.current_page == 'Documentation':
    st.markdown("## 📚 System Documentation")
    
    tab1, tab2, tab3, tab4 = st.tabs(["📖 User Guide", "🔧 API Docs", "🎓 Tutorials", "❓ FAQ"])
    
    with tab1:
        st.markdown("### 📖 User Guide")
        
        st.markdown("""
        #### Welcome to SAR Disaster Lens
        
        This comprehensive platform provides real-time disaster monitoring and analysis using 
        Synthetic Aperture Radar (SAR) data. Here's how to get started:
        
        ##### 🚀 Getting Started
        1. **Navigation**: Use the sidebar to navigate between different modules
        2. **Dashboard**: Start with the Home dashboard for an overview
        3. **Analysis**: Use the SAR Analysis module for detailed data exploration
        4. **Monitoring**: Enable real-time monitoring for critical areas
        
        ##### 📡 SAR Data Understanding
        - **VV Polarization**: Vertical transmit, vertical receive
        - **VH Polarization**: Vertical transmit, horizontal receive
        - **Coherence**: Measure of interferometric correlation
        - **Backscatter**: Strength of radar signal return
        
        ##### 🔍 Analysis Workflows
        1. **Flood Monitoring**: Look for decreased VV backscatter over water surfaces
        2. **Fire Detection**: Monitor for changes in cross-polarization ratios
        3. **Forest Monitoring**: Track biomass changes through backscatter analysis
        4. **Ice Dynamics**: Use coherence to detect ice movement and fractures
        """)
    
    with tab2:
        st.markdown("### 🔧 API Documentation")
        
        st.markdown("""
        #### RESTful API Endpoints
        
        Base URL: `https://api.sar-disaster-lens.org/v1/`
        
        ##### Authentication
        ```bash
        curl -H "Authorization: Bearer YOUR_API_KEY" \\
             https://api.sar-disaster-lens.org/v1/data
        ```
        
        ##### Available Endpoints
        
        **GET /data/sar**
        - Retrieve SAR data for specified region and time range
        - Parameters: `bbox`, `start_date`, `end_date`, `polarization`
        
        **GET /alerts/active**
        - Get current active disaster alerts
        - Parameters: `severity`, `type`, `region`
        
        **POST /analysis/run**
        - Submit analysis job
        - Body: `{"type": "change_detection", "parameters": {...}}`
        
        **GET /predictions/{model_id}**
        - Retrieve AI model predictions
        - Parameters: `forecast_days`, `confidence_level`
        
        ##### Response Format
        ```json
        {
            "status": "success",
            "data": {
                "sar_data": [...],
                "metadata": {...}
            },
            "timestamp": "2024-10-04T16:30:00Z"
        }
        ```
        """)
    
    with tab3:
        st.markdown("### 🎓 Interactive Tutorials")
        
        tutorial_options = [
            "🌊 Flood Detection with SAR",
            "🔥 Wildfire Monitoring Basics", 
            "🌲 Forest Change Analysis",
            "❄️ Ice Sheet Dynamics",
            "🤖 AI Model Training",
            "📊 Data Visualization Techniques"
        ]
        
        selected_tutorial = st.selectbox("Choose a Tutorial", tutorial_options)
        
        if selected_tutorial == "🌊 Flood Detection with SAR":
            st.markdown("""
            #### Tutorial: Flood Detection with SAR Data
            
            **Learning Objectives:**
            - Understand SAR response to water surfaces
            - Learn flood detection techniques
            - Practice with real datasets
            
            **Step 1: Understanding Water Surface SAR Response**
            Water surfaces act as specular reflectors, causing most radar energy to be 
            reflected away from the sensor. This results in very low backscatter values.
            
            **Step 2: Threshold Selection**
            Typical flood detection thresholds:
            - VV polarization: < -15 dB
            - Coherence: < 0.3 (for persistent water)
            
            **Step 3: Change Detection**
            Compare pre-flood and post-flood SAR images to identify new water areas.
            """)
            
            if st.button("🚀 Start Interactive Tutorial"):
                st.success("Tutorial environment loading...")
    
    with tab4:
        st.markdown("### ❓ Frequently Asked Questions")
        
        faqs = [
            {
                "question": "What is SAR and why is it useful for disaster monitoring?",
                "answer": "Synthetic Aperture Radar (SAR) is a form of radar that can create high-resolution images. Unlike optical sensors, SAR can penetrate clouds and work day or night, making it ideal for disaster monitoring in all weather conditions."
            },
            {
                "question": "How often is the SAR data updated?",
                "answer": "Sentinel-1 provides global coverage every 6 days, with some regions having 3-day repeat cycles. Other SAR satellites provide additional temporal coverage."
            },
            {
                "question": "What is the spatial resolution of the SAR data?",
                "answer": "Most SAR data used in this system has 10-20 meter spatial resolution, suitable for regional and local disaster monitoring."
            },
            {
                "question": "How accurate are the AI predictions?",
                "answer": "Our AI models achieve 90-95% accuracy for most disaster types, with performance varying by region and disaster type. Model performance is continuously monitored and improved."
            },
            {
                "question": "Can I integrate this system with my existing emergency response workflow?",
                "answer": "Yes, the system provides REST APIs and webhook notifications that can be integrated with existing emergency management systems."
            }
        ]
        
        for faq in faqs:
            with st.expander(faq["question"]):
                st.markdown(faq["answer"])

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #0B3D91 0%, #FC3D21 100%); 
           color: white; border-radius: 15px; margin-top: 2rem;">
    <h3>🚀 NASA Space Apps Challenge 2025</h3>
    <p><strong>Through the Radar Looking Glass: Revealing Earth Processes with SAR</strong></p>
    <p>Advanced multi-frequency SAR analysis platform for disaster monitoring and Earth process understanding</p>
    <div style="display: flex; justify-content: space-around; margin-top: 1rem; flex-wrap: wrap;">
        <div style="margin: 0.5rem;">
            <strong>🛰️ Data Sources</strong><br>
            Sentinel-1A/B, ALOS-2, TerraSAR-X, COSMO-SkyMed
        </div>
        <div style="margin: 0.5rem;">
            <strong>🔬 Analysis Methods</strong><br>
            Polarimetry, Interferometry, AI/ML, Change Detection
        </div>
        <div style="margin: 0.5rem;">
            <strong>🌍 Global Coverage</strong><br>
            24/7 Monitoring, Real-time Processing, Instant Alerts
        </div>
    </div>
    <p style="margin-top: 2rem; font-size: 0.9rem; opacity: 0.8;">
        Built with ❤️ for the global community • Empowering disaster resilience through space technology
    </p>
</div>
""", unsafe_allow_html=True)