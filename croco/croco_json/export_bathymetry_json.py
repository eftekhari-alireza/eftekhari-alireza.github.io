# Author: Alireza Eftekhari
#         PhD Researcher



import xarray as xr
import numpy as np
import json

# Load your CROCO grid file
file_path = '/content/croco_grd.nc'
ds = xr.open_dataset(file_path)

# Extract bathymetry and coordinates
h = ds['h'].values
lon = ds['lon_rho'].values
lat = ds['lat_rho'].values

# Use all data points (no subsampling)
lon_sub = lon.flatten().tolist()
lat_sub = lat.flatten().tolist()
h_sub = (-h).flatten().tolist()  # Negative values for depth

# Create a dictionary to hold the data
bathymetry_data = {
    "x": lon_sub,
    "y": lat_sub,
    "z": h_sub
}

# Save to JSON file
with open('bathymetry.json', 'w') as f:
    json.dump(bathymetry_data, f)
