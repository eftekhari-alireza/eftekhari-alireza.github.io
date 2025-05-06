"""
This script calculates the rated power of a tidal stream turbine using observed tidal current data
from the Shannon Estuary (1995–2024) and the standardised method from the paper 
'Resource assessment for future generations of tidal-stream energy arrays'.

Key steps:
- Uploads and reads the hourly tidal velocity dataset
- Extracts the maximum observed tidal speed (Umax)
- Computes the rated speed (Ur) using Scenario A2 (Ur/Umax = 0.87)
- Calculates the rated power based on turbine diameter, seawater density, and power coefficient (Cp = 0.37)
- Includes an optional interactive widget to explore rated power for different turbine diameters

Output:
- Displays Umax, rated speed, swept area, and calculated rated power in MW
"""



import pandas as pd
import numpy as np

# === Step 1: Upload the CSV file ===
from google.colab import files
uploaded = files.upload()

# === Step 2: Read the file ===
filename = 'TidalCurrents_1995_2024_hourly.csv'
df = pd.read_csv(filename)

# === Step 3: Extract Umax from Vel_Total column ===
Umax = df['Vel_Total'].max()
print(f"✅ Maximum observed velocity (Umax): {Umax:.3f} m/s")

# === Step 4: Use Scenario A2 from the paper: Ur = 0.87 * Umax ===
Ur = 0.87 * Umax
print(f"✅ Rated speed (Ur) using Scenario A2 (Ur/Umax = 0.87): {Ur:.3f} m/s")

# === Step 5: Turbine & fluid properties ===
rho = 1025        # Seawater density (kg/m³)
Cp = 0.37         # Power coefficient from the paper
D = 20            # Turbine diameter in meters (change if needed)
A = (np.pi * D**2) / 4  # Swept area (m²)

# === Step 6: Calculate Rated Power at Ur ===
Pr = 0.5 * rho * A * Cp * Ur**3    # Watts
Pr_MW = Pr / 1e6                   # Convert to MW

# === Step 7: Display results ===
print(f"✅ Swept area (A): {A:.2f} m²")
print(f"✅ Rated power at {Ur:.3f} m/s: {Pr:.2f} W ≈ {Pr_MW:.3f} MW")

# === Optional: interactive sweep for different diameters ===
try:
    from ipywidgets import interact
    def update_diameter(D=20):
        A = (np.pi * D**2) / 4
        Pr = 0.5 * rho * A * Cp * Ur**3
        Pr_MW = Pr / 1e6
        print(f"\n🔁 Diameter: {D} m → Rated Power: {Pr_MW:.3f} MW")
    interact(update_diameter, D=(5, 40, 1))
except:
    pass
