import pandas as pd
import numpy as np
import random

# Define months
months = [
    'January', 'February', 'March', 'April', 'May', 'June',
    'July', 'August', 'September', 'October', 'November', 'December'
]

# Loop Head baseline data (exposed Atlantic coast)
# Wave heights in meters - higher in winter months due to Atlantic storms
loop_head_wave_heights = [
    3.2, 3.0, 2.8, 2.3, 1.8, 1.5,
    1.3, 1.4, 2.0, 2.5, 2.9, 3.1
]

# Wave periods in seconds - typically 8-12s for Atlantic swells
loop_head_wave_periods = [
    10.5, 10.2, 9.8, 9.0, 8.5, 8.2,
    8.0, 8.1, 8.8, 9.5, 10.0, 10.3
]

# Create Loop Head dataset (baseline reference site)
loop_head_df = pd.DataFrame({
    'Month': months,
    'Significant Wave Height (m)': loop_head_wave_heights,
    'Average Wave Period (s)': loop_head_wave_periods
})

# Save Loop Head data
loop_head_df.to_excel('Loop_Head_Wave_2024.xlsx', index=False)
print("Created Loop Head dataset (baseline)")

# Define coastal locations around Ireland for wave energy
# Focus on exposed coastlines with good wave climate
locations = [
    "Belmullet (Northwest)",     # Very exposed to Atlantic
    "Malin Head (North)",        # Northern exposure
    "Dunmore East (Southeast)",  # Irish Sea waves
    "Old Head Kinsale (South)",  # Celtic Sea exposure
    "Brandon Bay (Southwest)",   # Atlantic swells
    "Aran Islands (West)",       # Direct Atlantic exposure
    "Achill Island (West)",      # Atlantic coast
    "Fastnet Rock (Southwest)"   # Extreme exposure
]

# Wave height adjustment factors relative to Loop Head
# Based on exposure to Atlantic swells and local bathymetry
location_height_factors = [
    1.10,  # Belmullet - very exposed
    0.85,  # Malin Head - some shelter from west
    0.70,  # Dunmore East - Irish Sea, smaller waves
    0.90,  # Old Head Kinsale - good exposure
    1.05,  # Brandon Bay - excellent exposure
    1.15,  # Aran Islands - fully exposed
    1.08,  # Achill Island - good Atlantic exposure
    1.20   # Fastnet Rock - most extreme exposure
]

# Wave period adjustment factors
# Exposed sites get longer period swells
location_period_factors = [
    1.05,  # Belmullet
    0.95,  # Malin Head
    0.85,  # Dunmore East - shorter period local waves
    0.98,  # Old Head Kinsale
    1.02,  # Brandon Bay
    1.08,  # Aran Islands - long Atlantic swells
    1.03,  # Achill Island
    1.10   # Fastnet Rock - longest swells
]

# Generate artificial datasets for each location
for i, location in enumerate(locations):
    wave_heights = []
    wave_periods = []

    # Create monthly data with realistic variations
    for j in range(len(months)):
        # Wave height with location factor and random variation (±15%)
        height_variation = 0.85 + (random.random() * 0.30)
        wave_height = loop_head_wave_heights[j] * location_height_factors[i] * height_variation
        wave_heights.append(round(wave_height, 1))

        # Wave period with less variation (±10%) as periods are more stable
        period_variation = 0.90 + (random.random() * 0.20)
        wave_period = loop_head_wave_periods[j] * location_period_factors[i] * period_variation
        wave_periods.append(round(wave_period, 1))

    # Create DataFrame with both wave parameters
    df = pd.DataFrame({
        'Month': months,
        'Significant Wave Height (m)': wave_heights,
        'Average Wave Period (s)': wave_periods
    })

    # Save to Excel file
    filename = f"{location.replace(' ', '_').replace('(', '').replace(')', '')}_Wave_2024.xlsx"
    df.to_excel(filename, index=False)
    print(f"Created wave dataset for {location}")

print("\nAll wave energy datasets created successfully!")
print("\nNote: Wave energy depends on both height AND period.")
print("Power is proportional to H²T (height squared × period)")
