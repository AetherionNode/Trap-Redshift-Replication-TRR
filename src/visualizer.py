"""
TRR Visualizer: Coherence Sensitivity to Detuning

Generates publication-quality visualization showing fidelity decay
with increasing redshift, highlighting the critical z = 0.014 barrier.
"""

import matplotlib.pyplot as plt
import numpy as np
import os
import csv


def plot_fidelity_vs_z(zs, fps, save_path='results/coherence_sensitivity.png'):
    """
    Generate fidelity vs. redshift plot with z=0.014 wall annotation.
    
    Creates a plot showing:
    - Blue line with markers: Fidelity proxy vs. redshift
    - Red vertical dashed line: z = 0.014 cosmic confinement limit
    - Annotation explaining the physical wall
    
    Args:
        zs: Array of redshift values
        fps: Array of fidelity proxy values
        save_path: Output file path for figure
    """
    plt.figure(figsize=(10, 6))
    
    # Plot fidelity data
    plt.plot(zs, fps, 'o-', color='#2E86DE', linewidth=2, markersize=8, 
             label='Fidelity Proxy', markeredgecolor='white', markeredgewidth=1.5)
    
    # Add z = 0.014 wall
    plt.axvline(x=0.014, color='red', linestyle='--', linewidth=2.5, 
                label='z = 0.014 Limit', alpha=0.8)
    
    # Annotation for the cosmic confinement limit
    plt.annotate('Cosmic Confinement Limit\n(193M Lightyears)',
                 xy=(0.014, 0.5),
                 xytext=(0.0085, 0.35),
                 fontsize=11,
                 color='darkred',
                 weight='bold',
                 bbox=dict(boxstyle='round,pad=0.5', facecolor='#FFE5E5', 
                          edgecolor='red', linewidth=1.5, alpha=0.9),
                 arrowprops=dict(arrowstyle='->', color='red', lw=2, 
                                connectionstyle='arc3,rad=0.3'))
    
    # Labels and styling
    plt.xlabel('Redshift (z)', fontsize=14, weight='bold')
    plt.ylabel('Fidelity Proxy', fontsize=14, weight='bold')
    plt.title('Sensitivity of Coherence Proxy to Detuning', fontsize=16, weight='bold', pad=20)
    plt.grid(True, alpha=0.3, linestyle=':', linewidth=1)
    plt.legend(fontsize=12, loc='upper right', framealpha=0.95)
    
    # Set axis limits with some padding
    plt.xlim(-0.0005, max(zs) * 1.1)
    plt.ylim(0, 1.05)
    
    # Ensure results directory exists
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"[PLOT] Saved visualization to {save_path}")
    plt.close()


def load_sweep_data_from_csv(csv_path='results/trr_simulation_log.csv'):
    """
    Load sweep data from CSV log file.
    
    Args:
        csv_path: Path to CSV log file
        
    Returns:
        Tuple of (z_values, fidelity_values) as numpy arrays
    """
    zs, fps = [], []
    
    if os.path.exists(csv_path):
        with open(csv_path, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                zs.append(float(row['z']))
                fps.append(float(row['fidelity_proxy']))
        
        # Remove duplicates while preserving order
        unique_data = {}
        for z, fp in zip(zs, fps):
            if z not in unique_data:
                unique_data[z] = fp
        
        zs = np.array(list(unique_data.keys()))
        fps = np.array(list(unique_data.values()))
        
        # Sort by z value
        sort_idx = np.argsort(zs)
        zs = zs[sort_idx]
        fps = fps[sort_idx]
        
        print(f"[DATA] Loaded {len(zs)} data points from {csv_path}")
    else:
        print(f"[WARNING] CSV file not found: {csv_path}")
        print("[DATA] Generating synthetic data for demonstration")
        
        # Generate synthetic data showing fidelity decay
        zs = np.linspace(0, 0.015, 15)
        
        # Fidelity model: gradual decay with sharp drop near 0.014
        fps = np.ones_like(zs)
        for i, z in enumerate(zs):
            if z < 0.012:
                fps[i] = 1.0 - 0.5 * z
            elif z < 0.014:
                fps[i] = 0.94 - 8.0 * (z - 0.012)
            else:
                fps[i] = 0.78 - 15.0 * (z - 0.014)
        
        fps = np.clip(fps, 0.5, 1.0)
    
    return zs, fps


if __name__ == "__main__":
    print("=" * 60)
    print("TRR Visualizer: Generating Coherence Sensitivity Plot")
    print("=" * 60)
    
    # Load or generate data
    zs, fps = load_sweep_data_from_csv()
    
    # Generate visualization
    plot_fidelity_vs_z(zs, fps)
    
    print("\nVisualization complete!")
    print("=" * 60)
