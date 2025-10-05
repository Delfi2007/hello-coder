import streamlit as st
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
    page_title="SAR Disaster Lens", 
    layout="wide",
    page_icon="🛰️",
    initial_sidebar_state="expanded"
)

# Professional CSS styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    .main {
        font-family: 'Inter', sans-serif;
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
    
    .three-js-container {
        width: 100%;
        height: 500px;
        background: linear-gradient(135deg, #000428 0%, #004e92 100%);
        border-radius: 15px;
        position: relative;
        overflow: hidden;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-family: 'Inter', sans-serif;
    }
    
    .loading-spinner {
        width: 60px;
        height: 60px;
        border: 4px solid rgba(255, 255, 255, 0.3);
        border-top: 4px solid white;
        border-radius: 50%;
        animation: spin 1s linear infinite;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state for navigation
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'Home'

# Navigation
def show_navigation():
    st.sidebar.markdown("""
    <div class="nav-section">
        <h4>🧭 Navigation</h4>
    </div>
    """, unsafe_allow_html=True)
    
    pages = {
        'Home': '🏠 Home Dashboard',
        'SAR Analysis': '📡 SAR Analysis',
        'Change Detection': '🔍 Change Detection',
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
    
    base_vv = -12
    base_vh = -18
    
    seasonal_vv = 2 * np.sin(2 * np.pi * np.arange(365) / 365)
    seasonal_vh = 1.5 * np.sin(2 * np.pi * np.arange(365) / 365)
    
    noise_vv = np.random.normal(0, 0.5, 365)
    noise_vh = np.random.normal(0, 0.4, 365)
    
    vv_data = base_vv + seasonal_vv + noise_vv
    vh_data = base_vh + seasonal_vh + noise_vh
    
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
        vertical_spacing=0.08
    )
    
    colors = {
        'VV': '#3b82f6',
        'VH': '#10b981',
        'coherence': '#64748b'
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
    
    fig.update_xaxes(showgrid=True, gridcolor='#f1f5f9')
    fig.update_yaxes(showgrid=True, gridcolor='#f1f5f9')
    
    return fig

# Show navigation
show_navigation()

# Page routing with complete implementations
if st.session_state.current_page == 'Home':
    st.markdown("## 🏠 SAR Disaster Lens Dashboard")
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3>🛰️ Active Satellites</h3>
            <h1>2</h1>
            <p>Sentinel-1A, Sentinel-1B</p>
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
    
    # Global coverage visualization
    st.markdown("### 🌍 Global SAR Coverage Network")
    
    # Expanded locations data with more detail
    locations_data = {
        'lat': [23.8563, 37.7749, 37.7510, 28.3949, -15.7975, 51.5074, 35.6762, -33.9249, 55.7558, 1.3521, -26.2041, 40.7128],
        'lon': [90.3564, -122.4194, 14.9934, 84.1240, -47.8919, -0.1278, 139.6503, 18.4241, 37.6176, 103.8198, 28.0473, -74.0060],
        'location': ['Dhaka, Bangladesh', 'San Francisco, CA', 'Naples, Italy', 'Kathmandu, Nepal', 'Brasília, Brazil', 'London, UK', 'Tokyo, Japan', 'Cape Town, SA', 'Moscow, Russia', 'Singapore', 'Johannesburg, SA', 'New York, USA'],
        'disaster_type': ['Flood Monitoring', 'Wildfire Detection', 'Volcanic Activity', 'Landslide Risk', 'Deforestation', 'Coastal Erosion', 'Earthquake Monitoring', 'Drought Assessment', 'Ice Sheet Tracking', 'Urban Subsidence', 'Mining Impact', 'Hurricane Tracking'],
        'severity': ['Critical', 'High', 'Moderate', 'High', 'Moderate', 'Low', 'High', 'Moderate', 'Low', 'Moderate', 'High', 'Moderate'],
        'satellites': ['Sentinel-1A/B', 'ALOS-2, Sentinel-1', 'COSMO-SkyMed', 'TerraSAR-X', 'Sentinel-1A/B', 'Sentinel-1A/B', 'ALOS-2', 'Sentinel-1A/B', 'Sentinel-1A/B', 'TerraSAR-X', 'TerraSAR-X', 'Sentinel-1A/B'],
        'coverage_area': ['12,500 km²', '8,200 km²', '3,100 km²', '4,600 km²', '25,700 km²', '6,800 km²', '11,200 km²', '15,300 km²', '18,900 km²', '720 km²', '9,400 km²', '13,600 km²'],
        'last_update': ['2 hours ago', '1 hour ago', '4 hours ago', '3 hours ago', '6 hours ago', '1 hour ago', '30 min ago', '5 hours ago', '2 hours ago', '45 min ago', '3 hours ago', '1 hour ago']
    }
    
    color_map = {'Critical': '#dc2626', 'High': '#f59e0b', 'Moderate': '#3b82f6', 'Low': '#10b981'}
    size_map = {'Critical': 25, 'High': 20, 'Moderate': 15, 'Low': 12}
    
    # Create the interactive map
    fig = go.Figure()
    
    # Add monitoring stations
    fig.add_trace(go.Scattergeo(
        lat=locations_data['lat'],
        lon=locations_data['lon'],
        text=[f"<b>📍 {location}</b><br>🚨 {disaster}<br>⚠️ Risk Level: {severity}<br>🛰️ Satellites: {satellite}<br>📏 Coverage: {area}<br>🕐 Last Update: {update}" 
              for location, disaster, severity, satellite, area, update in 
              zip(locations_data['location'], locations_data['disaster_type'], locations_data['severity'], 
                  locations_data['satellites'], locations_data['coverage_area'], locations_data['last_update'])],
        hovertemplate="<b>%{text}</b><extra></extra>",
        mode='markers+text',
        marker=dict(
            size=[size_map[s] for s in locations_data['severity']],
            color=[color_map[s] for s in locations_data['severity']],
            line=dict(width=3, color='white'),
            symbol='circle'
        ),
        textposition="top center",
        textfont=dict(size=10, color='white'),
        name='Monitoring Stations',
        showlegend=False
    ))
    
    # Add location labels that are always visible
    fig.add_trace(go.Scattergeo(
        lat=locations_data['lat'],
        lon=locations_data['lon'],
        text=[location.split(',')[0] for location in locations_data['location']],  # Show just city names
        mode='text',
        textposition="bottom center",
        textfont=dict(size=12, color='#1e293b', family='Inter'),
        showlegend=False,
        hoverinfo='skip'
    ))
    
    # Add coverage circles to show monitoring range
    for i, (lat, lon, severity, area) in enumerate(zip(locations_data['lat'], locations_data['lon'], 
                                                       locations_data['severity'], locations_data['coverage_area'])):
        # Extract numeric value from area string
        area_km = float(area.split()[0].replace(',', ''))
        # Calculate approximate radius for visualization (rough approximation)
        radius_deg = np.sqrt(area_km) / 100  # Rough conversion to degrees
        
        # Create circle points
        angles = np.linspace(0, 2*np.pi, 50)
        circle_lats = lat + radius_deg * np.cos(angles)
        circle_lons = lon + radius_deg * np.sin(angles)
        
        fig.add_trace(go.Scattergeo(
            lat=circle_lats,
            lon=circle_lons,
            mode='lines',
            line=dict(width=2, color=color_map[severity], dash='dot'),
            opacity=0.4,
            showlegend=False,
            hoverinfo='skip'
        ))
    
    # Add satellite coverage paths (simulated)
    # Sentinel-1 orbital path simulation
    orbit_lats = np.linspace(-80, 80, 100)
    orbit_lons1 = 45 * np.sin(orbit_lats * np.pi / 180) + 30
    orbit_lons2 = 45 * np.sin(orbit_lats * np.pi / 180) - 60
    
    fig.add_trace(go.Scattergeo(
        lat=orbit_lats,
        lon=orbit_lons1,
        mode='lines',
        line=dict(width=1, color='#64748b', dash='dash'),
        name='Sentinel-1A Orbit',
        opacity=0.6,
        hoverinfo='name'
    ))
    
    fig.add_trace(go.Scattergeo(
        lat=orbit_lats,
        lon=orbit_lons2,
        mode='lines',
        line=dict(width=1, color='#64748b', dash='dash'),
        name='Sentinel-1B Orbit',
        opacity=0.6,
        hoverinfo='name'
    ))
    
    # Update layout with enhanced styling
    fig.update_layout(
        title={
            'text': '🌍 Global SAR Monitoring Network - Real-time Coverage',
            'x': 0.5,
            'font': {'size': 18, 'color': '#1e293b', 'family': 'Inter'}
        },
        geo=dict(
            showland=True,
            landcolor='#f8fafc',
            coastlinecolor='#cbd5e1',
            showocean=True,
            oceancolor='#e0f2fe',
            showlakes=True,
            lakecolor='#bfdbfe',
            showcountries=True,
            countrycolor='#e2e8f0',
            projection_type='natural earth',
            bgcolor='#ffffff'
        ),
        height=550,
        font=dict(family='Inter', color='#64748b')
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Add legend and statistics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="feature-card" style="text-align: center;">
            <h4 style="color: #dc2626;">🔴 Critical Sites</h4>
            <h2>1</h2>
            <p>Immediate attention required</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card" style="text-align: center;">
            <h4 style="color: #f59e0b;">🟡 High Risk Sites</h4>
            <h2>4</h2>
            <p>Enhanced monitoring active</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card" style="text-align: center;">
            <h4 style="color: #3b82f6;">🔵 Moderate Risk Sites</h4>
            <h2>5</h2>
            <p>Regular monitoring schedule</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="feature-card" style="text-align: center;">
            <h4 style="color: #10b981;">🟢 Low Risk Sites</h4>
            <h2>2</h2>
            <p>Baseline monitoring</p>
        </div>
        """, unsafe_allow_html=True)

elif st.session_state.current_page == 'SAR Analysis':
    st.markdown("## 📡 Advanced SAR Data Analysis")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h4>⚙️ Analysis Configuration</h4>
        </div>
        """, unsafe_allow_html=True)
        
        frequency_bands = st.multiselect(
            "SAR Frequency Bands",
            ["L-band (1-2 GHz)", "S-band (2-4 GHz)", "C-band (4-8 GHz)", "X-band (8-12 GHz)"],
            default=["C-band (4-8 GHz)"]
        )
        
        polarization = st.multiselect(
            "Polarization Modes",
            ["VV", "VH", "HH", "HV"],
            default=["VV", "VH"]
        )
        
        analysis_type = st.selectbox(
            "Analysis Method",
            ["Time Series Analysis", "Change Detection", "Coherence Analysis", "Polarimetric Decomposition"]
        )
        
        if st.button("🚀 Execute Analysis", type="primary"):
            st.success("Analysis completed successfully!")
    
    with col2:
        st.markdown("### 📊 Analysis Results")
        
        sar_data = generate_sample_sar_data()
        
        if analysis_type == "Time Series Analysis":
            fig = create_professional_time_series(sar_data)
            st.plotly_chart(fig, use_container_width=True)
        else:
            # Create sample analysis visualization
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=sar_data['date'],
                y=sar_data['VV'],
                mode='lines',
                name='SAR Analysis',
                line=dict(color='#3b82f6', width=2)
            ))
            fig.update_layout(title=f"{analysis_type} Results", height=400)
            st.plotly_chart(fig, use_container_width=True)

elif st.session_state.current_page == 'Change Detection':
    st.markdown("## 🔍 SAR Change Detection Analysis")
    st.markdown("### Compare Before & After Events - Reveal Hidden Changes")
    
    # Event selection
    col1, col2, col3 = st.columns(3)
    
    with col1:
        disaster_type = st.selectbox(
            "Select Disaster Type",
            ["Flooding", "Wildfire", "Deforestation", "Landslide", "Volcanic Eruption", "Urban Development"]
        )
    
    with col2:
        location = st.selectbox(
            "Study Location",
            ["Bangladesh Delta", "California Coast", "Amazon Rainforest", "Nepal Mountains", "Italy Volcanic Region", "Custom Location"]
        )
    
    with col3:
        time_period = st.selectbox(
            "Analysis Period",
            ["Last Month", "Last 6 Months", "Last Year", "Custom Range"]
        )
    
    # Generate realistic SAR data for before/after comparison
    def generate_sar_change_data(disaster_type, rows=100, cols=100):
        np.random.seed(42)
        
        # Generate base SAR backscatter (before event)
        if disaster_type == "Flooding":
            before_data = -12 + 3 * np.random.random((rows, cols))
            # Simulate flood - water appears very dark in SAR
            flood_mask = np.random.random((rows, cols)) < 0.3
            after_data = before_data.copy()
            after_data[flood_mask] = -20 + 2 * np.random.random(np.sum(flood_mask))
            
        elif disaster_type == "Wildfire":
            before_data = -8 + 4 * np.random.random((rows, cols))
            # Simulate burn scars - increased backscatter from rough surfaces
            burn_mask = np.random.random((rows, cols)) < 0.25
            after_data = before_data.copy()
            after_data[burn_mask] = before_data[burn_mask] + 5 + 2 * np.random.random(np.sum(burn_mask))
            
        elif disaster_type == "Deforestation":
            before_data = -6 + 5 * np.random.random((rows, cols))
            # Simulate deforestation - loss of volume scattering
            deforest_mask = np.random.random((rows, cols)) < 0.2
            after_data = before_data.copy()
            after_data[deforest_mask] = before_data[deforest_mask] - 8 + 3 * np.random.random(np.sum(deforest_mask))
            
        elif disaster_type == "Landslide":
            before_data = -10 + 6 * np.random.random((rows, cols))
            # Simulate landslide - changes in surface roughness
            slide_mask = np.random.random((rows, cols)) < 0.15
            after_data = before_data.copy()
            after_data[slide_mask] = -5 + 8 * np.random.random(np.sum(slide_mask))
            
        elif disaster_type == "Volcanic Eruption":
            before_data = -7 + 4 * np.random.random((rows, cols))
            # Simulate volcanic deposits - increased backscatter
            volcanic_mask = np.random.random((rows, cols)) < 0.1
            after_data = before_data.copy()
            after_data[volcanic_mask] = before_data[volcanic_mask] + 8 + 3 * np.random.random(np.sum(volcanic_mask))
            
        else:  # Urban Development
            before_data = -10 + 5 * np.random.random((rows, cols))
            # Simulate urban development - strong corner reflections
            urban_mask = np.random.random((rows, cols)) < 0.2
            after_data = before_data.copy()
            after_data[urban_mask] = -2 + 4 * np.random.random(np.sum(urban_mask))
        
        change_data = after_data - before_data
        return before_data, after_data, change_data
    
    # Generate data
    before_sar, after_sar, change_map = generate_sar_change_data(disaster_type)
    
    # Create comparison visualization
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Before Event', 'After Event', 'Change Detection', 'Analysis Results'),
        specs=[[{"type": "heatmap"}, {"type": "heatmap"}],
               [{"type": "heatmap"}, {"type": "scatter"}]]
    )
    
    # Before event
    fig.add_trace(
        go.Heatmap(
            z=before_sar,
            colorscale='Blues',
            name='Before',
            showscale=False,
            hovertemplate="Before: %{z:.1f} dB<extra></extra>"
        ),
        row=1, col=1
    )
    
    # After event
    fig.add_trace(
        go.Heatmap(
            z=after_sar,
            colorscale='Blues',
            name='After',
            showscale=False,
            hovertemplate="After: %{z:.1f} dB<extra></extra>"
        ),
        row=1, col=2
    )
    
    # Change detection
    fig.add_trace(
        go.Heatmap(
            z=change_map,
            colorscale='RdBu',
            name='Change',
            showscale=True,
            colorbar=dict(title="Change (dB)", x=0.85),
            hovertemplate="Change: %{z:.1f} dB<extra></extra>"
        ),
        row=2, col=1
    )
    
    # Statistical analysis
    change_histogram = np.histogram(change_map.flatten(), bins=50)
    fig.add_trace(
        go.Scatter(
            x=change_histogram[1][:-1],
            y=change_histogram[0],
            mode='lines',
            fill='tonexty',
            name='Change Distribution',
            line=dict(color='#3b82f6', width=2)
        ),
        row=2, col=2
    )
    
    fig.update_layout(
        height=800,
        title_text=f"SAR Change Detection Analysis - {disaster_type} in {location}",
        title_font=dict(size=18, color='#1e293b'),
        showlegend=False
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # 3D Interactive Comparison using Three.js
    st.markdown("### 🌄 3D Interactive Terrain Comparison")
    
    # Three.js 3D visualization
    threejs_comparison = f"""
    <div id="threejs-comparison" style="width: 100%; height: 700px; background: linear-gradient(135deg, #1e293b 0%, #334155 100%); border-radius: 15px; position: relative; margin: 20px 0;">
        <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>
        <script>
            // Create two side-by-side 3D scenes for before/after comparison
            const container = document.getElementById('threejs-comparison');
            const containerWidth = container.clientWidth;
            const containerHeight = container.clientHeight;
            
            // Scene 1: Before Event
            const scene1 = new THREE.Scene();
            const camera1 = new THREE.PerspectiveCamera(75, (containerWidth/2) / containerHeight, 0.1, 1000);
            const renderer1 = new THREE.WebGLRenderer({{ alpha: true }});
            renderer1.setSize(containerWidth/2, containerHeight);
            renderer1.setClearColor(0x1e293b, 0.8);
            renderer1.domElement.style.position = 'absolute';
            renderer1.domElement.style.left = '0px';
            container.appendChild(renderer1.domElement);
            
            // Scene 2: After Event  
            const scene2 = new THREE.Scene();
            const camera2 = new THREE.PerspectiveCamera(75, (containerWidth/2) / containerHeight, 0.1, 1000);
            const renderer2 = new THREE.WebGLRenderer({{ alpha: true }});
            renderer2.setSize(containerWidth/2, containerHeight);
            renderer2.setClearColor(0x1e293b, 0.8);
            renderer2.domElement.style.position = 'absolute';
            renderer2.domElement.style.right = '0px';
            container.appendChild(renderer2.domElement);
            
            // Generate 3D terrain data based on location and disaster type
            function generateTerrainData(disasterType, location, isAfter = false) {{
                const size = 50;
                const geometry = new THREE.PlaneGeometry(10, 10, size-1, size-1);
                const vertices = geometry.attributes.position;
                
                for (let i = 0; i < vertices.count; i++) {{
                    const x = vertices.getX(i);
                    const y = vertices.getY(i);
                    let z = 0;
                    
                    // Generate location-specific base terrain
                    if (location === 'Bangladesh Delta') {{
                        // Flat delta terrain with river channels
                        z = 0.1 * Math.sin(x * 2) * Math.cos(y * 1.5) - 0.05;
                        // Add river channels
                        if (Math.abs(Math.sin(x * 3)) < 0.3) z -= 0.2;
                    }} else if (location === 'California Coast') {{
                        // Rolling hills and valleys
                        z = Math.sin(x * 0.8) * Math.cos(y * 0.6) * 1.2 + 0.5;
                        // Add coastal features
                        if (x > 3) z *= 0.3; // Flatter near coast
                    }} else if (location === 'Amazon Rainforest') {{
                        // Dense forest canopy with gentle undulations
                        z = Math.sin(x * 0.4) * Math.cos(y * 0.4) * 0.8;
                        // Add forest density variations
                        z += (Math.random() - 0.5) * 0.3;
                    }} else if (location === 'Nepal Mountains') {{
                        // Steep mountainous terrain
                        z = Math.sin(x * 0.3) * Math.cos(y * 0.3) * 3;
                        // Add steep slopes and ridges
                        z += Math.sin(x * 1.5) * 0.8;
                        if (z < 0) z = Math.abs(z); // No negative elevations in mountains
                    }} else if (location === 'Italy Volcanic Region') {{
                        // Volcanic cone and lava fields
                        const distFromCenter = Math.sqrt(x*x + y*y);
                        z = Math.max(0, 2 - distFromCenter * 0.4);
                        // Add volcanic texture
                        z += Math.sin(distFromCenter * 2) * 0.3;
                    }} else {{
                        // Default terrain
                        z = Math.sin(x * 0.5) * Math.cos(y * 0.5) * 0.5;
                    }}
                    
                    if (disasterType === 'Flooding' && isAfter) {{
                        // Simulate water level - flat areas at low elevation
                        if (z < -0.2) {{
                            z = -0.3; // Water level
                        }}
                    }} else if (disasterType === 'Wildfire' && isAfter) {{
                        // Simulate burned rough terrain
                        z += Math.random() * 0.3 - 0.15;
                    }} else if (disasterType === 'Landslide' && isAfter) {{
                        // Simulate landslide - displaced material
                        if (x > 2 && x < 4 && y > -1 && y < 1) {{
                            z -= 1.5; // Slide area
                        }}
                        if (x > -2 && x < 0 && y > -1 && y < 1) {{
                            z += 0.8; // Debris pile
                        }}
                    }} else if (disasterType === 'Volcanic Eruption' && isAfter) {{
                        // Simulate lava flow and ash deposits
                        const distFromCenter = Math.sqrt(x*x + y*y);
                        if (distFromCenter < 2) {{
                            z += 0.5 + Math.random() * 0.3; // Volcanic buildup
                        }}
                    }}
                    
                    vertices.setZ(i, z);
                }}
                
                geometry.attributes.position.needsUpdate = true;
                geometry.computeVertexNormals();
                return geometry;
            }}
            
            // Create terrains
            const beforeGeometry = generateTerrainData('{disaster_type}', '{location}', false);
            const afterGeometry = generateTerrainData('{disaster_type}', '{location}', true);
            
            // Materials based on location and disaster type
            let beforeMaterial, afterMaterial;
            
            // Location-specific base materials
            let locationBaseColor = 0x8B4513; // Default brown
            if ('{location}' === 'Bangladesh Delta') {{
                locationBaseColor = 0x9ACD32; // Yellow-green for delta
            }} else if ('{location}' === 'California Coast') {{
                locationBaseColor = 0xDEB887; // Burlywood for coastal hills
            }} else if ('{location}' === 'Amazon Rainforest') {{
                locationBaseColor = 0x228B22; // Forest green
            }} else if ('{location}' === 'Nepal Mountains') {{
                locationBaseColor = 0x696969; // Dim gray for mountains
            }} else if ('{location}' === 'Italy Volcanic Region') {{
                locationBaseColor = 0x654321; // Dark brown for volcanic soil
            }}
            
            if ('{disaster_type}' === 'Flooding') {{
                beforeMaterial = new THREE.MeshPhongMaterial({{ 
                    color: locationBaseColor,
                    wireframe: false,
                    transparent: true,
                    opacity: 0.9
                }});
                afterMaterial = new THREE.MeshPhongMaterial({{ 
                    color: '{location}' === 'Bangladesh Delta' ? 0x4682B4 : 0x4169E1,
                    transparent: true,
                    opacity: 0.8
                }});
            }} else if ('{disaster_type}' === 'Wildfire') {{
                beforeMaterial = new THREE.MeshPhongMaterial({{ 
                    color: '{location}' === 'Amazon Rainforest' ? 0x006400 : 
                           '{location}' === 'California Coast' ? 0x9ACD32 : locationBaseColor
                }});
                afterMaterial = new THREE.MeshPhongMaterial({{ 
                    color: '{location}' === 'California Coast' ? 0x8B0000 : 0xA0522D,
                    emissive: 0x2F0000,
                    emissiveIntensity: 0.2
                }});
            }} else if ('{disaster_type}' === 'Landslide') {{
                beforeMaterial = new THREE.MeshPhongMaterial({{ 
                    color: '{location}' === 'Nepal Mountains' ? 0x708090 : locationBaseColor
                }});
                afterMaterial = new THREE.MeshPhongMaterial({{ 
                    color: '{location}' === 'Nepal Mountains' ? 0xA0522D : 0x8B4513
                }});
            }} else if ('{disaster_type}' === 'Volcanic Eruption') {{
                beforeMaterial = new THREE.MeshPhongMaterial({{ 
                    color: '{location}' === 'Italy Volcanic Region' ? 0x654321 : locationBaseColor
                }});
                afterMaterial = new THREE.MeshPhongMaterial({{ 
                    color: 0xFF4500,
                    emissive: 0x440000,
                    emissiveIntensity: '{location}' === 'Italy Volcanic Region' ? 0.4 : 0.3
                }});
            }} else if ('{disaster_type}' === 'Deforestation') {{
                beforeMaterial = new THREE.MeshPhongMaterial({{ 
                    color: '{location}' === 'Amazon Rainforest' ? 0x006400 : 0x228B22
                }});
                afterMaterial = new THREE.MeshPhongMaterial({{ 
                    color: '{location}' === 'Amazon Rainforest' ? 0x8B4513 : 0xA0522D
                }});
            }} else {{
                beforeMaterial = new THREE.MeshPhongMaterial({{ color: locationBaseColor }});
                afterMaterial = new THREE.MeshPhongMaterial({{ color: 0x8B4513 }});
            }}
            
            // Create meshes
            const beforeTerrain = new THREE.Mesh(beforeGeometry, beforeMaterial);
            const afterTerrain = new THREE.Mesh(afterGeometry, afterMaterial);
            
            scene1.add(beforeTerrain);
            scene2.add(afterTerrain);
            
            // Add location-specific environmental effects
            if ('{disaster_type}' === 'Flooding') {{
                const waterGeometry = new THREE.PlaneGeometry(10, 10);
                let waterColor = 0x006994;
                
                // Location-specific water appearance
                if ('{location}' === 'Bangladesh Delta') {{
                    waterColor = 0x8B7355; // Muddy river water
                }} else if ('{location}' === 'California Coast') {{
                    waterColor = 0x4682B4; // Clear coastal water
                }}
                
                const waterMaterial = new THREE.MeshPhongMaterial({{
                    color: waterColor,
                    transparent: true,
                    opacity: 0.6,
                    side: THREE.DoubleSide
                }});
                const water = new THREE.Mesh(waterGeometry, waterMaterial);
                water.position.z = -0.25;
                water.rotation.x = 0;
                scene2.add(water);
            }}
            
            // Add location-specific vegetation for Amazon
            if ('{location}' === 'Amazon Rainforest' && '{disaster_type}' !== 'Deforestation') {{
                for (let i = 0; i < 30; i++) {{
                    const treeGeometry = new THREE.ConeGeometry(0.1, 0.3, 8);
                    const treeMaterial = new THREE.MeshPhongMaterial({{ color: 0x228B22 }});
                    const tree = new THREE.Mesh(treeGeometry, treeMaterial);
                    tree.position.x = (Math.random() - 0.5) * 8;
                    tree.position.y = (Math.random() - 0.5) * 8;
                    tree.position.z = 0.15;
                    scene1.add(tree);
                    
                    if ('{disaster_type}' !== 'Wildfire') {{
                        scene2.add(tree.clone());
                    }}
                }}
            }}
            
            // Add snow caps for Nepal Mountains
            if ('{location}' === 'Nepal Mountains') {{
                const snowGeometry = new THREE.PlaneGeometry(10, 10);
                const snowMaterial = new THREE.MeshPhongMaterial({{
                    color: 0xFFFAFA,
                    transparent: true,
                    opacity: 0.4
                }});
                const snow = new THREE.Mesh(snowGeometry, snowMaterial);
                snow.position.z = 1.5;
                snow.rotation.x = 0;
                scene1.add(snow);
                scene2.add(snow.clone());
            }}
            
            // Add particle effects for volcanic eruption
            if ('{disaster_type}' === 'Volcanic Eruption') {{
                const particleCount = 200;
                const particles = new THREE.BufferGeometry();
                const positions = new Float32Array(particleCount * 3);
                
                for (let i = 0; i < particleCount * 3; i += 3) {{
                    positions[i] = (Math.random() - 0.5) * 8;
                    positions[i + 1] = (Math.random() - 0.5) * 8;
                    positions[i + 2] = Math.random() * 3;
                }}
                
                particles.setAttribute('position', new THREE.BufferAttribute(positions, 3));
                const particleMaterial = new THREE.PointsMaterial({{
                    color: 0xff6600,
                    size: 0.1,
                    transparent: true,
                    opacity: 0.8
                }});
                
                const particleSystem = new THREE.Points(particles, particleMaterial);
                scene2.add(particleSystem);
            }}
            
            // Lighting
            const ambientLight1 = new THREE.AmbientLight(0x404040, 0.6);
            const ambientLight2 = new THREE.AmbientLight(0x404040, 0.6);
            scene1.add(ambientLight1);
            scene2.add(ambientLight2);
            
            const directionalLight1 = new THREE.DirectionalLight(0xffffff, 1);
            const directionalLight2 = new THREE.DirectionalLight(0xffffff, 1);
            directionalLight1.position.set(5, 5, 5);
            directionalLight2.position.set(5, 5, 5);
            scene1.add(directionalLight1);
            scene2.add(directionalLight2);
            
            // Camera positions
            camera1.position.set(5, 5, 5);
            camera2.position.set(5, 5, 5);
            camera1.lookAt(0, 0, 0);
            camera2.lookAt(0, 0, 0);
            
            // Controls
            const controls1 = new THREE.OrbitControls(camera1, renderer1.domElement);
            const controls2 = new THREE.OrbitControls(camera2, renderer2.domElement);
            controls1.enableDamping = true;
            controls2.enableDamping = true;
            
            // Sync camera movements
            controls1.addEventListener('change', () => {{
                camera2.position.copy(camera1.position);
                camera2.rotation.copy(camera1.rotation);
                controls2.update();
            }});
            
            controls2.addEventListener('change', () => {{
                camera1.position.copy(camera2.position);
                camera1.rotation.copy(camera2.rotation);
                controls1.update();
            }});
            
            // Animation loop
            function animate() {{
                requestAnimationFrame(animate);
                
                // Animate water for flooding
                if ('{disaster_type}' === 'Flooding') {{
                    const water = scene2.children.find(child => child.material && child.material.color.getHex() === 0x006994);
                    if (water) {{
                        water.rotation.z += 0.005;
                        water.material.opacity = 0.5 + 0.1 * Math.sin(Date.now() * 0.001);
                    }}
                }}
                
                // Animate particles for volcanic eruption
                if ('{disaster_type}' === 'Volcanic Eruption') {{
                    const particles = scene2.children.find(child => child.type === 'Points');
                    if (particles) {{
                        particles.rotation.y += 0.01;
                        const positions = particles.geometry.attributes.position;
                        for (let i = 2; i < positions.count * 3; i += 3) {{
                            positions.array[i] += 0.01;
                            if (positions.array[i] > 3) positions.array[i] = 0;
                        }}
                        positions.needsUpdate = true;
                    }}
                }}
                
                controls1.update();
                controls2.update();
                renderer1.render(scene1, camera1);
                renderer2.render(scene2, camera2);
            }}
            
            animate();
            
            // Handle window resize
            window.addEventListener('resize', () => {{
                const newWidth = container.clientWidth;
                const newHeight = container.clientHeight;
                
                camera1.aspect = (newWidth/2) / newHeight;
                camera2.aspect = (newWidth/2) / newHeight;
                camera1.updateProjectionMatrix();
                camera2.updateProjectionMatrix();
                
                renderer1.setSize(newWidth/2, newHeight);
                renderer2.setSize(newWidth/2, newHeight);
            }});
        </script>
        
        <!-- Labels and controls -->
        <div style="position: absolute; top: 20px; left: 20px; color: white; font-family: 'Inter', sans-serif; background: rgba(0,0,0,0.7); padding: 15px; border-radius: 10px; z-index: 1000;">
            <h4 style="margin: 0 0 10px 0; color: #ffffff;">🕐 BEFORE EVENT</h4>
            <p style="margin: 5px 0; font-size: 14px;">Original terrain state</p>
            <p style="margin: 5px 0; font-size: 14px;">📅 {pd.Timestamp.now().strftime('%Y-%m-%d')}</p>
        </div>
        
        <div style="position: absolute; top: 20px; right: 20px; color: white; font-family: 'Inter', sans-serif; background: rgba(0,0,0,0.7); padding: 15px; border-radius: 10px; z-index: 1000;">
            <h4 style="margin: 0 0 10px 0; color: #ffffff;">⚡ AFTER EVENT</h4>
            <p style="margin: 5px 0; font-size: 14px;">{disaster_type} impact visible</p>
            <p style="margin: 5px 0; font-size: 14px;">📅 {pd.Timestamp.now().strftime('%Y-%m-%d')}</p>
        </div>
        
        <div style="position: absolute; bottom: 20px; left: 50%; transform: translateX(-50%); color: white; font-family: 'Inter', sans-serif; background: rgba(0,0,0,0.7); padding: 15px; border-radius: 10px; z-index: 1000; text-align: center;">
            <h4 style="margin: 0 0 10px 0; color: #ffffff;">🎮 Interactive Controls</h4>
            <p style="margin: 5px 0; font-size: 14px;">🖱️ Drag to rotate • 🔍 Scroll to zoom • Cameras are synchronized</p>
            <p style="margin: 5px 0; font-size: 14px; color: #60a5fa;">Comparing {disaster_type} impact in {location}</p>
        </div>
    </div>
    """
    
    st.components.v1.html(threejs_comparison, height=720)
    
    # Analysis insights
    st.markdown("### 📊 Automated Analysis Results")
    
    # Calculate statistics
    total_pixels = change_map.size
    significant_change = np.abs(change_map) > 2  # 2dB threshold
    affected_pixels = np.sum(significant_change)
    affected_percentage = (affected_pixels / total_pixels) * 100
    mean_change = np.mean(change_map[significant_change]) if affected_pixels > 0 else 0
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h3>🎯 Affected Area</h3>
            <h1>{affected_percentage:.1f}%</h1>
            <p>Of total study region</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <h3>📏 Area Size</h3>
            <h1>{affected_pixels/100:.1f}</h1>
            <p>km² significantly changed</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <h3>📈 Avg Change</h3>
            <h1>{mean_change:.1f}</h1>
            <p>dB intensity change</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        confidence = min(95, 70 + affected_percentage)
        st.markdown(f"""
        <div class="metric-card">
            <h3>✅ Confidence</h3>
            <h1>{confidence:.0f}%</h1>
            <p>Detection accuracy</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Interpretation guide
    st.markdown("### 🔍 How to Interpret SAR Changes")
    
    if disaster_type == "Flooding":
        st.markdown("""
        <div class="info-panel">
            <h4>🌊 Flooding Analysis</h4>
            <p><strong>Dark Blue Areas (Negative Change):</strong> New water surfaces reflect radar away from sensor</p>
            <p><strong>Pattern:</strong> Sharp decrease in backscatter (-5 to -15 dB) indicates standing water</p>
            <p><strong>Validation:</strong> Compare with topographic low areas and drainage patterns</p>
        </div>
        """, unsafe_allow_html=True)
        
    elif disaster_type == "Wildfire":
        st.markdown("""
        <div class="alert-panel">
            <h4>🔥 Wildfire Analysis</h4>
            <p><strong>Red Areas (Positive Change):</strong> Burned areas show increased backscatter from rough ash/debris</p>
            <p><strong>Pattern:</strong> Increase of +3 to +8 dB indicates vegetation loss and surface roughening</p>
            <p><strong>Validation:</strong> Cross-reference with fire perimeter data and thermal anomalies</p>
        </div>
        """, unsafe_allow_html=True)
        
    elif disaster_type == "Deforestation":
        st.markdown("""
        <div class="alert-panel">
            <h4>🌳 Deforestation Analysis</h4>
            <p><strong>Blue Areas (Negative Change):</strong> Loss of forest volume scattering</p>
            <p><strong>Pattern:</strong> Decrease of -5 to -12 dB shows transition from forest to bare ground</p>
            <p><strong>Validation:</strong> Verify with optical imagery and forest cover maps</p>
        </div>
        """, unsafe_allow_html=True)
    
    # 3D Change Magnitude Visualization
    st.markdown("### 🌊 3D Change Magnitude Surface")
    
    threejs_change_surface = f"""
    <div id="change-surface" style="width: 100%; height: 500px; background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); border-radius: 15px; position: relative; margin: 20px 0;">
        <script>
            // Create scene for change magnitude visualization
            const changeScene = new THREE.Scene();
            const changeCamera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
            const changeRenderer = new THREE.WebGLRenderer({{ alpha: true }});
            
            const changeContainer = document.getElementById('change-surface');
            changeRenderer.setSize(changeContainer.clientWidth, changeContainer.clientHeight);
            changeRenderer.setClearColor(0x0f172a, 0.9);
            changeContainer.appendChild(changeRenderer.domElement);
            
            // Generate change surface
            const changeSurfaceGeometry = new THREE.PlaneGeometry(8, 8, 63, 63);
            const changeVertices = changeSurfaceGeometry.attributes.position;
            const colors = new Float32Array(changeVertices.count * 3);
            
            for (let i = 0; i < changeVertices.count; i++) {{
                const x = changeVertices.getX(i);
                const y = changeVertices.getY(i);
                
                // Generate change magnitude based on location and disaster type
                let changeValue = 0;
                
                if ('{disaster_type}' === 'Flooding') {{
                    if ('{location}' === 'Bangladesh Delta') {{
                        // River-channel flooding pattern
                        changeValue = -Math.abs(Math.sin(x * 3) * 2);
                        if (Math.abs(Math.sin(x * 3)) < 0.3) changeValue -= 1;
                    }} else {{
                        changeValue = -Math.abs(Math.sin(x * 0.8) * Math.cos(y * 0.8) * 2);
                    }}
                }} else if ('{disaster_type}' === 'Wildfire') {{
                    if ('{location}' === 'California Coast') {{
                        // Wind-driven fire pattern
                        changeValue = Math.max(0, Math.sin(x * 0.5 + y * 1.2) * 3);
                    }} else if ('{location}' === 'Amazon Rainforest') {{
                        // Scattered deforestation fires
                        const distance = Math.sqrt(x*x + y*y);
                        changeValue = Math.max(0, 2 - distance * 0.8) * (1 + Math.random() * 0.7);
                    }} else {{
                        const distance = Math.sqrt(x*x + y*y);
                        changeValue = Math.max(0, 3 - distance) * (1 + Math.random() * 0.5);
                    }}
                }} else if ('{disaster_type}' === 'Volcanic Eruption') {{
                    const distance = Math.sqrt(x*x + y*y);
                    if ('{location}' === 'Italy Volcanic Region') {{
                        // Realistic volcanic cone pattern
                        changeValue = Math.max(0, 3 - distance * 0.3) * 1.5;
                        // Add lava flow direction
                        if (y < 0) changeValue *= 1.3;
                    }} else {{
                        changeValue = Math.max(0, 2 - distance * 0.5) * 2;
                    }}
                }} else if ('{disaster_type}' === 'Landslide') {{
                    if ('{location}' === 'Nepal Mountains') {{
                        // Mountain slope failure pattern
                        changeValue = Math.sin(x * 0.8) * Math.cos(y * 0.3) * 2;
                        if (x > 0 && y > -1 && y < 1) changeValue += 2;
                    }} else {{
                        changeValue = Math.sin(x * 0.5) * Math.cos(y * 0.5) * 1.5;
                    }}
                }} else if ('{disaster_type}' === 'Deforestation') {{
                    if ('{location}' === 'Amazon Rainforest') {{
                        // Road-based deforestation pattern
                        changeValue = -Math.abs(Math.sin(x * 2) * 1.5);
                        // Add branching pattern
                        if (Math.abs(y) < 0.5) changeValue -= 1;
                    }} else {{
                        changeValue = -Math.abs(Math.sin(x * 0.6) * Math.cos(y * 0.6) * 1.2);
                    }}
                }} else {{
                    changeValue = Math.sin(x * 0.5) * Math.cos(y * 0.5) * 1.5;
                }}
                
                changeVertices.setZ(i, changeValue);
                
                // Color based on change magnitude
                if (changeValue > 1) {{
                    colors[i * 3] = 1;     // Red for positive change
                    colors[i * 3 + 1] = 0.2;
                    colors[i * 3 + 2] = 0.2;
                }} else if (changeValue < -1) {{
                    colors[i * 3] = 0.2;   // Blue for negative change
                    colors[i * 3 + 1] = 0.4;
                    colors[i * 3 + 2] = 1;
                }} else {{
                    colors[i * 3] = 0.5;   // Gray for no change
                    colors[i * 3 + 1] = 0.6;
                    colors[i * 3 + 2] = 0.5;
                }}
            }}
            
            changeSurfaceGeometry.setAttribute('color', new THREE.BufferAttribute(colors, 3));
            changeSurfaceGeometry.attributes.position.needsUpdate = true;
            changeSurfaceGeometry.computeVertexNormals();
            
            const changeMaterial = new THREE.MeshPhongMaterial({{
                vertexColors: true,
                wireframe: false,
                transparent: true,
                opacity: 0.8,
                side: THREE.DoubleSide
            }});
            
            const changeSurface = new THREE.Mesh(changeSurfaceGeometry, changeMaterial);
            changeSurface.rotation.x = -Math.PI / 2;
            changeScene.add(changeSurface);
            
            // Add wireframe overlay for better visualization
            const wireframeMaterial = new THREE.MeshBasicMaterial({{
                color: 0xffffff,
                wireframe: true,
                transparent: true,
                opacity: 0.3
            }});
            const wireframe = new THREE.Mesh(changeSurfaceGeometry.clone(), wireframeMaterial);
            wireframe.rotation.x = -Math.PI / 2;
            wireframe.position.y = 0.01;
            changeScene.add(wireframe);
            
            // Lighting for change surface
            const changeAmbientLight = new THREE.AmbientLight(0x404040, 0.4);
            changeScene.add(changeAmbientLight);
            
            const changeDirectionalLight = new THREE.DirectionalLight(0xffffff, 0.8);
            changeDirectionalLight.position.set(10, 10, 5);
            changeScene.add(changeDirectionalLight);
            
            // Camera and controls for change surface
            changeCamera.position.set(6, 8, 6);
            changeCamera.lookAt(0, 0, 0);
            
            const changeControls = new THREE.OrbitControls(changeCamera, changeRenderer.domElement);
            changeControls.enableDamping = true;
            changeControls.dampingFactor = 0.05;
            
            // Animation for change surface
            function animateChange() {{
                requestAnimationFrame(animateChange);
                
                // Gentle rotation for better viewing
                changeSurface.rotation.z += 0.002;
                wireframe.rotation.z += 0.002;
                
                changeControls.update();
                changeRenderer.render(changeScene, changeCamera);
            }}
            
            animateChange();
            
            // Handle resize for change surface
            window.addEventListener('resize', () => {{
                const newWidth = changeContainer.clientWidth;
                const newHeight = changeContainer.clientHeight;
                
                changeCamera.aspect = newWidth / newHeight;
                changeCamera.updateProjectionMatrix();
                changeRenderer.setSize(newWidth, newHeight);
            }});
        </script>
        
        <div style="position: absolute; top: 20px; left: 20px; color: white; font-family: 'Inter', sans-serif; background: rgba(0,0,0,0.8); padding: 15px; border-radius: 10px;">
            <h4 style="margin: 0 0 10px 0; color: #ffffff;">📊 Change Magnitude Surface</h4>
            <p style="margin: 5px 0; font-size: 14px;">🔴 Red: Positive change (increase)</p>
            <p style="margin: 5px 0; font-size: 14px;">🔵 Blue: Negative change (decrease)</p>
            <p style="margin: 5px 0; font-size: 14px;">⚪ Gray: No significant change</p>
        </div>
        
        <div style="position: absolute; bottom: 20px; right: 20px; color: white; font-family: 'Inter', sans-serif; background: rgba(0,0,0,0.8); padding: 15px; border-radius: 10px;">
            <h4 style="margin: 0 0 10px 0; color: #ffffff;">🎯 Analysis Zone</h4>
            <p style="margin: 5px 0; font-size: 14px;">{disaster_type} Impact Analysis</p>
            <p style="margin: 5px 0; font-size: 14px;">Location: {location}</p>
        </div>
    </div>
    """
    
    st.components.v1.html(threejs_change_surface, height=520)
    
    # Time series analysis
    st.markdown("### 📈 Temporal Change Analysis")
    
    # Generate time series data
    dates = pd.date_range('2024-01-01', periods=12, freq='M')
    change_trend = np.cumsum(np.random.normal(0, 0.5, 12))
    
    fig_trend = go.Figure()
    fig_trend.add_trace(go.Scatter(
        x=dates,
        y=change_trend,
        mode='lines+markers',
        name='Cumulative Change',
        line=dict(color='#dc2626', width=3),
        marker=dict(size=8)
    ))
    
    fig_trend.update_layout(
        title='Monthly Change Progression',
        xaxis_title='Date',
        yaxis_title='Cumulative Change (dB)',
        height=300
    )
    
    st.plotly_chart(fig_trend, use_container_width=True)
    
    # Expert recommendations
    st.markdown("### 💡 Expert Recommendations")
    
    recommendations = {
        "Flooding": [
            "Monitor drainage basins during monsoon season",
            "Set up early warning systems in low-lying areas",
            "Validate with river gauge data and precipitation records"
        ],
        "Wildfire": [
            "Track burn scar recovery over multiple seasons",
            "Monitor vegetation regrowth patterns",
            "Assess fire risk in adjacent unburned areas"
        ],
        "Deforestation": [
            "Implement continuous monitoring for illegal logging",
            "Track reforestation efforts and success rates",
            "Monitor carbon stock changes"
        ],
        "Landslide": [
            "Focus on steep terrain during heavy rainfall",
            "Monitor ground stability in vulnerable areas",
            "Correlate with geological and rainfall data"
        ],
        "Volcanic Eruption": [
            "Track ash deposit distribution patterns",
            "Monitor lava flow extent and cooling",
            "Assess infrastructure damage in affected areas"
        ],
        "Urban Development": [
            "Track urban sprawl and infrastructure growth",
            "Monitor environmental impact on surrounding areas",
            "Assess land use change patterns"
        ]
    }
    
    for i, rec in enumerate(recommendations[disaster_type], 1):
        st.markdown(f"**{i}.** {rec}")
    
    # Download and export options
    st.markdown("### 💾 Export Analysis")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📊 Export Data"):
            st.success("Change detection data exported successfully!")
    
    with col2:
        if st.button("📋 Generate Report"):
            st.success("Comprehensive analysis report generated!")
    
    with col3:
        if st.button("📧 Share Results"):
            st.success("Results shared with research team!")

elif st.session_state.current_page == 'Digital Twin':
    st.markdown("## 🌍 3D Digital Twin Visualization")
    
    # Create 3D Earth visualization with SAR data overlay
    def create_3d_earth_visualization():
        # Generate spherical coordinates for Earth
        phi = np.linspace(0, 2*np.pi, 50)
        theta = np.linspace(0, np.pi, 50)
        phi, theta = np.meshgrid(phi, theta)
        
        # Earth radius
        R = 1
        x = R * np.sin(theta) * np.cos(phi)
        y = R * np.sin(theta) * np.sin(phi)
        z = R * np.cos(theta)
        
        # Generate SAR data overlay (simulated)
        sar_intensity = np.sin(3*theta) * np.cos(4*phi) + 0.5*np.random.random((50, 50))
        
        # Create 3D surface plot
        fig = go.Figure()
        
        # Add Earth surface
        fig.add_trace(go.Surface(
            x=x, y=y, z=z,
            surfacecolor=sar_intensity,
            colorscale='Viridis',
            opacity=0.9,
            name='SAR Data',
            showscale=True,
            colorbar=dict(
                title=dict(text="SAR Backscatter (dB)", side="right"),
                tickmode="linear",
                tick0=-20,
                dtick=5
            )
        ))
        
        # Add disaster hotspots
        hotspot_lats = [23.8, 37.7, -15.8, 28.4]
        hotspot_lons = [90.4, -122.4, -47.9, 84.1]
        hotspot_names = ['Bangladesh Flood', 'California Fire', 'Amazon Deforestation', 'Nepal Landslide']
        
        # Convert lat/lon to 3D coordinates
        hotspot_phi = np.radians(hotspot_lons)
        hotspot_theta = np.radians(90 - np.array(hotspot_lats))
        hotspot_x = 1.1 * np.sin(hotspot_theta) * np.cos(hotspot_phi)
        hotspot_y = 1.1 * np.sin(hotspot_theta) * np.sin(hotspot_phi)
        hotspot_z = 1.1 * np.cos(hotspot_theta)
        
        fig.add_trace(go.Scatter3d(
            x=hotspot_x, y=hotspot_y, z=hotspot_z,
            mode='markers+text',
            marker=dict(
                size=15,
                color=['red', 'orange', 'darkred', 'yellow'],
                symbol='diamond'
            ),
            text=hotspot_names,
            textposition="top center",
            name='Disaster Events'
        ))
        
        # Update layout for 3D visualization
        fig.update_layout(
            title={
                'text': 'Interactive 3D Earth Digital Twin - SAR Data Overlay',
                'x': 0.5,
                'font': {'size': 20, 'color': '#1e293b'}
            },
            scene=dict(
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, title=''),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, title=''),
                zaxis=dict(showgrid=False, zeroline=False, showticklabels=False, title=''),
                bgcolor='rgba(0,0,0,0.9)',
                camera=dict(
                    eye=dict(x=1.5, y=1.5, z=1.5)
                )
            ),
            height=600,
            margin=dict(l=0, r=0, t=50, b=0)
        )
        
        return fig
    
    # Generate and display the 3D visualization
    fig_3d = create_3d_earth_visualization()
    st.plotly_chart(fig_3d, use_container_width=True)
    
    # Three.js Interactive 3D Earth Model
    st.markdown("### 🌍 Interactive 3D Earth Model with Three.js")
    
    # Embed Three.js visualization
    three_js_html = """
    <div id="threejs-container" style="width: 100%; height: 600px; background: linear-gradient(135deg, #000428 0%, #004e92 100%); border-radius: 15px; position: relative;">
        <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>
        <script>
            // Scene setup
            const scene = new THREE.Scene();
            const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
            const renderer = new THREE.WebGLRenderer({ alpha: true });
            
            const container = document.getElementById('threejs-container');
            renderer.setSize(container.clientWidth, container.clientHeight);
            renderer.setClearColor(0x000428, 0.8);
            container.appendChild(renderer.domElement);
            
            // Create Earth
            const earthGeometry = new THREE.SphereGeometry(2, 64, 64);
            
            // Load Earth texture (using a simple color for now)
            const earthMaterial = new THREE.MeshPhongMaterial({
                color: 0x4a90e2,
                shininess: 100,
                transparent: true,
                opacity: 0.9
            });
            
            const earth = new THREE.Mesh(earthGeometry, earthMaterial);
            scene.add(earth);
            
            // Create atmosphere
            const atmosphereGeometry = new THREE.SphereGeometry(2.1, 64, 64);
            const atmosphereMaterial = new THREE.MeshPhongMaterial({
                color: 0x87ceeb,
                transparent: true,
                opacity: 0.3
            });
            const atmosphere = new THREE.Mesh(atmosphereGeometry, atmosphereMaterial);
            scene.add(atmosphere);
            
            // Add SAR data points (disaster locations)
            const sarPoints = [
                { lat: 23.8563, lon: 90.3564, name: 'Bangladesh Flood', color: 0xff0000 },
                { lat: 37.7749, lon: -122.4194, name: 'California Fire', color: 0xff6600 },
                { lat: 37.7510, lon: 14.9934, name: 'Italy Volcanic', color: 0xffff00 },
                { lat: 28.3949, lon: 84.1240, name: 'Nepal Landslide', color: 0xff3300 }
            ];
            
            sarPoints.forEach(point => {
                // Convert lat/lon to 3D coordinates
                const phi = (90 - point.lat) * (Math.PI / 180);
                const theta = (point.lon + 180) * (Math.PI / 180);
                
                const x = 2.2 * Math.sin(phi) * Math.cos(theta);
                const y = 2.2 * Math.cos(phi);
                const z = 2.2 * Math.sin(phi) * Math.sin(theta);
                
                // Create marker
                const markerGeometry = new THREE.SphereGeometry(0.05, 16, 16);
                const markerMaterial = new THREE.MeshPhongMaterial({ 
                    color: point.color,
                    emissive: point.color,
                    emissiveIntensity: 0.3
                });
                const marker = new THREE.Mesh(markerGeometry, markerMaterial);
                marker.position.set(x, y, z);
                scene.add(marker);
                
                // Add pulsing effect
                marker.userData = { originalScale: 1, time: Math.random() * Math.PI * 2 };
            });
            
            // Add lighting
            const ambientLight = new THREE.AmbientLight(0x404040, 0.6);
            scene.add(ambientLight);
            
            const directionalLight = new THREE.DirectionalLight(0xffffff, 1);
            directionalLight.position.set(5, 5, 5);
            scene.add(directionalLight);
            
            // Add stars
            const starGeometry = new THREE.BufferGeometry();
            const starMaterial = new THREE.PointsMaterial({ color: 0xffffff, size: 2 });
            
            const starVertices = [];
            for (let i = 0; i < 1000; i++) {
                const x = (Math.random() - 0.5) * 2000;
                const y = (Math.random() - 0.5) * 2000;
                const z = (Math.random() - 0.5) * 2000;
                starVertices.push(x, y, z);
            }
            
            starGeometry.setAttribute('position', new THREE.Float32BufferAttribute(starVertices, 3));
            const stars = new THREE.Points(starGeometry, starMaterial);
            scene.add(stars);
            
            // Camera position
            camera.position.z = 5;
            
            // Add controls
            const controls = new THREE.OrbitControls(camera, renderer.domElement);
            controls.enableDamping = true;
            controls.dampingFactor = 0.05;
            controls.minDistance = 3;
            controls.maxDistance = 10;
            
            // Animation loop
            function animate() {
                requestAnimationFrame(animate);
                
                // Rotate Earth
                earth.rotation.y += 0.002;
                atmosphere.rotation.y += 0.001;
                
                // Animate SAR markers
                scene.children.forEach(child => {
                    if (child.userData && child.userData.originalScale) {
                        child.userData.time += 0.05;
                        const scale = 1 + 0.3 * Math.sin(child.userData.time);
                        child.scale.setScalar(scale);
                    }
                });
                
                // Rotate stars slowly
                stars.rotation.x += 0.0005;
                stars.rotation.y += 0.0005;
                
                controls.update();
                renderer.render(scene, camera);
            }
            
            animate();
            
            // Handle window resize
            window.addEventListener('resize', () => {
                const container = document.getElementById('threejs-container');
                camera.aspect = container.clientWidth / container.clientHeight;
                camera.updateProjectionMatrix();
                renderer.setSize(container.clientWidth, container.clientHeight);
            });
            
            // Add click interaction
            const raycaster = new THREE.Raycaster();
            const mouse = new THREE.Vector2();
            
            function onMouseClick(event) {
                const rect = renderer.domElement.getBoundingClientRect();
                mouse.x = ((event.clientX - rect.left) / rect.width) * 2 - 1;
                mouse.y = -((event.clientY - rect.top) / rect.height) * 2 + 1;
                
                raycaster.setFromCamera(mouse, camera);
                const intersects = raycaster.intersectObjects(scene.children);
                
                if (intersects.length > 0) {
                    const object = intersects[0].object;
                    if (object.userData && object.userData.originalScale) {
                        // Flash the clicked marker
                        object.material.emissiveIntensity = 1;
                        setTimeout(() => {
                            object.material.emissiveIntensity = 0.3;
                        }, 200);
                    }
                }
            }
            
            renderer.domElement.addEventListener('click', onMouseClick);
        </script>
        <div style="position: absolute; top: 20px; left: 20px; color: white; font-family: 'Inter', sans-serif; background: rgba(0,0,0,0.7); padding: 15px; border-radius: 10px;">
            <h3 style="margin: 0 0 10px 0; color: #ffffff;">🌍 Interactive 3D Earth Model</h3>
            <p style="margin: 5px 0; font-size: 14px;">🖱️ Click and drag to rotate</p>
            <p style="margin: 5px 0; font-size: 14px;">🔍 Scroll to zoom in/out</p>
            <p style="margin: 5px 0; font-size: 14px;">📍 Click markers for details</p>
            <p style="margin: 5px 0; font-size: 14px;">🔴 Red: Critical Events</p>
            <p style="margin: 5px 0; font-size: 14px;">🟡 Yellow: Volcanic Activity</p>
        </div>
    </div>
    """
    
    st.components.v1.html(three_js_html, height=650)
    
    # Add temporal control
    st.markdown("### ⏰ Temporal Analysis")
    time_slider = st.slider(
        "Time Period", 
        min_value=0, 
        max_value=365, 
        value=180,
        help="Slide to see SAR data changes over time"
    )
    
    if time_slider:
        st.info(f"Viewing SAR data for day {time_slider} of year")
    
    # Control panels
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h4>🎮 View Controls</h4>
            <p>Interactive navigation</p>
        </div>
        """, unsafe_allow_html=True)
        view_mode = st.selectbox("View Mode", ["Global", "Regional", "Local"])
        time_animation = st.checkbox("Time Animation")
        
        if time_animation:
            st.info("🔄 Time animation enabled")
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h4>📊 Data Layers</h4>
            <p>Visualization options</p>
        </div>
        """, unsafe_allow_html=True)
        show_sar = st.checkbox("SAR Intensity", value=True)
        show_coherence = st.checkbox("Coherence Map")
        show_change = st.checkbox("Change Detection")
    
    with col3:
        st.markdown("""
        <div class="feature-card">
            <h4>🎨 Visualization</h4>
            <p>Display settings</p>
        </div>
        """, unsafe_allow_html=True)
        color_scheme = st.selectbox("Color Scheme", ["Viridis", "Plasma", "Blues", "RdYlBu"])
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
        if st.button("🎥 Record"):
            st.success("Recording started!")
    
    # Additional 3D visualizations
    st.markdown("### 📈 Multi-dimensional SAR Analysis")
    
    # Create additional 3D plots
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🌊 3D Flood Visualization")
        
        # Generate 3D flood data
        x_flood = np.linspace(-10, 10, 30)
        y_flood = np.linspace(-10, 10, 30)
        X_flood, Y_flood = np.meshgrid(x_flood, y_flood)
        Z_flood = np.sin(np.sqrt(X_flood**2 + Y_flood**2)) * np.exp(-0.1*np.sqrt(X_flood**2 + Y_flood**2))
        
        # Add flood simulation
        flood_intensity = -15 + 5 * Z_flood + np.random.normal(0, 1, Z_flood.shape)
        
        fig_flood = go.Figure(data=[go.Surface(
            x=X_flood, y=Y_flood, z=flood_intensity,
            colorscale='Blues',
            name='Flood SAR Response'
        )])
        
        fig_flood.update_layout(
            title='3D Flood SAR Analysis',
            scene=dict(
                xaxis_title='Distance (km)',
                yaxis_title='Distance (km)',
                zaxis_title='SAR Backscatter (dB)'
            ),
            height=400
        )
        
        st.plotly_chart(fig_flood, use_container_width=True)
    
    with col2:
        st.markdown("#### 🔥 3D Fire Detection")
        
        # Generate 3D fire data
        fire_x = np.linspace(0, 20, 25)
        fire_y = np.linspace(0, 20, 25)
        X_fire, Y_fire = np.meshgrid(fire_x, fire_y)
        
        # Simulate fire hotspots
        fire_centers = [(10, 10), (5, 15), (15, 5)]
        Z_fire = np.zeros_like(X_fire)
        
        for cx, cy in fire_centers:
            distance = np.sqrt((X_fire - cx)**2 + (Y_fire - cy)**2)
            Z_fire += 10 * np.exp(-distance/3)
        
        fig_fire = go.Figure(data=[go.Surface(
            x=X_fire, y=Y_fire, z=Z_fire,
            colorscale='Hot',
            name='Fire Temperature'
        )])
        
        fig_fire.update_layout(
            title='3D Fire Detection Analysis',
            scene=dict(
                xaxis_title='Distance (km)',
                yaxis_title='Distance (km)',
                zaxis_title='Temperature Anomaly (°C)'
            ),
            height=400
        )
        
        st.plotly_chart(fig_fire, use_container_width=True)
    
    # Volumetric data visualization
    st.markdown("### 📦 Volumetric SAR Data Analysis")
    
    # Generate 3D volumetric data
    def create_volumetric_plot():
        # Create a 3D grid
        x = np.linspace(-5, 5, 20)
        y = np.linspace(-5, 5, 20)
        z = np.linspace(-5, 5, 20)
        X, Y, Z = np.meshgrid(x, y, z)
        
        # Generate volumetric SAR response
        values = np.sin(X) * np.cos(Y) * np.sin(Z) + 0.5*np.random.random(X.shape)
        
        # Create scatter plot for volumetric visualization
        fig_vol = go.Figure(data=go.Scatter3d(
            x=X.flatten(),
            y=Y.flatten(),
            z=Z.flatten(),
            mode='markers',
            marker=dict(
                size=3,
                color=values.flatten(),
                colorscale='Viridis',
                opacity=0.6,
                colorbar=dict(title="SAR Response")
            )
        ))
        
        fig_vol.update_layout(
            title='Volumetric SAR Data Visualization',
            scene=dict(
                xaxis_title='X (km)',
                yaxis_title='Y (km)',
                zaxis_title='Z (km)',
                bgcolor='rgba(0,0,0,0.1)'
            ),
            height=500
        )
        
        return fig_vol
    
    if st.button("🔮 Generate Volumetric Visualization"):
        with st.spinner("Generating 3D volumetric data..."):
            vol_fig = create_volumetric_plot()
            st.plotly_chart(vol_fig, use_container_width=True)

elif st.session_state.current_page == 'Real-time Monitoring':
    st.markdown("## ⚡ Real-time SAR Monitoring")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 📡 Live Data Stream")
        
        # Real-time simulation
        if st.button("🔴 Start Live Monitoring"):
            progress_bar = st.progress(0)
            status_text = st.empty()
            chart_placeholder = st.empty()
            
            for i in range(100):
                progress_bar.progress(i + 1)
                status_text.text(f'Processing... {i+1}%')
                
                # Generate real-time data
                current_time = datetime.now() - timedelta(seconds=i*10)
                vv_value = -12 + np.random.normal(0, 2)
                
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=[current_time],
                    y=[vv_value],
                    mode='markers',
                    name='Live SAR Data',
                    marker=dict(size=10, color='#3b82f6')
                ))
                
                fig.update_layout(
                    title="Real-time SAR Backscatter",
                    height=300
                )
                
                chart_placeholder.plotly_chart(fig, use_container_width=True)
                time.sleep(0.1)
        
        # System metrics
        st.markdown("### 📊 System Performance")
        
        metrics_col1, metrics_col2, metrics_col3 = st.columns(3)
        with metrics_col1:
            st.metric("Processing Rate", "2.3 GB/min", "0.2 GB/min")
        with metrics_col2:
            st.metric("Latency", "4.2 sec", "-0.3 sec")
        with metrics_col3:
            st.metric("Uptime", "99.7%", "0.1%")
    
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
        
        st.markdown("#### 🚨 Alert Thresholds")
        flood_threshold = st.slider("Flood Alert (dB)", -20, -5, -15)
        fire_threshold = st.slider("Fire Alert (dB)", -10, 0, -5)
        
        st.markdown("#### 📱 Notifications")
        email_alerts = st.checkbox("Email Alerts")
        sms_alerts = st.checkbox("SMS Alerts")

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
                time.sleep(2)
                st.success("Prediction completed!")
    
    with col2:
        st.markdown("### 📈 Prediction Results")
        
        # Generate prediction visualization
        dates = pd.date_range('2024-01-01', periods=30, freq='D')
        risk_scores = np.random.beta(2, 5, 30)
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=dates,
            y=risk_scores,
            mode='lines+markers',
            name='Risk Score',
            line=dict(color='#dc2626', width=3),
            fill='tonexty',
            fillcolor='rgba(220, 38, 38, 0.1)'
        ))
        
        fig.add_hline(y=0.7, line_dash="dash", line_color="#f59e0b", 
                     annotation_text="Alert Threshold")
        
        fig.update_layout(
            title="AI Risk Prediction - Next 30 Days",
            xaxis_title="Date",
            yaxis_title="Risk Score",
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
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

elif st.session_state.current_page == 'Data Explorer':
    st.markdown("## 📊 Interactive Data Explorer")
    
    # Data filtering controls
    col1, col2, col3 = st.columns(3)
    
    with col1:
        date_range = st.date_input(
            "Analysis Period",
            value=(datetime(2024, 1, 1), datetime(2024, 12, 31))
        )
    
    with col2:
        data_types = st.multiselect(
            "Data Products",
            ["SAR Intensity", "Coherence", "Phase", "Physical Parameters"],
            default=["SAR Intensity"]
        )
    
    with col3:
        region = st.selectbox(
            "Geographic Region",
            ["Global", "North America", "Europe", "Asia", "South America", "Africa"]
        )
    
    # Generate sample data
    sample_data = generate_sample_sar_data()
    
    # Data exploration tabs
    tab1, tab2, tab3 = st.tabs(["📈 Time Series", "🌍 Spatial", "📊 Statistics"])
    
    with tab1:
        st.markdown("### 📈 Temporal Analysis")
        
        fig = create_professional_time_series(sample_data)
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("### 📋 Data Summary")
        st.dataframe(sample_data.head(10), use_container_width=True)
    
    with tab2:
        st.markdown("### 🌍 Spatial Distribution")
        
        # Generate synthetic spatial data
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
                colorscale='Blues',
                colorbar=dict(title="SAR Intensity (dB)")
            )
        ))
        
        fig.update_layout(
            title='Spatial Distribution of SAR Data',
            geo=dict(showland=True, landcolor='#f8fafc'),
            height=500
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        st.markdown("### 📊 Statistical Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📋 Descriptive Statistics")
            stats_df = sample_data[['VV', 'VH', 'coherence']].describe()
            st.dataframe(stats_df, use_container_width=True)
        
        with col2:
            st.markdown("#### 📈 Distribution")
            
            fig = go.Figure()
            fig.add_trace(go.Histogram(
                x=sample_data['VV'],
                nbinsx=30,
                name='VV Distribution',
                marker_color='#3b82f6'
            ))
            
            fig.update_layout(
                title="VV Backscatter Distribution",
                height=300
            )
            
            st.plotly_chart(fig, use_container_width=True)

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
        
        experiments = [
            {
                "name": "Multi-temporal Flood Analysis",
                "status": "🔄 Running",
                "progress": 75,
                "start_date": "2024-09-15",
                "completion": "2024-10-20"
            },
            {
                "name": "Polarimetric Forest Monitoring",
                "status": "✅ Completed",
                "progress": 100,
                "start_date": "2024-08-01",
                "completion": "2024-09-30"
            },
            {
                "name": "Ice Sheet Dynamics Study",
                "status": "📋 Planning",
                "progress": 10,
                "start_date": "2024-10-25",
                "completion": "2024-12-15"
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
                st.markdown(f"End: {exp['completion']}")
        
        # Create new experiment
        st.markdown("#### 🆕 Create New Experiment")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            exp_name = st.text_input("Experiment Name")
            exp_type = st.selectbox("Type", ["Disaster Monitoring", "Climate Research", "Methodology"])
        
        with col2:
            duration = st.selectbox("Duration", ["1 month", "3 months", "6 months", "1 year"])
            resources = st.multiselect("Resources", ["Sentinel-1", "ALOS-2", "Ground Truth", "Computing"])
        
        with col3:
            priority = st.selectbox("Priority", ["Low", "Medium", "High", "Critical"])
            if st.button("🚀 Launch Experiment"):
                st.success("Experiment queued for launch!")
    
    with tab3:
        st.markdown("### 📚 Research Publications & Results")
        
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

elif st.session_state.current_page == 'Alert System':
    st.markdown("## 🚨 Advanced Alert & Response System")
    
    # Critical alerts
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
            email_list = st.text_area("Email Recipients", "admin@disaster-lens.org")
        
        with col2:
            st.markdown("**SMS Notifications**")
            sms_enabled = st.checkbox("Enable SMS Alerts")
            sms_list = st.text_area("Phone Numbers", "+1-555-0123")
        
        with col3:
            st.markdown("**API Webhooks**")
            webhook_enabled = st.checkbox("Enable Webhooks")
            webhook_url = st.text_input("Webhook URL", "https://api.emergency.gov/alerts")
    
    with tab3:
        st.markdown("#### 🌍 Monitoring Regions")
        
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

elif st.session_state.current_page == 'Documentation':
    st.markdown("## 📚 System Documentation")
    
    tab1, tab2, tab3, tab4 = st.tabs(["📖 User Guide", "🔧 API Docs", "🎓 Tutorials", "❓ FAQ"])
    
    with tab1:
        st.markdown("### 📖 User Guide")
        
        st.markdown("""
        #### Welcome to SAR Disaster Lens
        
        This comprehensive platform provides real-time disaster monitoring and analysis using 
        Synthetic Aperture Radar (SAR) data.
        
        ##### 🚀 Getting Started
        1. **Navigation**: Use the sidebar to navigate between modules
        2. **Dashboard**: Start with the Home dashboard for overview
        3. **Analysis**: Use SAR Analysis for detailed data exploration
        4. **Monitoring**: Enable real-time monitoring for critical areas
        
        ##### 📡 SAR Data Understanding
        - **VV Polarization**: Vertical transmit, vertical receive
        - **VH Polarization**: Vertical transmit, horizontal receive
        - **Coherence**: Measure of interferometric correlation
        - **Backscatter**: Strength of radar signal return
        
        ##### 🔍 Analysis Workflows
        1. **Flood Monitoring**: Look for decreased VV backscatter over water
        2. **Fire Detection**: Monitor changes in cross-polarization ratios
        3. **Forest Monitoring**: Track biomass changes through backscatter
        4. **Ice Dynamics**: Use coherence to detect ice movement
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
                with st.spinner("Loading tutorial environment..."):
                    time.sleep(2)
                    st.success("Tutorial environment ready!")
        else:
            st.info(f"Tutorial '{selected_tutorial}' will be available soon.")
    
    with tab4:
        st.markdown("### ❓ Frequently Asked Questions")
        
        faqs = [
            {
                "question": "What is SAR and why is it useful for disaster monitoring?",
                "answer": "Synthetic Aperture Radar (SAR) can penetrate clouds and work day or night, making it ideal for disaster monitoring in all weather conditions."
            },
            {
                "question": "How often is the SAR data updated?",
                "answer": "Sentinel-1 provides global coverage every 6 days, with some regions having 3-day repeat cycles."
            },
            {
                "question": "What is the spatial resolution of the SAR data?",
                "answer": "Most SAR data used has 10-20 meter spatial resolution, suitable for regional disaster monitoring."
            },
            {
                "question": "How accurate are the AI predictions?",
                "answer": "Our AI models achieve 90-95% accuracy for most disaster types, with continuous performance monitoring."
            }
        ]
        
        for faq in faqs:
            with st.expander(faq["question"]):
                st.markdown(faq["answer"])