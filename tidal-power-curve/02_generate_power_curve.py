"""
Site-Specific Tidal Turbine Power Curve (Based on Shannon Estuary Data)

This script calculates and plots the power output curve of a single tidal-stream turbine 
using site-specific maximum tidal velocity and a standardised method based on the paper:

Lewis, M., Neill, S. P., Robins, P. E., Hashemi, M. R., & Ward, S. (2015). 
"Resource assessment for future generations of tidal-stream energy arrays."
*Renewable Energy, 83*, 142–157.

Key methodology:
- Rated speed (Vr) is determined using Scenario A2 from the paper: Vr = 0.87 × Umax
- Cut-in speed is 30% of Vr (Vs = 0.3 × Vr)
- Cut-out speed is assumed to be 150% of Vr (Vco = 1.5 × Vr) for realistic turbine control
- Power output follows the standard cubic relationship (P ∝ u³) up to Vr,
  and is constant at rated power between Vr and Vco

Turbine parameters:
- Diameter = 20 m
- Power coefficient Cp = 0.37
- Seawater density = 1025 kg/m³

Outputs:
- A CSV file containing tidal speed vs. power output
- A plot of the turbine power curve showing cut-in, rated, and cut-out points
"""



import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# === 1. Turbine and environmental constants ===
D = 20.0                         # Turbine diameter (m)
A = np.pi * (D / 2)**2          # Swept area (m²)
rho = 1025.0                    # Seawater density (kg/m³)
Cp = 0.37                       # Power coefficient from the paper

# === 2. Site-specific input ===
Umax = 2.574                    # Maximum tidal velocity from your data
Vr = 0.87 * Umax                # Rated speed (Scenario A2)
Vs = 0.3 * Vr                   # Cut-in speed (30% of Vr)
Vco = 1.5 * Vr                  # Cut-out speed (150% of Vr)

# === 3. Compute rated power ===
Pr = 0.5 * rho * Cp * A * Vr**3
Pr_kW = Pr / 1000.0

# === 4. Print turbine performance specs ===
print(f" Umax (from site data): {Umax:.3f} m/s")
print(f" Rated speed (Vr)     : {Vr:.3f} m/s")
print(f" Cut-in speed (Vs)    : {Vs:.3f} m/s")
print(f" Cut-out speed (Vco)  : {Vco:.3f} m/s")
print(f" Rated power (Pr)     : {Pr:.0f} W ≈ {Pr_kW:.2f} kW")

# === 5. Generate speed range up to cut-out
speeds = np.arange(0.0, Vco + 0.01, 0.01)
powers = []

for u in speeds:
    if u < Vs or u > Vco:
        P = 0.0
    elif u <= Vr:
        P = 0.5 * rho * Cp * A * u**3
    else:  # Between Vr and Vco
        P = Pr
    powers.append(P / 1000.0)  # convert to kW

# === 6. Save results to CSV
df = pd.DataFrame({
    "Tidal Speed (m/s)": speeds,
    "Power Output (kW)": powers
})
df.to_csv("power_curve_site_cutout.csv", index=False)
print(" Saved: power_curve_site_cutout.csv")

# === 7. Plot power curve
plt.figure(figsize=(8, 5))
plt.plot(speeds, powers, label='Power Curve', color='blue')
plt.axvline(Vs, color='gray', linestyle='--', label=f"Cut-in (Vs = {Vs:.2f} m/s)")
plt.axvline(Vr, color='red', linestyle='--', label=f"Rated (Vr = {Vr:.2f} m/s)")
plt.axvline(Vco, color='black', linestyle='--', label=f"Cut-out (Vco = {Vco:.2f} m/s)")
plt.axhline(Pr_kW, color='green', linestyle='--', label=f"Rated Power ≈ {Pr_kW:.1f} kW")
plt.xlabel("Tidal Speed (m/s)")
plt.ylabel("Power Output (kW)")
plt.title("Site-Specific Tidal Turbine Power Curve (Ø20m)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
