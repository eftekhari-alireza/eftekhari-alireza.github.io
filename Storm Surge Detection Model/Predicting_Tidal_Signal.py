"""
# Script 2: Predicting Tidal Signal
# =================================
#
# This script performs the second step in tidal harmonic analysis:
# using the constituent information to reconstruct/predict the tidal signal.
#
# In this script, we:
# 1. Load the constituent data from Script 1
# 2. Create a time series with proper timestamps
# 3. Reconstruct the tidal signal using the constituent amplitudes and phases
# 4. Visualize and save the predicted tide for use in the next step
#
# The predicted tide represents the "pure" astronomical tidal signal
# without any weather or other non-tidal influences.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import os

# Create output directory for saving results
output_dir = './tidal_analysis_results'
os.makedirs(output_dir, exist_ok=True)

# Load original SSH data for comparison
def load_original_data(file_path, has_header=False):
    """Load the original SSH data"""
    print(f"Loading original data from {file_path}...")

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

    return ssh_values

# Create time index for the data
def create_time_index(length, start_date='2022-01-01', freq='h'):
    """Create a time index for the SSH data"""
    print(f"Creating time index starting from {start_date}...")

    start = pd.to_datetime(start_date)
    return pd.date_range(start=start, periods=length, freq=freq)

# Load the constituent parameters from Script 1
def load_constituent_parameters():
    """Load the constituent parameters saved by Script 1"""
    print("Loading constituent parameters...")

    param_file = f'{output_dir}/model_parameters.npz'
    if not os.path.exists(param_file):
        raise FileNotFoundError(f"Could not find {param_file}. Run Script 1 first.")

    data = np.load(param_file, allow_pickle=True)
    params = data['params']
    intercept = data['intercept']
    frequencies = data['frequencies']
    constituent_names = data['constituent_names']

    # Also load the constituent DataFrame for reference
    constituent_df = pd.read_csv(f'{output_dir}/tidal_constituents.csv')

    print(f"Loaded parameters for {len(constituent_names)} constituents")
    return params, intercept, frequencies, constituent_names, constituent_df

# Create a prediction function using constituent parameters
def predict_tide(t, params, intercept, frequencies):
    """
    Predict tidal heights using constituent parameters

    Parameters:
    -----------
    t : numpy.ndarray
        Time vector (numeric indices)
    params : numpy.ndarray
        Model coefficients
    intercept : float
        Model intercept
    frequencies : numpy.ndarray
        Array of frequencies

    Returns:
    --------
    numpy.ndarray
        Predicted tidal heights
    """
    print("Predicting tidal signal...")

    # Create design matrix for prediction
    X_pred = np.zeros((len(t), 2 * len(frequencies)))
    for i, freq in enumerate(frequencies):
        X_pred[:, 2*i] = np.cos(2 * np.pi * freq * t)
        X_pred[:, 2*i+1] = np.sin(2 * np.pi * freq * t)

    # Calculate predicted values
    predicted_ssh = X_pred.dot(params) + intercept

    print("Tidal prediction complete")
    return predicted_ssh

# Function to demonstrate individual constituent contributions
def visualize_constituent_contributions(time_index, frequencies, params, intercept, constituent_names, top_n=3):
    """
    Visualize how individual top constituents contribute to the overall tide

    This is educational to show how tides are composed of multiple sinusoidal components
    """
    print(f"Visualizing contributions of top {top_n} constituents...")

    # Get numeric time vector
    t = np.arange(len(time_index))

    # Get indices of top constituents by amplitude
    cos_coeffs = params[0::2]
    sin_coeffs = params[1::2]
    amplitudes = np.sqrt(cos_coeffs**2 + sin_coeffs**2)
    top_indices = np.argsort(amplitudes)[::-1][:top_n]

    # Set up plot
    fig, axes = plt.subplots(top_n + 1, 1, figsize=(14, 10), sharex=True)

    # Plot each top constituent individually
    for i, idx in enumerate(top_indices):
        # Create design matrix with just this constituent
        X_single = np.zeros((len(t), 2 * len(frequencies)))
        X_single[:, 2*idx] = np.cos(2 * np.pi * frequencies[idx] * t)
        X_single[:, 2*idx+1] = np.sin(2 * np.pi * frequencies[idx] * t)

        # Calculate contribution of just this constituent
        single_contribution = X_single.dot(params) + (intercept / len(frequencies))

        # Plot
        constituent = constituent_names[idx]
        amp = amplitudes[idx]
        axes[i].plot(time_index[:168], single_contribution[:168], label=f'{constituent} contribution')
        axes[i].set_ylabel('Height (m)')
        axes[i].set_title(f'{constituent} - Amplitude: {amp:.3f}m')
        axes[i].grid(True, alpha=0.3)

        # Highlight peaks for educational purposes
        period_hours = 1/frequencies[idx]
        axes[i].text(0.02, 0.85, f'Period: {period_hours:.2f} hours',
                    transform=axes[i].transAxes, bbox=dict(facecolor='white', alpha=0.7))

    # Calculate full predicted tide (all constituents)
    X_full = np.zeros((len(t), 2 * len(frequencies)))
    for i, freq in enumerate(frequencies):
        X_full[:, 2*i] = np.cos(2 * np.pi * freq * t)
        X_full[:, 2*i+1] = np.sin(2 * np.pi * freq * t)
    full_tide = X_full.dot(params) + intercept

    # Plot full tide
    axes[-1].plot(time_index[:168], full_tide[:168], 'r-', label='Complete tidal prediction')
    axes[-1].set_ylabel('Height (m)')
    axes[-1].set_title('Complete Tidal Prediction (All Constituents Combined)')
    axes[-1].grid(True, alpha=0.3)

    # Format x-axis with date labels (just show one week)
    for ax in axes:
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d %H:00'))
        ax.xaxis.set_major_locator(mdates.DayLocator(interval=1))

    plt.xlabel('Date/Time')
    plt.tight_layout()
    plt.savefig(f'{output_dir}/constituent_contributions.png', dpi=300)
    plt.show()

# Main function to predict tidal signal
def predict_tidal_signal(file_path, start_date='2022-01-01', has_header=False):
    """Main function to predict tidal signal from constituent parameters"""

    print("\n= Step 2: Predicting Tidal Signal =\n")

    # Load original data for comparison
    original_ssh = load_original_data(file_path, has_header)

    # Load constituent parameters from Script 1
    params, intercept, frequencies, constituent_names, constituent_df = load_constituent_parameters()

    # Create time vectors
    t = np.arange(len(original_ssh))
    time_index = create_time_index(len(original_ssh), start_date)

    # Predict tidal signal using the constituent parameters
    predicted_ssh = predict_tide(t, params, intercept, frequencies)

    # Create DataFrame with both original and predicted data
    tidal_df = pd.DataFrame({
        'Timestamp': time_index,
        'Original_SSH': original_ssh,
        'Predicted_SSH': predicted_ssh
    })

    # Save the predicted tide data
    print("Saving predicted tide data...")
    tidal_df.to_csv(f'{output_dir}/predicted_tide.csv', index=False)

    # Visualize original and predicted tides (full time series)
    print("Creating visualizations...")
    fig, ax = plt.subplots(figsize=(14, 7))
    ax.plot(time_index, original_ssh, label='Original SSH', linestyle='-', color='blue', linewidth=1)
    ax.plot(time_index, predicted_ssh, label='Predicted Tide', linestyle='--', color='red', linewidth=1)

    # Format x-axis with date labels
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    fig.autofmt_xdate()

    plt.xlabel('Date')
    plt.ylabel('Sea Surface Height (m)')
    plt.title('Comparison of Original and Predicted Sea Surface Height')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(f'{output_dir}/ssh_comparison_full.png', dpi=300)
    plt.show()

    # Show a shorter time period (one week) for better detail
    one_week = slice(0, 7*24)  # 7 days
    fig, ax = plt.subplots(figsize=(14, 7))
    ax.plot(time_index[one_week], original_ssh[one_week], label='Original SSH', linestyle='-', color='blue', linewidth=1)
    ax.plot(time_index[one_week], predicted_ssh[one_week], label='Predicted Tide', linestyle='--', color='red', linewidth=1)

    # Format x-axis with date labels
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d %H:00'))
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=1))
    fig.autofmt_xdate()

    plt.xlabel('Date')
    plt.ylabel('Sea Surface Height (m)')
    plt.title('Comparison of Original and Predicted Sea Surface Height (7-Day Sample)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(f'{output_dir}/ssh_comparison_week.png', dpi=300)
    plt.show()

    # Visualize the contributions of top constituents (educational)
    visualize_constituent_contributions(time_index, frequencies, params, intercept, constituent_names)

    print(f"\nAll predicted tide data saved to {output_dir}/predicted_tide.csv")

    return tidal_df

# Execute the prediction
if __name__ == "__main__":
    file_path = 'adjusted_data (3).csv'  # Adjust this path to your data file
    tidal_df = predict_tidal_signal(file_path)

    print("\n==== EDUCATIONAL NOTES ====")
    print("The predicted tide is a reconstruction of the 'pure' astronomical tide")
    print("based on the tidal constituents identified in Step 1.")
    print("\nThis predicted tide should match the overall pattern of the original data,")
    print("but without the non-tidal influences like weather, which we'll extract in Step 3.")
    print("\nThe constituent contribution plots show how each major tidal constituent")
    print("contributes to the overall tidal pattern. Notice how they have different periods,")
    print("amplitudes, and phases, which combine to create the complex tidal pattern.")
    print("\nIn the next step, we'll extract the storm surge by subtracting this")
    print("predicted tide from the original measurements.")
