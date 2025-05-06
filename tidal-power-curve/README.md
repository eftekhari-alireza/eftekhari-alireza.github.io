# Tidal Stream Turbine Power Curve

This repository contains Python scripts to analyze and model the power curve of a tidal stream turbine using real tidal current data from the Shannon Estuary and a standardized methodology based on the paper:

**Reference**:  
*Lewis, M., Neill, S. P., Robins, P. E., Hashemi, M. R., & Ward, S. (2015). Resource assessment for future generations of tidal-stream energy arrays.* Renewable Energy, 83, 142–157.  
 Section 3.3 and Equation (5) define the standardized power curve used in this repository.

---

##  Overview

We use real tidal velocity data from 1995–2024 and follow the paper’s recommended approach to:

1. Derive the **maximum observed velocity** at the site.
2. Use a ratio \( U_r / U_{\text{max}} = 0.87 \) (Scenario A2) to determine the rated speed.
3. Apply the standardised power coefficient \( C_p = 0.37 \) and calculate:
   - Cut-in speed = \( 0.3 \cdot U_r \)
   - Cut-out speed = \( 1.5 \cdot U_r \)
   - Rated power \( P_r \)
4. Generate a site-specific power curve using this information.

---

##  Files

### `01_extract_rated_power.py`

- Loads tidal current velocity data from `TidalCurrents_1995_2024_hourly.csv`
- Extracts maximum observed velocity
- Calculates rated speed, swept area, and rated power for a given turbine diameter
- Includes an optional interactive widget for exploring different rotor sizes

### `02_generate_power_curve.py`

- Uses the rated speed and turbine parameters to generate a full power curve
- Applies Equation (5) logic:
  - \( P = 0 \) below cut-in or above cut-out
  - Cubic power growth up to rated speed
  - Flat power at \( P_r \) until cut-out
- Saves the curve to `power_curve_site_cutout.csv`
- Produces a labelled power curve plot

---

##  Assumptions

- Rotor diameter: **20 m**
- Seawater density: **1025 kg/m³**
- Power coefficient: **0.37**
- Rated speed: **0.87 × Umax** (from site data)
- Cut-in: **0.3 × rated speed**, Cut-out: **1.5 × rated speed**
- Rated power calculated from first principles using site-specific speed

---

##  Outputs

- A CSV file containing tidal speed vs. power output
- A matplotlib plot showing the power curve with cut-in, rated, and cut-out points

---

## 👤 Author

Alireza Eftekhari
PhD Researcher, University of Galway
