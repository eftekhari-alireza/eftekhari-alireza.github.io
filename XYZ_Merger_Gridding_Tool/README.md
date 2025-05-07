# 🌊 XYZ Merger & Gridding Tool

A Python script to merge multiple terrain datasets in `.xyz` format, interpolate them onto a regular grid, and export the gridded output. This tool is ideal for coastal modeling, marine GIS, and environmental visualization projects.

---

## 📦 Features

- Merges multiple `.xyz` files into a unified dataset
- Supports elevation and bathymetry data
- Interpolates onto a regular grid using `nearest` (default), `linear`, or `cubic` methods
- Exports the result as a clean, gridded `.xyz` file
- Visualizes both raw data and interpolated results

---

## 📂 Input

Each input file must be a text file in XYZ format:

X Y Z

markdown
Copy
Edit

- `X`: Longitude or local X coordinate  
- `Y`: Latitude or local Y coordinate  
- `Z`: Elevation (positive) or Depth (negative)

Example files:
- `Topo.xyz`
- `HY-TOPO.xyz`
- `hydro-5m.xyz`

---

## 🛠 Requirements

Install the dependencies with:

```bash
pip install numpy pandas scipy matplotlib
🚀 Usage
Update the input files list in xyz_merger_and_gridding.py:

input_files = ['Topo.xyz', 'HY-TOPO.xyz', 'hydro-5m.xyz']
output_file = 'merged_gridded_output.xyz'
grid_spacing = 5  # meters
Run the script:


python xyz_merger_and_gridding.py
Output files:

merged_gridded_output.xyz: Tab-delimited XYZ file on a regular grid

Two PNG visualizations will be displayed showing raw and gridded data

🗺 Applications
Coastal and marine modeling (CROCO, MIKE, SWAN, etc.)

Flood modeling and adaptation planning

Digital Elevation Model (DEM) creation

Port and estuary engineering

Web-based mapping (e.g., CesiumJS, Leaflet)

🧠 Interpolation Methods
Edit the interpolation method in the script:


method='nearest'  # Options: 'nearest', 'linear', 'cubic'

👤 Author
Alireza Eftekhari
PhD Researcher
University of Galway

