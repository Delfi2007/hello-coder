# SAR Analysis Utilities for NASA Space Apps Challenge
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import json

class SARAnalyzer:
    """Advanced SAR data analysis for Earth process monitoring"""
    
    def __init__(self):
        self.frequency_bands = {
            'L': {'freq_range': (1, 2), 'wavelength': 0.15, 'penetration': 'high'},
            'S': {'freq_range': (2, 4), 'wavelength': 0.075, 'penetration': 'medium'},
            'C': {'freq_range': (4, 8), 'wavelength': 0.0375, 'penetration': 'low'},
            'X': {'freq_range': (8, 12), 'wavelength': 0.025, 'penetration': 'very_low'}
        }
        
    def simulate_sar_response(self, process_type, days=365):
        """Simulate SAR backscatter response for different Earth processes"""
        dates = pd.date_range('2024-01-01', periods=days, freq='D')
        
        if process_type == 'flood':
            return self._simulate_flood_response(dates)
        elif process_type == 'fire':
            return self._simulate_fire_response(dates)
        elif process_type == 'forest':
            return self._simulate_forest_response(dates)
        elif process_type == 'ice':
            return self._simulate_ice_response(dates)
        elif process_type == 'volcano':
            return self._simulate_volcano_response(dates)
        else:
            return self._simulate_generic_response(dates)
    
    def _simulate_flood_response(self, dates):
        """Simulate SAR response to flooding events"""
        # Base backscatter for dry land
        base_vv = -12  # dB
        base_vh = -18  # dB
        
        # Seasonal variation
        seasonal = 2 * np.sin(2 * np.pi * np.arange(len(dates)) / 365)
        
        # Flood events (water surfaces have low backscatter)
        flood_events = np.zeros(len(dates))
        
        # Major flood event
        flood_start = 100
        flood_duration = 30
        flood_events[flood_start:flood_start+flood_duration] = -8 * np.exp(-0.1 * np.arange(flood_duration))
        
        # Minor flood event
        flood_start2 = 250
        flood_duration2 = 15
        flood_events[flood_start2:flood_start2+flood_duration2] = -5 * np.exp(-0.2 * np.arange(flood_duration2))
        
        # Add noise
        noise = np.random.normal(0, 0.5, len(dates))
        
        vv_response = base_vv + seasonal + flood_events + noise
        vh_response = base_vh + seasonal * 0.7 + flood_events * 1.2 + noise
        
        return {
            'dates': dates,
            'VV': vv_response,
            'VH': vh_response,
            'coherence': np.random.uniform(0.3, 0.8, len(dates)),
            'process_events': [(dates[flood_start], 'Major Flood'), (dates[flood_start2], 'Minor Flood')]
        }
    
    def _simulate_fire_response(self, dates):
        """Simulate SAR response to wildfire and recovery"""
        base_vv = -8  # Forest backscatter
        base_vh = -15
        
        # Pre-fire conditions
        pre_fire_days = 120
        fire_day = pre_fire_days
        
        # Fire impact (immediate decrease due to vegetation loss)
        fire_impact_vv = np.concatenate([
            np.full(pre_fire_days, base_vv),
            np.linspace(base_vv, base_vv - 8, 10),  # Fire event
            base_vv - 8 + 6 * (1 - np.exp(-0.005 * np.arange(len(dates) - pre_fire_days - 10)))  # Recovery
        ])
        
        fire_impact_vh = np.concatenate([
            np.full(pre_fire_days, base_vh),
            np.linspace(base_vh, base_vh - 10, 10),
            base_vh - 10 + 8 * (1 - np.exp(-0.005 * np.arange(len(dates) - pre_fire_days - 10)))
        ])
        
        # Add seasonal variation and noise
        seasonal = np.sin(2 * np.pi * np.arange(len(dates)) / 365)
        noise = np.random.normal(0, 0.3, len(dates))
        
        return {
            'dates': dates,
            'VV': fire_impact_vv + seasonal + noise,
            'VH': fire_impact_vh + seasonal * 0.8 + noise,
            'coherence': np.concatenate([
                np.random.uniform(0.6, 0.8, fire_day),
                np.random.uniform(0.2, 0.4, len(dates) - fire_day)  # Low coherence after fire
            ]),
            'process_events': [(dates[fire_day], 'Wildfire Start')]
        }
    
    def _simulate_forest_response(self, dates):
        """Simulate SAR response to deforestation"""
        base_vv = -8
        base_vh = -15
        
        # Gradual deforestation
        deforestation_rate = 0.01  # per day
        deforestation_start = 150
        
        vv_response = np.full(len(dates), base_vv)
        vh_response = np.full(len(dates), base_vh)
        
        # Apply deforestation effect
        for i in range(deforestation_start, len(dates)):
            days_since_start = i - deforestation_start
            forest_loss = min(1.0, days_since_start * deforestation_rate)
            
            # Less vegetation = higher backscatter
            vv_response[i] = base_vv + forest_loss * 4
            vh_response[i] = base_vh + forest_loss * 6
        
        # Add seasonal variation
        seasonal = 2 * np.sin(2 * np.pi * np.arange(len(dates)) / 365)
        noise = np.random.normal(0, 0.4, len(dates))
        
        return {
            'dates': dates,
            'VV': vv_response + seasonal + noise,
            'VH': vh_response + seasonal * 0.9 + noise,
            'coherence': np.random.uniform(0.5, 0.7, len(dates)),
            'process_events': [(dates[deforestation_start], 'Deforestation Begins')]
        }
    
    def _simulate_ice_response(self, dates):
        """Simulate SAR response to ice dynamics"""
        base_vv = -6  # Ice backscatter
        base_vh = -12
        
        # Seasonal ice variations
        seasonal_vv = 4 * np.cos(2 * np.pi * np.arange(len(dates)) / 365)  # Winter high, summer low
        seasonal_vh = 3 * np.cos(2 * np.pi * np.arange(len(dates)) / 365)
        
        # Ice break-up events
        breakup_events = np.zeros(len(dates))
        breakup_days = [120, 290]  # Spring and fall
        
        for breakup_day in breakup_days:
            if breakup_day < len(dates):
                breakup_events[breakup_day:breakup_day+7] = -3 * np.exp(-0.3 * np.arange(7))
        
        noise = np.random.normal(0, 0.6, len(dates))
        
        return {
            'dates': dates,
            'VV': base_vv + seasonal_vv + breakup_events + noise,
            'VH': base_vh + seasonal_vh + breakup_events * 0.8 + noise,
            'coherence': 0.8 + 0.2 * np.cos(2 * np.pi * np.arange(len(dates)) / 365),
            'process_events': [(dates[day], 'Ice Break-up') for day in breakup_days if day < len(dates)]
        }
    
    def _simulate_volcano_response(self, dates):
        """Simulate SAR response to volcanic activity"""
        base_vv = -10
        base_vh = -16
        
        # Volcanic eruption
        eruption_day = 200
        pre_eruption_activity = np.zeros(len(dates))
        
        # Pre-eruption ground deformation
        if eruption_day > 30:
            pre_eruption_activity[eruption_day-30:eruption_day] = np.linspace(0, 2, 30)
        
        # Eruption impact
        eruption_impact = np.zeros(len(dates))
        if eruption_day < len(dates):
            eruption_impact[eruption_day:eruption_day+14] = 8 * np.exp(-0.2 * np.arange(14))
        
        # Post-eruption changes
        post_eruption = np.zeros(len(dates))
        if eruption_day + 14 < len(dates):
            post_days = len(dates) - eruption_day - 14
            post_eruption[eruption_day+14:] = 3 * np.exp(-0.01 * np.arange(post_days))
        
        noise = np.random.normal(0, 0.5, len(dates))
        
        return {
            'dates': dates,
            'VV': base_vv + pre_eruption_activity + eruption_impact + post_eruption + noise,
            'VH': base_vh + pre_eruption_activity * 0.7 + eruption_impact * 1.2 + post_eruption * 0.8 + noise,
            'coherence': np.maximum(0.1, 0.7 - eruption_impact * 0.1),
            'process_events': [(dates[eruption_day], 'Volcanic Eruption')]
        }
    
    def _simulate_generic_response(self, dates):
        """Generic SAR response simulation"""
        base_vv = -10
        base_vh = -16
        
        seasonal = 2 * np.sin(2 * np.pi * np.arange(len(dates)) / 365)
        trend = 0.001 * np.arange(len(dates))  # Small trend
        noise = np.random.normal(0, 0.5, len(dates))
        
        return {
            'dates': dates,
            'VV': base_vv + seasonal + trend + noise,
            'VH': base_vh + seasonal * 0.8 + trend * 0.6 + noise,
            'coherence': np.random.uniform(0.4, 0.8, len(dates)),
            'process_events': []
        }
    
    def calculate_polarimetric_parameters(self, vv, vh, hh=None, hv=None):
        """Calculate polarimetric decomposition parameters"""
        # Convert to linear units if in dB
        if np.mean(vv) < 0:  # Likely in dB
            vv_lin = 10 ** (vv / 10)
            vh_lin = 10 ** (vh / 10)
        else:
            vv_lin = vv
            vh_lin = vh
        
        # Calculate common polarimetric ratios
        vh_vv_ratio = vh_lin / vv_lin
        copolar_ratio = vv_lin / (hh if hh is not None else vv_lin)
        
        # Simulated entropy and alpha parameters
        entropy = np.random.uniform(0.3, 0.9, len(vv))
        alpha = np.random.uniform(15, 60, len(vv))  # degrees
        
        return {
            'VH_VV_ratio': vh_vv_ratio,
            'copolar_ratio': copolar_ratio,
            'entropy': entropy,
            'alpha_angle': alpha
        }
    
    def physical_parameter_estimation(self, sar_data, process_type):
        """Estimate physical parameters from SAR data"""
        vv = sar_data['VV']
        vh = sar_data['VH']
        
        if process_type == 'flood':
            # Estimate water extent and depth
            water_threshold = -15  # dB
            water_mask = vv < water_threshold
            water_extent = np.sum(water_mask) / len(water_mask) * 100  # percentage
            
            # Estimate soil moisture for non-water areas
            soil_moisture = np.clip((-vv + 10) / 20, 0, 1)  # Normalized
            
            return {
                'water_extent_percent': water_extent,
                'avg_soil_moisture': np.mean(soil_moisture[~water_mask]) if not np.all(water_mask) else 0,
                'flood_duration_days': np.sum(water_mask) / len(water_mask) * 365
            }
        
        elif process_type == 'fire':
            # Estimate burn severity and recovery
            pre_fire_baseline = np.mean(vv[:50])  # First 50 days
            burn_severity = pre_fire_baseline - np.min(vv)
            
            # Recovery rate (simplified)
            post_fire_idx = np.argmin(vv)
            if post_fire_idx < len(vv) - 50:
                recovery_data = vv[post_fire_idx:post_fire_idx+50]
                recovery_rate = (recovery_data[-1] - recovery_data[0]) / 50
            else:
                recovery_rate = 0
            
            return {
                'burn_severity_db': burn_severity,
                'recovery_rate_db_per_day': recovery_rate,
                'time_to_min_backscatter_days': post_fire_idx
            }
        
        elif process_type == 'forest':
            # Estimate biomass and deforestation rate
            biomass_proxy = (vv + 20) / 15  # Normalized biomass proxy
            
            # Calculate deforestation trend
            from scipy import stats
            slope, intercept, r_value, p_value, std_err = stats.linregress(range(len(vv)), vv)
            
            return {
                'avg_biomass_proxy': np.mean(biomass_proxy),
                'deforestation_trend_db_per_day': slope,
                'trend_significance_p': p_value,
                'trend_r_squared': r_value**2
            }
        
        else:
            # Generic physical parameters
            return {
                'avg_backscatter_vv_db': np.mean(vv),
                'avg_backscatter_vh_db': np.mean(vh),
                'backscatter_std_vv': np.std(vv),
                'temporal_stability': 1 / (1 + np.std(vv))
            }

class HypothesisFramework:
    """Framework for developing and testing scientific hypotheses"""
    
    def __init__(self):
        self.hypotheses = []
        self.test_results = []
    
    def create_hypothesis(self, title, description, variables, expected_outcome):
        """Create a new hypothesis"""
        hypothesis = {
            'id': len(self.hypotheses),
            'title': title,
            'description': description,
            'variables': variables,
            'expected_outcome': expected_outcome,
            'created_date': datetime.now(),
            'status': 'created'
        }
        self.hypotheses.append(hypothesis)
        return hypothesis['id']
    
    def test_hypothesis(self, hypothesis_id, test_data, confidence_level=0.95):
        """Test a hypothesis using statistical methods"""
        if hypothesis_id >= len(self.hypotheses):
            return None
        
        hypothesis = self.hypotheses[hypothesis_id]
        
        # Simulate statistical testing
        from scipy import stats
        
        # Generate synthetic test results
        np.random.seed(hypothesis_id)  # For reproducible results
        
        # Simulate correlation test
        correlation = np.random.uniform(-0.8, 0.8)
        n_samples = len(test_data.get('VV', [100] * 100))
        
        # Calculate p-value based on correlation and sample size
        t_stat = correlation * np.sqrt((n_samples - 2) / (1 - correlation**2))
        p_value = 2 * (1 - stats.t.cdf(abs(t_stat), n_samples - 2))
        
        # Determine if hypothesis is supported
        alpha = 1 - confidence_level
        is_significant = p_value < alpha
        
        result = {
            'hypothesis_id': hypothesis_id,
            'correlation': correlation,
            'p_value': p_value,
            'is_significant': is_significant,
            'confidence_level': confidence_level,
            'test_date': datetime.now(),
            'status': 'supported' if is_significant else 'rejected'
        }
        
        self.test_results.append(result)
        self.hypotheses[hypothesis_id]['status'] = result['status']
        
        return result
    
    def get_hypothesis_summary(self):
        """Get summary of all hypotheses and their test results"""
        summary = {
            'total_hypotheses': len(self.hypotheses),
            'supported': len([h for h in self.hypotheses if h['status'] == 'supported']),
            'rejected': len([h for h in self.hypotheses if h['status'] == 'rejected']),
            'pending': len([h for h in self.hypotheses if h['status'] == 'created'])
        }
        return summary

# Usage example functions
def generate_sample_data():
    """Generate sample SAR data for demonstration"""
    analyzer = SARAnalyzer()
    
    # Generate data for different processes
    flood_data = analyzer.simulate_sar_response('flood')
    fire_data = analyzer.simulate_sar_response('fire') 
    forest_data = analyzer.simulate_sar_response('forest')
    
    return {
        'flood': flood_data,
        'fire': fire_data,
        'forest': forest_data
    }

def create_sample_hypotheses():
    """Create sample hypotheses for demonstration"""
    framework = HypothesisFramework()
    
    # Flood hypothesis
    framework.create_hypothesis(
        "Flood Impact on SAR Backscatter",
        "Increased water coverage leads to decreased VV polarization backscatter due to specular reflection",
        ["Water extent", "VV backscatter", "Surface roughness"],
        "Strong negative correlation between water extent and VV backscatter"
    )
    
    # Fire hypothesis
    framework.create_hypothesis(
        "Post-fire Vegetation Recovery",
        "Vegetation regrowth after wildfire shows exponential recovery pattern in VH/VV ratio",
        ["Time since fire", "VH/VV ratio", "Vegetation density"],
        "Exponential increase in VH/VV ratio over time post-fire"
    )
    
    # Forest hypothesis
    framework.create_hypothesis(
        "Deforestation Detection Sensitivity",
        "C-band SAR is more sensitive to forest structure changes than L-band",
        ["Forest biomass", "C-band backscatter", "L-band backscatter"],
        "Higher correlation between biomass changes and C-band than L-band"
    )
    
    return framework

if __name__ == "__main__":
    # Demonstration
    print("SAR Analysis Utilities - NASA Space Apps Challenge")
    print("=" * 50)
    
    # Generate sample data
    sample_data = generate_sample_data()
    print(f"Generated sample data for {len(sample_data)} processes")
    
    # Create sample hypotheses
    framework = create_sample_hypotheses()
    print(f"Created {len(framework.hypotheses)} sample hypotheses")
    
    # Test hypotheses
    for i in range(len(framework.hypotheses)):
        result = framework.test_hypothesis(i, sample_data['flood'])
        print(f"Hypothesis {i}: {result['status']} (p={result['p_value']:.3f})")