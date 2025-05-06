"""
Script: croco_grid_visualizer.py
Description: Visualize the CROCO model grid, including bathymetry and land-sea mask,
             and compute basic statistical summaries of the bathymetry.
Author: Alireza [Your Last Name]
Date: 2025-05-07
Usage: python croco_grid_visualizer.py
"""

# 📚 Import libraries
import xarray as xr
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# 📂 Load CROCO grid NetCDF file
file_path = '/content/croco_grd_updated.nc'  # Update this path as needed
ds = xr.open_dataset(file_path)

# 🌊 Extract grid variables
h = ds['h'].values                  # Bathymetry (depth)
lon = ds['lon_rho'].values         # Longitude grid
lat = ds['lat_rho'].values         # Latitude grid
mask_rho = ds['mask_rho'].values   # Land-sea mask: 1 = ocean, 0 = land

# 📊 Bathymetry Statistics
bathymetry_stats = {
    'Min Depth (m)': np.nanmin(h),
    'Max Depth (m)': np.nanmax(h),
    'Mean Depth (m)': np.nanmean(h),
    'Std Deviation (m)': np.nanstd(h),
    'Median Depth (m)': np.nanmedian(h),
    'NaNs in h': int(np.isnan(h).sum()),
    'NaNs in mask_rho': int(np.isnan(mask_rho).sum())
}
print("=== Bathymetry Statistics ===")
print(pd.DataFrame([bathymetry_stats]))

# 🖼️ Plot 1: Land-Sea Mask
plt.figure(figsize=(10, 6))
plt.pcolormesh(lon, lat, mask_rho, shading='auto', cmap='Greys')
plt.colorbar(label='Land-Sea Mask (1=Ocean, 0=Land)')
plt.title('Grid with Land-Sea Mask')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.tight_layout()
plt.savefig('land_sea_mask.png', dpi=300)
plt.show()

# 🖼️ Plot 2: Bathymetry with Land-Sea Mask Overlay
plt.figure(figsize=(10, 6))
plt.pcolormesh(lon, lat, h, shading='auto', cmap='viridis')
plt.colorbar(label='Depth (m)')
plt.contour(lon, lat, mask_rho, levels=[0.5], colors='red', linewidths=1.0)
plt.title('Bathymetry with Land-Sea Mask Overlay')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.tight_layout()
plt.savefig('bathymetry_with_mask.png', dpi=300)
plt.show()

# ✅ Close dataset
ds.close()
