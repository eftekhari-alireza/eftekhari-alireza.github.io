# 🌊 CROCO Grid to JSON Exporter

This Python script extracts and downsamples bathymetry data from a CROCO grid file (`croco_grd.nc`) and converts it into a lightweight JSON format. The resulting file (`bathymetry.json`) is optimized for use in web-based visualization tools such as Plotly, Leaflet, Deck.gl, or CesiumJS.

---

## 🚀 Features

- Reads bathymetry and coordinate data from CROCO NetCDF grid files
- Subsamples the data to reduce size for faster performance
- Converts depth to negative values (standard for web visualization)
- Exports the result as a JSON file ready for frontend applications

---

## 📂 Input

A CROCO grid file (`.nc`) that includes:
- `h`: Bathymetry (positive depth values)
- `lon_rho`: Longitude grid
- `lat_rho`: Latitude grid

---

## 📤 Output

A JSON file (`bathymetry.json`) structured as:
```json
{
  "x": [lon1, lon2, ...],
  "y": [lat1, lat2, ...],
  "z": [-depth1, -depth2, ...]
}


📈 Applications
Interactive ocean maps

Coastal engineering dashboards

Marine spatial planning tools

Education and outreach platforms

👨‍💻 Author
Alireza Eftekhari
PhD Researcher
University of Galway

