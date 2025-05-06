# 🌍 CROCO Grid Visualizer

This Python script helps you **analyze and visualize the grid used in the CROCO ocean model**, specifically the bathymetry (`h`) and land-sea mask (`mask_rho`), both of which are critical for assessing the model setup before running simulations.

---

## 📌 Features

- ✅ Computes basic bathymetry statistics:
  - Minimum, Maximum, Mean, Median, Standard Deviation
  - Count of missing (NaN) values
- 🎨 Generates two useful plots:
  - **Land-Sea Mask** (`land_sea_mask.png`)
  - **Bathymetry with Mask Overlay** (`bathymetry_with_mask.png`)

---

## 📁 Input

A CROCO grid file in NetCDF format (`croco_grd.nc`), containing:
- `h`: Bathymetry values (depths in meters)
- `mask_rho`: Land-sea mask (1 = ocean, 0 = land)
- `lon_rho`, `lat_rho`: Longitude and latitude arrays

You can adjust the file path inside the script:
```python
file_path = '/path/to/your/croco_grd.nc'

🧪 Installation
Make sure you have the following Python libraries installed:

pip install xarray numpy pandas matplotlib

🚀 Usage
Run the script directly from the terminal:

python croco_grid_visualizer.py


📊 Output
Bathymetry statistics printed to console

Two PNG images saved:

land_sea_mask.png

bathymetry_with_mask.png

👨‍🔬 Author
Alireza Eftekhari
PhD Researcher in Numerical Ocean Modeling
University of Galway
