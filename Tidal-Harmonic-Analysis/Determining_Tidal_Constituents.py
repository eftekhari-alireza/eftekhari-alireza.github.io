"""
Author: Alireza Eftekhadi
PhD Researcher, University of Galway
a.eftekhari2@universityofgalway.ie

# Determining Tidal Constituents
# =======================================
#
# Identifying and calculating the amplitude and phase of tidal constituents.
#
# Tidal constituents represent different astronomical forces (from the sun, moon, etc.)
# that contribute to the overall tidal pattern. Each has a known frequency based on
# astronomical calculations.
#
# This script will:
# 1. Load the SSH (Sea Surface Height) data
# 2. Create a design matrix based on tidal constituent frequencies
# 3. Fit a linear model to determine amplitude and phase of each constituent
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score
from sklearn.linear_model import LinearRegression
import os

# Create output directory for saving results
output_dir = './tidal_analysis_results'
os.makedirs(output_dir, exist_ok=True)

# Define function to load and preprocess SSH data
def load_ssh_data(file_path, has_header=False):
    """Load sea surface height data from a CSV file"""
    print(f"Loading data from {file_path}...")

    if has_header:
        ssh_data = pd.read_csv(file_path)
        ssh_values = ssh_data.iloc[:, 0].values
    else:
        ssh_data = pd.read_csv(file_path, header=None)
        ssh_values = ssh_data.iloc[:, 0].values

    # Handle potential missing or non-numeric data
    ssh_values = pd.to_numeric(ssh_values, errors='coerce')
    if np.isnan(ssh_values).any():
        print("Data contains NaN values. Filling missing data using linear interpolation...")
        ssh_values = pd.Series(ssh_values).interpolate(method='linear', limit_direction='both').values

    # Ensure 'ssh_values' is a one-dimensional array
    ssh_values = ssh_values.flatten()

    print(f"Loaded {len(ssh_values)} data points.")
    return ssh_values

# Define the tidal constituents and their frequencies
def define_tidal_constituents():
    """Define standard tidal constituent frequencies in cycles per hour"""
    print("Defining tidal constituents...")
    # Frequencies converted from degrees per hour to cycles per hour
    constituents = {
        'M2': 28.9841042 / 360,  # Principal lunar semidiurnal (12.42 hour period)
        'S2': 30.0000000 / 360,  # Principal solar semidiurnal (12.00 hour period)
        'N2': 28.4397295 / 360,  # Larger lunar elliptic semidiurnal (12.66 hour period)
        'K2': 30.0821373 / 360,  # Lunisolar semidiurnal (11.97 hour period)
        'K1': 15.0410686 / 360,  # Lunar diurnal (23.93 hour period)
        'O1': 13.9430356 / 360,  # Lunar diurnal (25.82 hour period)
        'P1': 14.9589314 / 360,  # Solar diurnal (24.07 hour period)
        'Q1': 13.3986609 / 360,  # Larger lunar elliptic diurnal (26.87 hour period)
        'Mf': 1.0980331 / 360,   # Lunar fortnightly (327.86 hour period)
        'Mm': 0.5443747 / 360,   # Lunar monthly (661.30 hour period)
        'Ssa': 0.0821373 / 360,  # Solar semiannual (4382.9 hour period)
        'M4': 57.9682084 / 360   # Shallow water overtides of principal lunar (6.21 hour period)
    }

    print(f"Defined {len(constituents)} tidal constituents")
    return constituents

# Create the design matrix for linear regression
def create_design_matrix(t, freqs):
    """
    Create a design matrix for tidal harmonic analysis

    For each constituent frequency, we need both sine and cosine terms to
    account for the amplitude and phase.
    """
    print("Creating design matrix...")
    X = np.zeros((len(t), 2 * len(freqs)))
    for i, freq in enumerate(freqs):
        # For each frequency, we need both cosine and sine terms
        X[:, 2*i] = np.cos(2 * np.pi * freq * t)      # Cosine term
        X[:, 2*i+1] = np.sin(2 * np.pi * freq * t)    # Sine term

    print(f"Design matrix shape: {X.shape}")
    return X

# Function to extract constituent information from model parameters
def extract_constituent_info(params, constituent_names, frequencies):
    """Extract amplitudes and phases from the model parameters"""
    print("Extracting constituent information...")

    # Parameters come in pairs (cosine, sine) for each constituent
    cos_coeffs = params[0::2]  # Every even parameter (0, 2, 4...)
    sin_coeffs = params[1::2]  # Every odd parameter (1, 3, 5...)

    # Calculate amplitude and phase from cosine and sine coefficients
    amplitudes = np.sqrt(cos_coeffs**2 + sin_coeffs**2)
    phases = np.arctan2(sin_coeffs, cos_coeffs) * (180 / np.pi)  # Convert to degrees
    phases = np.mod(phases, 360)  # Adjust phase angles to be between 0 and 360 degrees

    # Create a dataframe with results
    results_df = pd.DataFrame({
        'Constituent': constituent_names,
        'Frequency (cycles per hour)': frequencies,
        'Period (hours)': 1/frequencies,
        'Amplitude': amplitudes,
        'Phase (degrees)': phases,
        'Cosine_coef': cos_coeffs,
        'Sine_coef': sin_coeffs
    })

    # Sort the dataframe by amplitude in descending order
    results_df = results_df.sort_values(by='Amplitude', ascending=False).reset_index(drop=True)

    print("Constituent information extracted")
    return results_df

# Main function to analyze tidal constituents
def analyze_tidal_constituents(file_path, start_date='2022-01-01', has_header=False):
    """Main function to determine tidal constituents from SSH data"""

    print("\n= Step 1: Determining Tidal Constituents =\n")

    # Load SSH data
    ssh_values = load_ssh_data(file_path, has_header)

    # Create time vector
    t = np.arange(len(ssh_values))

    # Define tidal constituents
    constituents = define_tidal_constituents()
    frequencies = np.array(list(constituents.values()))
    constituent_names = list(constituents.keys())

    # Create design matrix
    X = create_design_matrix(t, frequencies)

    # Fit linear regression model
    print("Fitting linear regression model...")
    linear_model = LinearRegression()
    linear_model.fit(X, ssh_values)

    # Extract model parameters
    params = linear_model.coef_
    intercept = linear_model.intercept_

    # Extract constituent information
    results_df = extract_constituent_info(params, constituent_names, frequencies)

    # Save results to files
    print("Saving results...")
    results_df.to_csv(f'{output_dir}/tidal_constituents.csv', index=False)

    # Save model parameters for later use
    np.savez(f'{output_dir}/model_parameters.npz',
             params=params,
             intercept=intercept,
             frequencies=frequencies,
             constituent_names=constituent_names)

    # Calculate basic model fit statistics
    reconstructed_ssh = X.dot(params) + intercept
    r_squared = r2_score(ssh_values, reconstructed_ssh)
    print(f"R-squared of the model: {r_squared:.4f}")

    # Plot the top constituents
    plt.figure(figsize=(12, 6))
    top_n = min(10, len(results_df))  # Show top 10 or all if less than 10
    bars = plt.bar(results_df['Constituent'][:top_n], results_df['Amplitude'][:top_n], color='tab:blue', alpha=0.7)

    # Add amplitude values on top of bars
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                f'{height:.3f}', ha='center', va='bottom', rotation=0)

    plt.xlabel('Tidal Constituent')
    plt.ylabel('Amplitude (m)')
    plt.title('Top Tidal Constituents by Amplitude')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(f'{output_dir}/top_constituents.png', dpi=300)
    plt.show()

    # Print the top constituents
    print("\nTop 5 Tidal Constituents:")
    print(results_df.head(5)[['Constituent', 'Period (hours)', 'Amplitude', 'Phase (degrees)']])

    print(f"\nAll tidal constituent data saved to {output_dir}/tidal_constituents.csv")
    print(f"Model parameters saved to {output_dir}/model_parameters.npz")

    return results_df, params, intercept

# Execute the analysis
if __name__ == "__main__":
    file_path = 'adjusted_data (3).csv'  # Adjust this path to your data file
    results_df, params, intercept = analyze_tidal_constituents(file_path)

    print("\n==== EDUCATIONAL NOTES ====")
    print("Tidal constituent analysis is based on the fact that tides are caused by a combination")
    print("of astronomical forces, each with a characteristic frequency.")
    print("The largest constituent is typically M2 (the principal lunar semidiurnal tide)")
    print("with a period of about 12.42 hours.")
    print("\nThe amplitude of each constituent tells us how much it contributes to the overall tide.")
    print("The phase tells us when each constituent's peak occurs relative to a reference time.")
