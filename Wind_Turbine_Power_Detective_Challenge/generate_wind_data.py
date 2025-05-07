import pandas as pd
import numpy as np
import random

# Define months
months = [
    'January', 'February', 'March', 'April', 'May', 'June',
    'July', 'August', 'September', 'October', 'November', 'December'
]

# Valentia Observatory data (baseline)
valentia_wind_speeds = [
    9.2, 8.7, 8.1, 6.5, 6.0, 5.7,
    5.5, 5.8, 6.9, 7.8, 8.5, 9.0
]

# Create Valentia Observatory dataset
valentia_df = pd.DataFrame({
    'Month': months,
    'Wind Speed (m/s)': valentia_wind_speeds
})

# Save Valentia data
valentia_df.to_excel('Valentia_Observatory_Wind_2024.xlsx', index=False)
print("Created Valentia Observatory dataset")

# Define offshore locations around Ireland
locations = [
    "Dublin Bay (East)",
    "Cork Harbour (South)",
    "Shannon Estuary (West)",
    "Galway Bay (West)",
    "Donegal Bay (Northwest)",
    "Irish Sea (East)",
    "Celtic Sea (South)",
    "Atlantic Coast (West)"
]

# Wind speed adjustment factors relative to Valentia
# Based on general Irish wind patterns where west/northwest tends to be windier
location_factors = [
    0.85,  # Dublin Bay - less windy than west coast
    0.95,  # Cork Harbour
    1.05,  # Shannon Estuary - slightly windier
    1.10,  # Galway Bay
    1.15,  # Donegal Bay - among the windiest areas
    0.90,  # Irish Sea
    1.00,  # Celtic Sea
    1.20   # Atlantic Coast - most exposed to Atlantic winds
]

# Generate artificial datasets for each location
for i, location in enumerate(locations):
    wind_speeds = []

    # Create monthly wind speeds with realistic variations
    for j in range(len(months)):
        # Apply location factor plus small random variation (±10%)
        random_variation = 0.9 + (random.random() * 0.2)
        wind_speed = valentia_wind_speeds[j] * location_factors[i] * random_variation
        wind_speeds.append(round(wind_speed, 1))

    # Create DataFrame
    df = pd.DataFrame({
        'Month': months,
        'Wind Speed (m/s)': wind_speeds
    })

    # Save to Excel file
    filename = f"{location.replace(' ', '_').replace('(', '').replace(')', '')}_Wind_2024.xlsx"
    df.to_excel(filename, index=False)
    print(f"Created dataset for {location}")

print("\nAll datasets created successfully!")
