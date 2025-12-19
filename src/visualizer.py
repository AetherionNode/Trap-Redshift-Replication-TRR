# src/visualizer.py

import matplotlib.pyplot as plt
import numpy as np

def plot_fidelity_vs_z(zs, fps, highlight_z=0.014):
    plt.figure(figsize=(8, 5))
    plt.plot(zs, fps, marker='o', label='Fidelity Proxy')
    plt.xlabel('Redshift (z)')
    plt.ylabel('Coherence Proxy (Fidelity)')
    plt.title('Sensitivity of Coherence Proxy to Detuning')
    plt.grid(True)
    # Highlight the z=0.014 dip
    idx = (np.abs(zs - highlight_z)).argmin()
    plt.scatter([zs[idx]], [fps[idx]], color='red', zorder=5)
    plt.annotate('Cosmic Confinement Limit',
                 xy=(zs[idx], fps[idx]),
                 xytext=(zs[idx]+0.03, fps[idx]-0.1),
                 arrowprops=dict(facecolor='red', shrink=0.05),
                 fontsize=10, color='red')
    plt.legend()
    plt.tight_layout()
    plt.savefig('results/fidelity_vs_z.png')
    plt.show()

if __name__ == "__main__":
    # Example usage: load data from demo or CSV
    import os
    import csv
    zs, fps = [], []
    csv_path = 'results/trr_log.csv'
    if os.path.exists(csv_path):
        with open(csv_path, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                zs.append(float(row['z']))
                fps.append(float(row['fidelity_proxy']))
    else:
        # fallback: generate dummy data
        zs = np.linspace(0, 0.02, 12)
        fps = 1 - 30 * (zs - 0.014)**2
    plot_fidelity_vs_z(np.array(zs), np.array(fps))
