import pandas as pd
import numpy as np
import random

# Define months
months = [
    'January', 'February', 'March', 'April', 'May', 'June',
    'July', 'August', 'September', 'October', 'November', 'December'
]

# Shannon Estuary baseline data
# Tidal ranges in meters (spring tide averages by month)
# Ireland has semi-diurnal tides with spring/neap cycles
shannon_tidal_ranges = [
    4.8, 4.6, 4.9, 5.0, 4.7, 4.5,
    4.4, 4.6, 4.8, 5.0, 4.9, 4.7
]

# Peak tidal current velocities in m/s
# Currents are strongest during spring tides
shannon_current_velocities = [
    1.8, 1.7, 1.9, 1.9, 1.8, 1.7,
    1.6, 1.7, 1.8, 1.9, 1.9, 1.8
]

# Spring/Neap tide ratio (spring tides are ~1.4x neap tides)
spring_neap_ratio = 1.4

# Create Shannon Estuary dataset (baseline)
shannon_df = pd.DataFrame({
    'Month': months,
    'Mean Tidal Range (m)': shannon_tidal_ranges,
    'Peak Current Velocity (m/s)': shannon_current_velocities,
    'Spring Tide Range (m)': [r * 1.2 for r in shannon_tidal_ranges],
    'Neap Tide Range (m)': [r / spring_neap_ratio for r in shannon_tidal_ranges]
})

# Save Shannon data
shannon_df.to_excel('Shannon_Estuary_Tide_2024.xlsx', index=False)
print("Created Shannon Estuary tidal dataset (baseline)")

# Define tidal energy locations around Ireland
# Focus on straits, narrow channels, and areas with strong currents
locations = [
    "Strangford Lough (Northeast)",   # Famous for tidal turbine testing
    "Cork Harbour Entrance (South)",   # Large harbor with tidal flows
    "Tuskar Rock Channel (Southeast)", # Strong currents around headland
    "Saltee Sound (Southeast)",        # Channel between islands
    "Bulls Mouth (Southwest)",         # Narrow channel, strong currents
    "Blasket Sound (Southwest)",       # Between mainland and islands
    "Gregory Sound (West)",            # Between Aran Islands
    "Rathlin Sound (North)"           # Between Rathlin Island and mainland
]

# Tidal range adjustment factors relative to Shannon
# Based on local bathymetry and coastal configuration
location_range_factors = [
    0.85,  # Strangford - smaller range but faster currents
    0.75,  # Cork Harbour - moderate tidal range
    0.70,  # Tuskar Rock - open coast, smaller range
    0.80,  # Saltee Sound - good funneling effect
    0.90,  # Bulls Mouth - good range and currents
    0.95,  # Blasket Sound - excellent tidal resource
    0.88,  # Gregory Sound - good island channeling
    0.82   # Rathlin Sound - moderate range, good currents
]

# Current velocity adjustment factors
# Narrow channels and straits have higher velocities
location_velocity_factors = [
    1.40,  # Strangford - very strong currents in narrows
    0.85,  # Cork Harbour - moderate currents
    1.10,  # Tuskar Rock - accelerated flow around headland
    1.25,  # Saltee Sound - strong channel flow
    1.35,  # Bulls Mouth - very strong in narrow channel
    1.30,  # Blasket Sound - strong currents
    1.20,  # Gregory Sound - good channel acceleration
    1.15   # Rathlin Sound - enhanced currents
]

# Tidal asymmetry factors (flood vs ebb dominance)
# 1.0 = symmetric, >1.0 = flood dominant, <1.0 = ebb dominant
location_asymmetry = [
    1.05,  # Strangford - slightly flood dominant
    0.95,  # Cork Harbour - ebb dominant (draining large area)
    1.00,  # Tuskar Rock - symmetric
    1.10,  # Saltee Sound - flood dominant
    0.90,  # Bulls Mouth - ebb dominant
    1.00,  # Blasket Sound - symmetric
    1.08,  # Gregory Sound - flood dominant
    0.98   # Rathlin Sound - nearly symmetric
]

# Generate datasets for each location
for i, location in enumerate(locations):
    tidal_ranges = []
    current_velocities = []
    spring_ranges = []
    neap_ranges = []
    flood_velocities = []
    ebb_velocities = []

    # Create monthly data with realistic variations
    for j in range(len(months)):
        # Tidal range with small monthly variation (±5%)
        range_variation = 0.95 + (random.random() * 0.10)
        tidal_range = shannon_tidal_ranges[j] * location_range_factors[i] * range_variation
        tidal_ranges.append(round(tidal_range, 1))

        # Spring and neap ranges
        spring_range = tidal_range * 1.2  # Spring tides 20% higher
        neap_range = tidal_range / spring_neap_ratio
        spring_ranges.append(round(spring_range, 1))
        neap_ranges.append(round(neap_range, 1))

        # Current velocity with variation (±10%)
        velocity_variation = 0.90 + (random.random() * 0.20)
        current_velocity = shannon_current_velocities[j] * location_velocity_factors[i] * velocity_variation
        current_velocities.append(round(current_velocity, 2))

        # Flood and ebb velocities based on asymmetry
        flood_velocity = current_velocity * location_asymmetry[i]
        ebb_velocity = current_velocity / location_asymmetry[i]
        flood_velocities.append(round(flood_velocity, 2))
        ebb_velocities.append(round(ebb_velocity, 2))

    # Create comprehensive tidal dataset
    df = pd.DataFrame({
        'Month': months,
        'Mean Tidal Range (m)': tidal_ranges,
        'Spring Tide Range (m)': spring_ranges,
        'Neap Tide Range (m)': neap_ranges,
        'Peak Current Velocity (m/s)': current_velocities,
        'Peak Flood Velocity (m/s)': flood_velocities,
        'Peak Ebb Velocity (m/s)': ebb_velocities
    })

    # Save to Excel file
    filename = f"{location.replace(' ', '_').replace('(', '').replace(')', '')}_Tide_2024.xlsx"
    df.to_excel(filename, index=False)
    print(f"Created tidal dataset for {location}")

print("\nAll tidal energy datasets created successfully!")
print("\nNote: Tidal energy depends on current velocity cubed (P ∝ v³)")
print("Sites with currents >2 m/s are typically needed for commercial viability")
