"""
Script: xyz_merger_and_gridding.py
Description: Merge multiple XYZ terrain datasets, interpolate onto a regular grid,
             and export the gridded surface for use in modeling or GIS.
Author: Alireza [Your Last Name]
Date: 2025-05-07
"""

import pandas as pd
import numpy as np
from scipy.interpolate import griddata
import matplotlib.pyplot as plt
import os

# === USER INPUTS ===
input_files = ['Topo.xyz', 'HY-TOPO.xyz', 'hydro-5m.xyz']  # List your XYZ files here
output_file = 'merged_gridded_output.xyz'                  # Output file name
grid_spacing = 5                                           # Grid resolution (in same units as X, Y)

# === LOAD AND MERGE DATA ===
df_list = []
for file in input_files:
    if os.path.exists(file):
        df = pd.read_csv(file, sep=r'\s+|\t+', engine='python', header=None, names=['X', 'Y', 'Z'])
        df_list.append(df)
    else:
        print(f"Warning: {file} not found. Skipping.")

# Combine all XYZ points
df_combined = pd.concat(df_list, ignore_index=True)

# === VISUALIZE RAW MERGED DATA ===
plt.figure(figsize=(10, 8))
sc = plt.scatter(df_combined['X'], df_combined['Y'], c=df_combined['Z'], cmap='terrain', s=5)
plt.colorbar(sc, label='Elevation / Depth (m)')
plt.title('Merged Raw Terrain Data')
plt.xlabel('X')
plt.ylabel('Y')
plt.grid(True)
plt.tight_layout()
plt.show()

# === DEFINE REGULAR GRID ===
xmin, xmax = df_combined['X'].min(), df_combined['X'].max()
ymin, ymax = df_combined['Y'].min(), df_combined['Y'].max()

grid_x = np.arange(xmin, xmax, grid_spacing)
grid_y = np.arange(ymin, ymax, grid_spacing)
grid_X, grid_Y = np.meshgrid(grid_x, grid_y)

# === INTERPOLATE ONTO GRID ===
grid_Z = griddata(
    (df_combined['X'], df_combined['Y']),
    df_combined['Z'],
    (grid_X, grid_Y),
    method='nearest'  # Options: 'nearest', 'linear', 'cubic'
)

# === CONVERT TO FLAT XYZ FORMAT ===
df_grid = pd.DataFrame({
    'X': grid_X.flatten(),
    'Y': grid_Y.flatten(),
    'Z': grid_Z.flatten()
})

# === SAVE TO OUTPUT FILE ===
df_grid.to_csv(output_file, sep='\t', index=False, header=False)
print(f"\n✅ Gridded output saved to: {output_file}")

# === VISUALIZE FINAL GRID ===
plt.figure(figsize=(10, 8))
sc_grid = plt.scatter(df_grid['X'], df_grid['Y'], c=df_grid['Z'], cmap='terrain', s=5)
plt.colorbar(sc_grid, label='Interpolated Elevation / Depth (m)')
plt.title('Gridded Terrain Surface')
plt.xlabel('X')
plt.ylabel('Y')
plt.grid(True)
plt.tight_layout()
plt.show()
