import streamlit as st
import geopandas as gpd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
import time

# Page configuration
st.set_page_config(
    page_title="SAR Disaster Lens - NASA Space Apps 2025", 
    layout="wide",
    page_icon="🛰️",
    initial_sidebar_state="expanded"
)

# Professional CSS styling with sophisticated colors
st.markdown("""
<style>
    /* Import professional fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Main styling */
    .main {
        font-family: 'Inter', sans-serif;
    }
    
    .main-header {
        background: linear-gradient(135deg, #1e293b 0%, #334155 50%, #475569 100%);
        padding: 3rem 2rem;
        border-radius: 16px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
        box-shadow: 0 8px 32px rgba(30, 41, 59, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .main-header h1 {
        font-size: 3.2rem;
        margin-bottom: 0.8rem;
        font-weight: 600;
        letter-spacing: -0.02em;
        color: #f8fafc;
    }
    
    .main-header p {
        font-size: 1.2rem;
        opacity: 0.9;
        margin: 0.5rem 0;
        color: #e2e8f0;
        font-weight: 400;
    }
    
    .nasa-badge {
        background: rgba(255, 255, 255, 0.15);
        padding: 0.75rem 1.5rem;
        border-radius: 30px;
        display: inline-block;
        margin-top: 1.5rem;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        font-weight: 500;
    }
    
    .feature-card {
        background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
        padding: 2rem;
        border-radius: 12px;
        color: #1e293b;
        margin: 1rem 0;
        box-shadow: 0 4px 16px rgba(30, 41, 59, 0.08);
        border: 1px solid #e2e8f0;
        transition: all 0.3s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(30, 41, 59, 0.12);
        border-color: #cbd5e1;
    }
    
    .feature-card h4 {
        color: #334155;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    
    .sar-card {
        background: white;
        padding: 2rem;
        border-radius: 12px;
        box-shadow: 0 2px 12px rgba(30, 41, 59, 0.06);
        border-left: 4px solid #3b82f6;
        margin: 1rem 0;
        border: 1px solid #f1f5f9;
    }
    
    .sar-card h4, .sar-card h5 {
        color: #1e293b;
        font-weight: 600;
    }
    
    .sar-card p {
        color: #64748b;
        margin: 0.5rem 0;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #64748b 0%, #475569 100%);
        padding: 2rem;
        border-radius: 12px;
        text-align: center;
        color: white;
        margin: 0.5rem 0;
        box-shadow: 0 4px 16px rgba(30, 41, 59, 0.15);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .metric-card h1 {
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0.5rem 0;
        color: #f8fafc;
    }
    
    .metric-card h3 {
        font-weight: 600;
        color: #e2e8f0;
        margin-bottom: 0.5rem;
    }
    
    .metric-card p {
        color: #cbd5e1;
        font-size: 0.9rem;
        margin: 0;
    }
    
    .alert-panel {
        background: linear-gradient(135deg, #dc2626 0%, #b91c1c 100%);
        padding: 1.5rem;
        border-radius: 12px;
        color: white;
        margin: 1rem 0;
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 4px 16px rgba(220, 38, 38, 0.2);
    }
    
    .success-panel {
        background: linear-gradient(135deg, #059669 0%, #047857 100%);
        padding: 1.5rem;
        border-radius: 12px;
        color: white;
        margin: 1rem 0;
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 4px 16px rgba(5, 150, 105, 0.2);
    }
    
    .info-panel {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
        padding: 1.5rem;
        border-radius: 12px;
        color: white;
        margin: 1rem 0;
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 4px 16px rgba(59, 130, 246, 0.2);
    }
    
    .hypothesis-panel {
        background: #fefefe;
        padding: 2rem;
        border-radius: 12px;
        border: 2px solid #10b981;
        margin: 1rem 0;
        box-shadow: 0 2px 12px rgba(16, 185, 129, 0.1);
    }
    
    .digital-twin-container {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        padding: 2.5rem;
        border-radius: 16px;
        color: white;
        margin: 2rem 0;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Professional sidebar styling */
    .css-1d391kg {
        background-color: #f8fafc;
    }
    
    .css-1d391kg .stSelectbox > div > div {
        background-color: white;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
    }
    
    /* Professional button styling */
    .stButton > button {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        font-weight: 500;
        font-family: 'Inter', sans-serif;
        transition: all 0.3s ease;
        box-shadow: 0 2px 8px rgba(59, 130, 246, 0.2);
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
    }
    
    /* Professional tabs */
    .stTabs [data-baseweb="tab-list"] {
        background-color: #f8fafc;
        border-radius: 8px;
        padding: 0.25rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: transparent;
        border-radius: 6px;
        color: #64748b;
        font-weight: 500;
        padding: 0.75rem 1.5rem;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: white;
        color: #1e293b;
        box-shadow: 0 2px 4px rgba(30, 41, 59, 0.1);
    }
    
    /* Professional metrics */
    .css-1xarl3l {
        background-color: white;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 1rem;
    }
    
    /* Professional dataframes */
    .dataframe {
        border: 1px solid #e2e8f0;
        border-radius: 8px;
    }
    
    /* Navigation styling */
    .nav-section {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 1rem;
        border: 1px solid #e2e8f0;
    }
    
    .nav-section h4 {
        color: #1e293b;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    
    /* Professional color palette variables */
    :root {
        --primary-blue: #3b82f6;
        --primary-slate: #1e293b;
        --secondary-gray: #64748b;
        --accent-green: #10b981;
        --warning-amber: #f59e0b;
        --danger-red: #dc2626;
        --background-light: #f8fafc;
        --text-primary: #1e293b;
        --text-secondary: #64748b;
        --border-light: #e2e8f0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state for navigation
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'Home'

# Professional Navigation
def show_navigation():
    st.sidebar.markdown("""
    <div class="nav-section">
        <h4>🧭 Navigation</h4>
    </div>
    """, unsafe_allow_html=True)
    
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

# Utility functions with professional styling
def generate_sample_sar_data():
    """Generate realistic SAR data with professional visualization"""
    dates = pd.date_range('2024-01-01', periods=365, freq='D')
    np.random.seed(42)
    
    # More realistic SAR data patterns
    base_vv = -12
    base_vh = -18
    
    # Seasonal variations
    seasonal_vv = 2 * np.sin(2 * np.pi * np.arange(365) / 365)
    seasonal_vh = 1.5 * np.sin(2 * np.pi * np.arange(365) / 365)
    
    # Add noise
    noise_vv = np.random.normal(0, 0.5, 365)
    noise_vh = np.random.normal(0, 0.4, 365)
    
    vv_data = base_vv + seasonal_vv + noise_vv
    vh_data = base_vh + seasonal_vh + noise_vh
    
    # Coherence with realistic patterns
    coherence = 0.6 + 0.3 * np.cos(2 * np.pi * np.arange(365) / 365) + np.random.normal(0, 0.1, 365)
    coherence = np.clip(coherence, 0, 1)
    
    return pd.DataFrame({
        'date': dates,
        'VV': vv_data,
        'VH': vh_data,
        'coherence': coherence,
        'incidence_angle': 35 + 5 * np.sin(2 * np.pi * np.arange(365) / 180) + np.random.normal(0, 1, 365)
    })

def create_professional_time_series(data):
    """Create professional time series plot"""
    fig = make_subplots(
        rows=3, cols=1,
        subplot_titles=('VV Polarization (dB)', 'VH Polarization (dB)', 'Interferometric Coherence'),
        vertical_spacing=0.08,
        specs=[[{"secondary_y": False}], [{"secondary_y": False}], [{"secondary_y": False}]]
    )
    
    # Professional color scheme
    colors = {
        'VV': '#3b82f6',      # Professional blue
        'VH': '#10b981',      # Professional green
        'coherence': '#64748b' # Professional gray
    }
    
    fig.add_trace(
        go.Scatter(
            x=data['date'], 
            y=data['VV'], 
            name='VV Polarization',
            line=dict(color=colors['VV'], width=2),
            fill='tonexty',
            fillcolor='rgba(59, 130, 246, 0.1)'
        ),
        row=1, col=1
    )
    
    fig.add_trace(
        go.Scatter(
            x=data['date'], 
            y=data['VH'], 
            name='VH Polarization',
            line=dict(color=colors['VH'], width=2),
            fill='tonexty',
            fillcolor='rgba(16, 185, 129, 0.1)'
        ),
        row=2, col=1
    )
    
    fig.add_trace(
        go.Scatter(
            x=data['date'], 
            y=data['coherence'], 
            name='Coherence',
            line=dict(color=colors['coherence'], width=2),
            fill='tonexty',
            fillcolor='rgba(100, 116, 139, 0.1)'
        ),
        row=3, col=1
    )
    
    fig.update_layout(
        height=650,
        title_text="SAR Time Series Analysis",
        title_font=dict(size=20, color='#1e293b', family='Inter'),
        showlegend=False,
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(family='Inter', color='#64748b')
    )
    
    # Update axes
    fig.update_xaxes(
        showgrid=True, 
        gridwidth=1, 
        gridcolor='#f1f5f9',
        showline=True,
        linewidth=1,
        linecolor='#e2e8f0'
    )
    fig.update_yaxes(
        showgrid=True, 
        gridwidth=1, 
        gridcolor='#f1f5f9',
        showline=True,
        linewidth=1,
        linecolor='#e2e8f0'
    )
    
    return fig

def create_professional_3d_plot():
    """Create professional 3D surface plot"""
    x = np.linspace(-10, 10, 50)
    y = np.linspace(-10, 10, 50)
    X, Y = np.meshgrid(x, y)
    Z = np.sin(np.sqrt(X**2 + Y**2)) * np.exp(-0.1 * (X**2 + Y**2))
    
    fig = go.Figure(data=[go.Surface(
        z=Z, x=X, y=Y, 
        colorscale='Blues',
        showscale=True,
        colorbar=dict(title="Backscatter (dB)")
    )])
    
    fig.update_layout(
        title='3D SAR Backscatter Surface',
        title_font=dict(size=18, color='#1e293b', family='Inter'),
        scene=dict(
            xaxis_title='Distance (km)',
            yaxis_title='Distance (km)',
            zaxis_title='Backscatter (dB)',
            bgcolor='white'
        ),
        width=700,
        height=500,
        paper_bgcolor='white',
        font=dict(family='Inter', color='#64748b')
    )
    return fig

def create_professional_correlation_matrix():
    """Create professional correlation matrix"""
    params = ['VV Backscatter', 'VH Backscatter', 'Coherence', 'Temperature', 'Precipitation', 'Soil Moisture', 'Vegetation Index']
    
    # Generate realistic correlation data
    np.random.seed(42)
    corr_data = np.random.rand(7, 7)
    corr_data = (corr_data + corr_data.T) / 2
    np.fill_diagonal(corr_data, 1)
    
    # Make some correlations more realistic
    corr_data[0, 1] = 0.75  # VV and VH correlation
    corr_data[1, 0] = 0.75
    corr_data[3, 4] = 0.65  # Temperature and precipitation
    corr_data[4, 3] = 0.65
    
    fig = go.Figure(data=go.Heatmap(
        z=corr_data,
        x=params,
        y=params,
        colorscale='RdBu',
        zmid=0,
        text=np.round(corr_data, 2),
        texttemplate="%{text}",
        textfont={"size": 10, "color": "white"},
        colorbar=dict(title="Correlation Coefficient")
    ))
    
    fig.update_layout(
        title='Parameter Correlation Matrix',
        title_font=dict(size=18, color='#1e293b', family='Inter'),
        width=600,
        height=500,
        paper_bgcolor='white',
        font=dict(family='Inter', color='#64748b')
    )
    return fig

# Professional Header
st.markdown("""
<div class="main-header">
    <h1>🛰️ SAR Disaster Lens</h1>
    <p><strong>Through the Radar Looking Glass: Revealing Earth Processes with SAR</strong></p>
    <p>Advanced Multi-frequency SAR Analysis • Real-time Monitoring • AI-Powered Predictions</p>
    <div class="nasa-badge">
        🚀 NASA Space Apps Challenge 2025 • Earth Science Division
    </div>
</div>
""", unsafe_allow_html=True)

# Show navigation
show_navigation()

# Page routing with professional content
if st.session_state.current_page == 'Home':
    st.markdown("## 🏠 Mission Control Dashboard")
    
    # Professional key metrics
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
            <h3>🌍 Coverage Area</h3>
            <h1>2.4M</h1>
            <p>km² under continuous surveillance</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h3>🚨 Active Alerts</h3>
            <h1>7</h1>
            <p>Critical events being monitored</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card">
            <h3>🎯 Analysis Accuracy</h3>
            <h1>94.2%</h1>
            <p>AI model performance</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Professional alert system
    st.markdown("### 🚨 Current Disaster Monitoring Status")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        alerts_data = {
            'Time': ['2 hours ago', '6 hours ago', '1 day ago', '2 days ago', '3 days ago'],
            'Event Type': ['🌊 Flood Monitoring', '🔥 Wildfire Detection', '🌋 Volcanic Activity', '🏔️ Landslide Risk', '❄️ Ice Dynamics'],
            'Location': ['Ganges Delta, Bangladesh', 'Northern California, USA', 'Mount Etna, Italy', 'Nepal Himalayas', 'Greenland Ice Sheet'],
            'Risk Level': ['Critical', 'High', 'Moderate', 'High', 'Moderate'],
            'Status': ['Active Response', 'Monitoring', 'Resolved', 'Monitoring', 'Routine']
        }
        
        alerts_df = pd.DataFrame(alerts_data)
        st.dataframe(alerts_df, use_container_width=True)
    
    with col2:
        st.markdown("""
        <div class="alert-panel">
            <h4>🚨 Priority Alert</h4>
            <p><strong>Flood Expansion</strong></p>
            <p>Ganges Delta Region</p>
            <p><strong>Affected Area:</strong> 1,247 km²</p>
            <p><strong>Population:</strong> 2.3M at risk</p>
            <p><strong>Response:</strong> Emergency teams deployed</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Professional global coverage visualization
    st.markdown("### 🌍 Global SAR Coverage Network")
    
    locations_data = {
        'lat': [23.8563, 37.7749, 37.7510, 28.3949, -15.7975, 51.5074],
        'lon': [90.3564, -122.4194, 14.9934, 84.1240, -47.8919, -0.1278],
        'location': ['Bangladesh', 'California', 'Italy', 'Nepal', 'Brazil', 'United Kingdom'],
        'disaster_type': ['Flood Monitoring', 'Wildfire Detection', 'Volcanic Activity', 'Landslide Risk', 'Deforestation', 'Coastal Erosion'],
        'severity': ['Critical', 'High', 'Moderate', 'High', 'Moderate', 'Low']
    }
    
    # Professional color mapping
    color_map = {'Critical': '#dc2626', 'High': '#f59e0b', 'Moderate': '#3b82f6', 'Low': '#10b981'}
    
    fig = go.Figure(data=go.Scattergeo(
        lat=locations_data['lat'],
        lon=locations_data['lon'],
        text=[f"<b>{location}</b><br>{disaster}<br>Risk: {severity}" for location, disaster, severity in 
              zip(locations_data['location'], locations_data['disaster_type'], locations_data['severity'])],
        mode='markers',
        marker=dict(
            size=[20 if s == 'Critical' else 15 if s == 'High' else 12 if s == 'Moderate' else 10 
                  for s in locations_data['severity']],
            color=[color_map[s] for s in locations_data['severity']],
            line=dict(width=2, color='white'),
            sizemode='diameter'
        ),
        hovertemplate='%{text}<extra></extra>'
    ))
    
    fig.update_layout(
        title=dict(
            text='Global Disaster Monitoring Network',
            font=dict(size=18, color='#1e293b', family='Inter')
        ),
        geo=dict(
            showland=True,
            landcolor='#f8fafc',
            coastlinecolor='#cbd5e1',
            projection_type='equirectangular',
            showlakes=True,
            lakecolor='#dbeafe'
        ),
        height=450,
        paper_bgcolor='white',
        font=dict(family='Inter', color='#64748b')
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # System health indicators
    st.markdown("### 🖥️ System Health & Performance")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="success-panel">
            <h4>🛰️ Satellite Network</h4>
            <p>✅ Sentinel-1A: Operational</p>
            <p>✅ Sentinel-1B: Operational</p>
            <p>✅ ALOS-2: Operational</p>
            <p>⚠️ TerraSAR-X: Maintenance Mode</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="info-panel">
            <h4>📡 Data Processing</h4>
            <p><strong>Processing Rate:</strong> 2.3 GB/min</p>
            <p><strong>Queue Length:</strong> 12 scenes</p>
            <p><strong>Average Latency:</strong> 4.2 minutes</p>
            <p><strong>Uptime:</strong> 99.7%</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="success-panel">
            <h4>🌐 Network Status</h4>
            <p>✅ Ground Stations: 8/8 Online</p>
            <p>✅ Cloud Services: Active</p>
            <p>✅ API Endpoints: Healthy</p>
            <p>✅ Database: Synchronized</p>
        </div>
        """, unsafe_allow_html=True)

elif st.session_state.current_page == 'SAR Analysis':
    st.markdown("## 📡 Advanced SAR Data Analysis")
    
    # Professional analysis interface
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h4>⚙️ Analysis Configuration</h4>
        </div>
        """, unsafe_allow_html=True)
        
        # SAR parameters
        frequency_bands = st.multiselect(
            "SAR Frequency Bands",
            ["L-band (1-2 GHz)", "S-band (2-4 GHz)", "C-band (4-8 GHz)", "X-band (8-12 GHz)"],
            default=["C-band (4-8 GHz)", "L-band (1-2 GHz)"]
        )
        
        polarization = st.multiselect(
            "Polarization Modes",
            ["VV (Vertical-Vertical)", "VH (Vertical-Horizontal)", "HH (Horizontal-Horizontal)", "HV (Horizontal-Vertical)"],
            default=["VV (Vertical-Vertical)", "VH (Vertical-Horizontal)"]
        )
        
        analysis_type = st.selectbox(
            "Analysis Method",
            ["Time Series Analysis", "Change Detection", "Coherence Analysis", "Polarimetric Decomposition", "InSAR Processing"]
        )
        
        process_type = st.selectbox(
            "Earth Process Focus",
            ["Flood Monitoring", "Wildfire Detection", "Deforestation Analysis", "Ice Sheet Dynamics", "Volcanic Activity", "Urban Development"]
        )
        
        temporal_window = st.slider("Temporal Analysis Window (days)", 1, 365, 30)
        
        if st.button("🚀 Execute Analysis", type="primary"):
            with st.spinner("Processing SAR data..."):
                time.sleep(2)
                st.success("Analysis completed successfully!")
    
    with col2:
        st.markdown("### 📊 Analysis Results")
        
        # Generate professional SAR analysis
        sar_data = generate_sample_sar_data()
        
        if analysis_type == "Time Series Analysis":
            fig = create_professional_time_series(sar_data)
            st.plotly_chart(fig, use_container_width=True)
            
        elif analysis_type == "Change Detection":
            # Professional change detection visualization
            fig = go.Figure()
            
            # Pre-event baseline
            baseline_data = sar_data['VV'][:100]
            event_data = sar_data['VV'][100:200] - 4  # Simulate significant change
            post_event_data = sar_data['VV'][200:] - 2  # Partial recovery
            
            fig.add_trace(go.Scatter(
                x=sar_data['date'][:100],
                y=baseline_data,
                name='Pre-Event Baseline',
                line=dict(color='#10b981', width=2),
                fill='tonexty',
                fillcolor='rgba(16, 185, 129, 0.1)'
            ))
            
            fig.add_trace(go.Scatter(
                x=sar_data['date'][100:200],
                y=event_data,
                name='Event Period',
                line=dict(color='#dc2626', width=2),
                fill='tonexty',
                fillcolor='rgba(220, 38, 38, 0.1)'
            ))
            
            fig.add_trace(go.Scatter(
                x=sar_data['date'][200:],
                y=post_event_data,
                name='Post-Event Recovery',
                line=dict(color='#f59e0b', width=2),
                fill='tonexty',
                fillcolor='rgba(245, 158, 11, 0.1)'
            ))
            
            fig.update_layout(
                title="Change Detection Analysis",
                title_font=dict(size=18, color='#1e293b', family='Inter'),
                xaxis_title="Date",
                yaxis_title="Backscatter Coefficient (dB)",
                height=450,
                plot_bgcolor='white',
                paper_bgcolor='white',
                font=dict(family='Inter', color='#64748b')
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
        elif analysis_type == "Polarimetric Decomposition":
            fig = create_professional_3d_plot()
            st.plotly_chart(fig, use_container_width=True)
            
        else:  # Default to coherence analysis
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=sar_data['date'],
                y=sar_data['coherence'],
                mode='lines+markers',
                name='Interferometric Coherence',
                line=dict(color='#3b82f6', width=2),
                marker=dict(size=4, color='#3b82f6'),
                fill='tonexty',
                fillcolor='rgba(59, 130, 246, 0.1)'
            ))
            
            # Add coherence threshold line
            fig.add_hline(
                y=0.5, 
                line_dash="dash", 
                line_color="#64748b", 
                annotation_text="Coherence Threshold (0.5)"
            )
            
            fig.update_layout(
                title="Interferometric Coherence Analysis",
                title_font=dict(size=18, color='#1e293b', family='Inter'),
                xaxis_title="Date",
                yaxis_title="Coherence",
                height=450,
                plot_bgcolor='white',
                paper_bgcolor='white',
                font=dict(family='Inter', color='#64748b')
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    # Professional parameter estimation results
    st.markdown("### 🔬 Derived Physical Parameters")
    
    col1, col2, col3, col4 = st.columns(4)
    
    parameters = [
        ("Soil Moisture", "34.2%", "↑ 2.1%", "#10b981"),
        ("Surface Roughness", "3.4 cm", "→ 0.0 cm", "#3b82f6"),
        ("Vegetation Density", "0.67 NDVI", "↓ 0.03", "#f59e0b"),
        ("Dielectric Constant", "12.4", "↑ 0.8", "#64748b")
    ]
    
    for i, (param, value, change, color) in enumerate(parameters):
        with [col1, col2, col3, col4][i]:
            st.metric(param, value, change)

elif st.session_state.current_page == 'Data Explorer':
    st.markdown("## 📊 Interactive Data Explorer")
    
    # Professional data filtering interface
    with st.container():
        col1, col2, col3 = st.columns(3)
        
        with col1:
            date_range = st.date_input(
                "Analysis Period",
                value=(datetime(2024, 1, 1), datetime(2024, 12, 31)),
                min_value=datetime(2020, 1, 1),
                max_value=datetime(2025, 12, 31)
            )
        
        with col2:
            data_types = st.multiselect(
                "Data Products",
                ["SAR Intensity", "Coherence", "Phase", "Physical Parameters"],
                default=["SAR Intensity", "Coherence"]
            )
        
        with col3:
            region = st.selectbox(
                "Geographic Region",
                ["Global Coverage", "North America", "Europe", "Asia-Pacific", "South America", "Africa", "Arctic"]
            )
    
    # Generate professional sample data
    sample_data = generate_sample_sar_data()
    
    # Professional data exploration tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📈 Time Series", "🌍 Spatial Analysis", "📊 Statistical Summary", "🔍 Correlation Analysis"])
    
    with tab1:
        st.markdown("### 📈 Temporal Analysis")
        
        fig = create_professional_time_series(sample_data)
        st.plotly_chart(fig, use_container_width=True)
        
        # Data summary table
        st.markdown("### 📋 Data Summary")
        st.dataframe(sample_data.head(10), use_container_width=True)
    
    with tab2:
        st.markdown("### 🌍 Spatial Distribution Analysis")
        
        # Generate synthetic spatial data
        lat = np.random.uniform(20, 60, 200)
        lon = np.random.uniform(-120, 40, 200)
        intensity = np.random.normal(-12, 3, 200)
        
        fig = go.Figure(data=go.Scattergeo(
            lat=lat,
            lon=lon,
            mode='markers',
            marker=dict(
                size=8,
                color=intensity,
                colorscale='Blues',
                colorbar=dict(title="SAR Intensity (dB)"),
                line=dict(width=1, color='white')
            ),
            text=[f"Intensity: {i:.1f} dB<br>Lat: {la:.2f}°<br>Lon: {lo:.2f}°" 
                  for i, la, lo in zip(intensity, lat, lon)],
            hovertemplate='%{text}<extra></extra>'
        ))
        
        fig.update_layout(
            title=dict(
                text='Spatial Distribution of SAR Measurements',
                font=dict(size=18, color='#1e293b', family='Inter')
            ),
            geo=dict(
                showland=True,
                landcolor='#f8fafc',
                coastlinecolor='#cbd5e1',
                projection_type='natural earth'
            ),
            height=500,
            paper_bgcolor='white',
            font=dict(family='Inter', color='#64748b')
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        st.markdown("### 📊 Statistical Analysis")
        
        # Professional statistical summary
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📋 Descriptive Statistics")
            stats_df = sample_data[['VV', 'VH', 'coherence']].describe()
            st.dataframe(stats_df, use_container_width=True)
        
        with col2:
            st.markdown("#### 📈 Distribution Analysis")
            
            # Distribution plots
            fig = make_subplots(
                rows=2, cols=1,
                subplot_titles=('VV Backscatter Distribution', 'Coherence Distribution')
            )
            
            fig.add_trace(
                go.Histogram(x=sample_data['VV'], nbinsx=30, name='VV', marker_color='#3b82f6'),
                row=1, col=1
            )
            
            fig.add_trace(
                go.Histogram(x=sample_data['coherence'], nbinsx=30, name='Coherence', marker_color='#10b981'),
                row=2, col=1
            )
            
            fig.update_layout(
                height=500,
                showlegend=False,
                plot_bgcolor='white',
                paper_bgcolor='white',
                font=dict(family='Inter', color='#64748b')
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    with tab4:
        st.markdown("### 🔍 Correlation Analysis")
        
        fig = create_professional_correlation_matrix()
        st.plotly_chart(fig, use_container_width=True)
        
        # Scatter plot relationships
        col1, col2 = st.columns(2)
        
        with col1:
            fig = go.Figure(data=go.Scatter(
                x=sample_data['VV'],
                y=sample_data['VH'],
                mode='markers',
                marker=dict(
                    color=sample_data['coherence'], 
                    colorscale='Blues',
                    size=6,
                    opacity=0.7,
                    colorbar=dict(title="Coherence")
                ),
                text=[f"VV: {vv:.1f} dB<br>VH: {vh:.1f} dB<br>Coherence: {coh:.2f}" 
                      for vv, vh, coh in zip(sample_data['VV'], sample_data['VH'], sample_data['coherence'])],
                hovertemplate='%{text}<extra></extra>'
            ))
            
            fig.update_layout(
                title="VV vs VH Backscatter Relationship",
                title_font=dict(size=16, color='#1e293b', family='Inter'),
                xaxis_title="VV Backscatter (dB)",
                yaxis_title="VH Backscatter (dB)",
                height=400,
                plot_bgcolor='white',
                paper_bgcolor='white',
                font=dict(family='Inter', color='#64748b')
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = go.Figure(data=go.Scatter(
                x=sample_data['coherence'],
                y=sample_data['VV'],
                mode='markers',
                marker=dict(color='#64748b', size=6, opacity=0.7),
                text=[f"Coherence: {coh:.2f}<br>VV: {vv:.1f} dB" 
                      for coh, vv in zip(sample_data['coherence'], sample_data['VV'])],
                hovertemplate='%{text}<extra></extra>'
            ))
            
            fig.update_layout(
                title="Coherence vs VV Backscatter",
                title_font=dict(size=16, color='#1e293b', family='Inter'),
                xaxis_title="Interferometric Coherence",
                yaxis_title="VV Backscatter (dB)",  
                height=400,
                plot_bgcolor='white',
                paper_bgcolor='white',
                font=dict(family='Inter', color='#64748b')
            )
            
            st.plotly_chart(fig, use_container_width=True)

# Continue with other pages...
else:
    st.markdown(f"## {st.session_state.current_page}")
    st.markdown("""
    <div class="feature-card">
        <h4>🚧 Page Under Development</h4>
        <p>This page is currently being developed with professional styling and advanced features.</p>
        <p>Please check back soon for the complete implementation.</p>
    </div>
    """, unsafe_allow_html=True)

# Clean minimal footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 1rem; color: #64748b; margin-top: 1rem;">
    <p style="font-size: 0.85rem; margin: 0;">
        SAR Disaster Lens © 2025 • NASA Space Apps Challenge
    </p>
</div>
""")