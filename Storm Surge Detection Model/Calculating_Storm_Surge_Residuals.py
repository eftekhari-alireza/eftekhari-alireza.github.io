"""
# Script 3: Calculating Storm Surge Residuals
# ===========================================
#
# This script performs the third step in tidal harmonic analysis:
# calculating the residual (storm surge) by subtracting the predicted tide
# from the original measured sea surface height.
#
# In this script, we:
# 1. Load the original data and predicted tide from Script 2
# 2. Calculate the residual (original - predicted)
# 3. Analyze the statistical properties of the residual
# 4. Visualize the storm surge components
# 5. Save the surge data for further analysis in Script 4
#
# The residual represents all non-tidal influences on sea level, primarily:
# - Meteorological effects (barometric pressure, wind)
# - Ocean dynamics (currents, eddies)
# - Measurement errors
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from scipy import stats
import os

# Create output directory for saving results
output_dir = './tidal_analysis_results'
os.makedirs(output_dir, exist_ok=True)

# Load the tidal data from Script 2
def load_tidal_data():
    """Load the tidal data produced by Script 2"""
    print("Loading tidal data...")

    tidal_file = f'{output_dir}/predicted_tide.csv'
    if not os.path.exists(tidal_file):
        raise FileNotFoundError(f"Could not find {tidal_file}. Run Script 2 first.")

    tidal_df = pd.read_csv(tidal_file)
    tidal_df['Timestamp'] = pd.to_datetime(tidal_df['Timestamp'])

    print(f"Loaded tidal data with {len(tidal_df)} data points")
    return tidal_df

# Calculate the residual (storm surge)
def calculate_storm_surge(tidal_df):
    """
    Calculate the residual (storm surge) by subtracting predicted tide from original

    Parameters:
    -----------
    tidal_df : pandas.DataFrame
        DataFrame containing original and predicted SSH

    Returns:
    --------
    pandas.DataFrame
        DataFrame with original, predicted, and residual data
    """
    print("Calculating storm surge residuals...")

    # Calculate the residual
    tidal_df['Storm_Surge'] = tidal_df['Original_SSH'] - tidal_df['Predicted_SSH']

    print("Storm surge calculation complete")
    return tidal_df

# Analyze storm surge statistics
def analyze_surge_statistics(surge_df):
    """Calculate and display statistics for the storm surge data"""
    print("Analyzing storm surge statistics...")

    # Basic statistics
    surge_stats = {
        'Mean': np.mean(surge_df['Storm_Surge']),
        'Median': np.median(surge_df['Storm_Surge']),
        'Std Dev': np.std(surge_df['Storm_Surge']),
        'Min': np.min(surge_df['Storm_Surge']),
        'Max': np.max(surge_df['Storm_Surge']),
        'Abs Max': np.max(np.abs(surge_df['Storm_Surge']))
    }

    # Calculate skewness and kurtosis
    skewness = stats.skew(surge_df['Storm_Surge'].dropna())
    kurtosis = stats.kurtosis(surge_df['Storm_Surge'].dropna())
    surge_stats['Skewness'] = skewness
    surge_stats['Kurtosis'] = kurtosis

    # Identify extreme events (beyond 3 standard deviations)
    std_dev = surge_stats['Std Dev']
    threshold = 3 * std_dev
    extreme_events = surge_df[np.abs(surge_df['Storm_Surge']) > threshold].copy()

    # Group consecutive extreme events
    if len(extreme_events) > 0:
        extreme_events['event_diff'] = extreme_events['Timestamp'].diff().dt.total_seconds() / 3600
        extreme_events['event_group'] = (extreme_events['event_diff'] > 3).cumsum()

        # Find the peak of each event group
        peak_events = extreme_events.groupby('event_group').apply(
            lambda x: x.loc[x['Storm_Surge'].abs().idxmax()]
        ).reset_index(drop=True)

        # Add direction of surge
        peak_events['Direction'] = ['Positive' if x > 0 else 'Negative' for x in peak_events['Storm_Surge']]

        # Sort by magnitude
        peak_events = peak_events.sort_values(by='Storm_Surge', key=abs, ascending=False)
    else:
        peak_events = pd.DataFrame(columns=['Timestamp', 'Storm_Surge', 'Direction'])

    print("Statistical analysis complete")
    return surge_stats, peak_events

# Visualize storm surge data
def visualize_storm_surge(surge_df, surge_stats, peak_events):
    """Create visualizations of the storm surge data"""
    print("Creating storm surge visualizations...")

    # Plot 1: Storm Surge Time Series
    fig, ax = plt.subplots(figsize=(14, 7))
    ax.plot(surge_df['Timestamp'], surge_df['Storm_Surge'], label='Storm Surge', color='green', linewidth=1)

    # Add a horizontal line at zero
    ax.axhline(y=0, color='red', linestyle='--', alpha=0.7)

    # Add threshold lines at +/- 2 standard deviations
    std_dev = surge_stats['Std Dev']
    ax.axhline(y=2*std_dev, color='orange', linestyle=':', alpha=0.7, label='+2σ Threshold')
    ax.axhline(y=-2*std_dev, color='orange', linestyle=':', alpha=0.7, label='-2σ Threshold')

    # Format x-axis with date labels
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    fig.autofmt_xdate()

    # Highlight extreme events
    for _, event in peak_events.iterrows():
        if event['Storm_Surge'] > 0:
            color = 'red'
        else:
            color = 'purple'
        ax.plot(event['Timestamp'], event['Storm_Surge'], 'o', color=color, markersize=8)

    plt.xlabel('Date')
    plt.ylabel('Storm Surge (m)')
    plt.title('Storm Surge (Residual After Removing Tidal Signal)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(f'{output_dir}/storm_surge_raw.png', dpi=300)
    plt.show()

    # Plot 2: Storm Surge Distribution
    plt.figure(figsize=(10, 6))
    plt.hist(surge_df['Storm_Surge'], bins=50, color='skyblue', edgecolor='black', alpha=0.7)
    plt.axvline(x=0, color='red', linestyle='--')

    # Add vertical lines for standard deviations
    plt.axvline(x=std_dev, color='orange', linestyle=':', label='+1σ')
    plt.axvline(x=-std_dev, color='orange', linestyle=':')
    plt.axvline(x=2*std_dev, color='orange', linestyle='--', label='+2σ')
    plt.axvline(x=-2*std_dev, color='orange', linestyle='--')

    plt.xlabel('Storm Surge (m)')
    plt.ylabel('Frequency')
    plt.title('Distribution of Storm Surge Values')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(f'{output_dir}/surge_distribution_raw.png', dpi=300)
    plt.show()

    # Plot 3: Monthly Box Plot (to see seasonal patterns)
    surge_df['Month'] = surge_df['Timestamp'].dt.month
    monthly_data = [surge_df[surge_df['Month'] == month]['Storm_Surge'] for month in range(1, 13)]

    plt.figure(figsize=(12, 6))
    plt.boxplot(monthly_data, labels=[
        'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
    ])
    plt.axhline(y=0, color='red', linestyle='--', alpha=0.7)
    plt.xlabel('Month')
    plt.ylabel('Storm Surge (m)')
    plt.title('Monthly Distribution of Storm Surge')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(f'{output_dir}/surge_monthly_boxplot.png', dpi=300)
    plt.show()

    print("Visualizations complete")

# Main function to calculate and analyze storm surge
def calculate_and_analyze_surge():
    """Main function to calculate and analyze storm surge from tidal data"""

    print("\n= Step 3: Calculating Storm Surge Residuals =\n")

    # Load tidal data from Script 2
    tidal_df = load_tidal_data()

    # Calculate storm surge
    surge_df = calculate_storm_surge(tidal_df)

    # Analyze surge statistics
    surge_stats, peak_events = analyze_surge_statistics(surge_df)

    # Create visualizations
    visualize_storm_surge(surge_df, surge_stats, peak_events)

    # Save surge data for further analysis
    print("Saving storm surge data...")
    surge_df.to_csv(f'{output_dir}/storm_surge_raw.csv', index=False)

    # Save significant events to a separate file
    if len(peak_events) > 0:
        peak_events.to_csv(f'{output_dir}/extreme_surge_events_raw.csv', index=False)

    # Generate a report on surge statistics
    with open(f'{output_dir}/surge_statistics_raw.txt', 'w') as f:
        f.write("STORM SURGE STATISTICS (RAW)\n")
        f.write("===========================\n\n")
        for key, value in surge_stats.items():
            f.write(f"{key}: {value:.4f}\n")

        f.write("\nEXTREME SURGE EVENTS (>3σ)\n")
        f.write("==========================\n\n")
        if len(peak_events) > 0:
            for i, (_, event) in enumerate(peak_events.iterrows(), 1):
                if i > 10:  # Limit to top 10 events
                    break
                f.write(f"{i}. {event['Timestamp'].strftime('%Y-%m-%d %H:%M')}: ")
                f.write(f"{event['Storm_Surge']:.4f} m ({event['Direction']})\n")
        else:
            f.write("No extreme events detected\n")

    # Print summary statistics
    print("\nSTORM SURGE SUMMARY STATISTICS")
    print("=============================")
    for key, value in surge_stats.items():
        print(f"{key}: {value:.4f}")

    # Print top surge events
    if len(peak_events) > 0:
        print("\nTOP 5 EXTREME SURGE EVENTS")
        print("=========================")
        display_events = min(5, len(peak_events))
        for i in range(display_events):
            event = peak_events.iloc[i]
            print(f"{i+1}. {event['Timestamp'].strftime('%Y-%m-%d %H:%M')}: {event['Storm_Surge']:.4f} m ({event['Direction']})")

    print(f"\nAll storm surge data saved to {output_dir}/storm_surge_raw.csv")
    print(f"Storm surge statistics saved to {output_dir}/surge_statistics_raw.txt")

    return surge_df, surge_stats, peak_events

# Execute the analysis
if __name__ == "__main__":
    surge_df, surge_stats, peak_events = calculate_and_analyze_surge()

    print("\n==== EDUCATIONAL NOTES ====")
    print("Storm surge is the non-tidal component of sea level variation.")
    print("It's primarily caused by weather effects such as:")
    print("  - Low atmospheric pressure (which can raise water levels)")
    print("  - Wind pushing water toward or away from the coast")
    print("\nPositive surge means water level is higher than predicted by the tide alone.")
    print("Negative surge means water level is lower than predicted.")
    print("\nIn Script 4, we'll apply a low-pass filter to this raw surge signal to")
    print("isolate the meteorological component from high-frequency noise.")
