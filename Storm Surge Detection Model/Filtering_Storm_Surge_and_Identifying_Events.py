"""
# Script 4: Filtering Storm Surge and Identifying Events
# =====================================================
#
# This script performs the final step in our tidal harmonic analysis:
# filtering the raw storm surge to remove high-frequency noise and identify significant events.
#
# In this script, we:
# 1. Load the raw storm surge data from Script 3
# 2. Apply a Butterworth low-pass filter to separate meteorological signals from noise
# 3. Identify and characterize significant surge events
# 4. Create comprehensive visualizations of the filtered surge
# 5. Generate a final report summarizing the entire analysis
#
# The filtered surge provides a clearer picture of meteorologically-driven
# sea level variations that might impact coastal areas.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from scipy import signal
from datetime import datetime, timedelta
import os

# Create output directory for saving results
output_dir = './tidal_analysis_results'
os.makedirs(output_dir, exist_ok=True)

# Load the raw storm surge data from Script 3
def load_raw_surge_data():
    """Load the raw storm surge data produced by Script 3"""
    print("Loading raw storm surge data...")

    surge_file = f'{output_dir}/storm_surge_raw.csv'
    if not os.path.exists(surge_file):
        raise FileNotFoundError(f"Could not find {surge_file}. Run Script 3 first.")

    surge_df = pd.read_csv(surge_file)
    surge_df['Timestamp'] = pd.to_datetime(surge_df['Timestamp'])

    print(f"Loaded storm surge data with {len(surge_df)} data points")
    return surge_df

# Apply Butterworth filter to the raw storm surge
def apply_butterworth_filter(surge_df, cutoff_period=12, order=3):
    """
    Apply a Butterworth low-pass filter to the raw storm surge data

    Parameters:
    -----------
    surge_df : pandas.DataFrame
        DataFrame containing raw storm surge data
    cutoff_period : float, optional
        Cutoff period in hours (default: 12)
    order : int, optional
        Filter order (default: 3)

    Returns:
    --------
    pandas.DataFrame
        DataFrame with original and filtered surge data
    """
    print(f"Applying Butterworth low-pass filter (cutoff period: {cutoff_period} hours, order: {order})...")

    # Get the raw surge data
    raw_surge = surge_df['Storm_Surge'].values

    # Design Butterworth low-pass filter
    # Cutoff frequency is 1/cutoff_period (normalized by Nyquist frequency)
    cutoff_freq = 1/cutoff_period
    b, a = signal.butter(order, cutoff_freq, 'low', fs=1)  # fs=1 for hourly data

    # Apply the filter
    filtered_surge = signal.filtfilt(b, a, raw_surge)

    # Add filtered surge to the dataframe
    surge_df['Filtered_Surge'] = filtered_surge

    print("Filtering complete")
    return surge_df

# Function to explore different filter settings (educational)
def explore_filter_settings(surge_df):
    """
    Explore different filter settings to demonstrate their effect
    This is educational to show how filter parameters affect the result
    """
    print("Exploring different filter settings...")

    # Get the raw surge data
    raw_surge = surge_df['Storm_Surge'].values
    time_index = surge_df['Timestamp']

    # Try different filter settings
    cutoff_periods = [6, 12, 24, 48]  # hours
    orders = [2, 3, 5]  # filter order

    # Create subplots
    fig, axes = plt.subplots(len(orders), len(cutoff_periods), figsize=(18, 12), sharex=True, sharey=True)

    # For demonstration, use only a 14-day sample
    sample_slice = slice(0, 14*24)  # 14 days
    sample_time = time_index[sample_slice]
    sample_raw = raw_surge[sample_slice]

    # Apply filters with different settings
    for i, order in enumerate(orders):
        for j, period in enumerate(cutoff_periods):
            # Design filter
            cutoff_freq = 1/period
            b, a = signal.butter(order, cutoff_freq, 'low', fs=1)

            # Apply filter
            filtered = signal.filtfilt(b, a, sample_raw)

            # Plot
            ax = axes[i, j]
            ax.plot(sample_time, sample_raw, 'lightgrey', label='Raw', alpha=0.5)
            ax.plot(sample_time, filtered, 'b-', label='Filtered', linewidth=1.5)
            ax.set_title(f'Order: {order}, Period: {period}h')
            ax.grid(True, alpha=0.3)

            # Format x-axis
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))

            # Add correlation coefficient to quantify how well each filter preserves signal
            corr = np.corrcoef(sample_raw, filtered)[0, 1]
            ax.text(0.05, 0.90, f'Corr: {corr:.3f}', transform=ax.transAxes,
                   bbox=dict(facecolor='white', alpha=0.7))

    # Add common labels
    fig.text(0.5, 0.04, 'Date', ha='center', va='center', fontsize=14)
    fig.text(0.06, 0.5, 'Storm Surge (m)', ha='center', va='center',
             rotation='vertical', fontsize=14)

    plt.tight_layout()
    plt.savefig(f'{output_dir}/filter_comparison.png', dpi=300)
    plt.show()

    print("Filter exploration complete")

# Identify significant surge events
def identify_surge_events(surge_df, std_multiplier=2):
    """
    Identify significant surge events in the filtered data

    Parameters:
    -----------
    surge_df : pandas.DataFrame
        DataFrame containing filtered surge data
    std_multiplier : float, optional
        Multiple of standard deviation to use as threshold (default: 2)

    Returns:
    --------
    tuple
        Surge statistics and significant events DataFrame
    """
    print(f"Identifying significant surge events (threshold: {std_multiplier}σ)...")

    # Calculate statistics on filtered surge
    filtered_surge = surge_df['Filtered_Surge']
    surge_stats = {
        'Mean': np.mean(filtered_surge),
        'Std Dev': np.std(filtered_surge),
        'Min': np.min(filtered_surge),
        'Max': np.max(filtered_surge),
        'Abs Max': np.max(np.abs(filtered_surge))
    }

    # Define threshold based on standard deviation
    threshold = std_multiplier * surge_stats['Std Dev']

    # Identify significant events (exceeding threshold)
    significant_events = surge_df[np.abs(surge_df['Filtered_Surge']) > threshold].copy()

    # Group consecutive events
    if len(significant_events) > 0:
        # Add event group identifier
        significant_events['event_diff'] = significant_events['Timestamp'].diff().dt.total_seconds() / 3600
        significant_events['event_group'] = (significant_events['event_diff'] > 3).cumsum()

        # Find key characteristics of each event group
        event_groups = []
        for group_id, group in significant_events.groupby('event_group'):
            # Find peak value
            peak_idx = group['Filtered_Surge'].abs().idxmax()
            peak_row = group.loc[peak_idx].copy()

            # Calculate event duration
            start_time = group['Timestamp'].min()
            end_time = group['Timestamp'].max()
            duration_hours = (end_time - start_time).total_seconds() / 3600

            # Create event summary
            event = {
                'Start_Time': start_time,
                'End_Time': end_time,
                'Peak_Time': peak_row['Timestamp'],
                'Duration_Hours': duration_hours,
                'Peak_Surge': peak_row['Filtered_Surge'],
                'Direction': 'Positive' if peak_row['Filtered_Surge'] > 0 else 'Negative',
                'Event_Group': group_id
            }
            event_groups.append(event)

        # Create DataFrame of event summaries
        events_df = pd.DataFrame(event_groups)

        # Sort by absolute magnitude
        events_df = events_df.sort_values(by='Peak_Surge', key=abs, ascending=False)
    else:
        # Create empty DataFrame if no events found
        events_df = pd.DataFrame(columns=[
            'Start_Time', 'End_Time', 'Peak_Time', 'Duration_Hours',
            'Peak_Surge', 'Direction', 'Event_Group'
        ])

    print(f"Identified {len(events_df)} significant surge events")
    return surge_stats, events_df

# Enhanced visualization of filtered surge and events
def visualize_filtered_surge(surge_df, surge_stats, events_df):
    """Create comprehensive visualizations of the filtered surge and events"""
    print("Creating visualizations of filtered surge and events...")

    # Plot 1: Filtered vs Raw Surge (full time series)
    fig, ax = plt.subplots(figsize=(14, 7))
    ax.plot(surge_df['Timestamp'], surge_df['Storm_Surge'], color='lightgrey', label='Raw Surge', alpha=0.5, linewidth=0.5)
    ax.plot(surge_df['Timestamp'], surge_df['Filtered_Surge'], color='blue', label='Filtered Surge', linewidth=1.2)

    # Add a horizontal line at zero
    ax.axhline(y=0, color='red', linestyle='--', alpha=0.7)

    # Add threshold lines
    std_dev = surge_stats['Std Dev']
    ax.axhline(y=2*std_dev, color='orange', linestyle=':', alpha=0.7, label='+2σ Threshold')
    ax.axhline(y=-2*std_dev, color='orange', linestyle=':', alpha=0.7, label='-2σ Threshold')

    # Highlight significant events
    if len(events_df) > 0:
        for _, event in events_df.iterrows():
            color = 'red' if event['Direction'] == 'Positive' else 'purple'
            ax.plot(event['Peak_Time'], event['Peak_Surge'], 'o', color=color, markersize=8)

    # Format x-axis with date labels
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    fig.autofmt_xdate()

    plt.xlabel('Date')
    plt.ylabel('Storm Surge (m)')
    plt.title('Filtered Storm Surge with Significant Events')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(f'{output_dir}/filtered_surge_full.png', dpi=300)
    plt.show()

    # Plot 2: Close-up of top 3 surge events (if available)
    if len(events_df) >= 3:
        fig, axes = plt.subplots(3, 1, figsize=(14, 12), sharex=False)

        for i in range(3):
            event = events_df.iloc[i]

            # Define time window (1 day before and after peak)
            peak_time = event['Peak_Time']
            start_window = peak_time - timedelta(days=1)
            end_window = peak_time + timedelta(days=1)

            # Get data for this window
            window_data = surge_df[
                (surge_df['Timestamp'] >= start_window) &
                (surge_df['Timestamp'] <= end_window)
            ]

            # Plot
            ax = axes[i]
            ax.plot(window_data['Timestamp'], window_data['Storm_Surge'],
                   color='lightgrey', label='Raw Surge', alpha=0.5)
            ax.plot(window_data['Timestamp'], window_data['Filtered_Surge'],
                   color='blue', label='Filtered Surge', linewidth=1.5)

            # Add zero line and threshold
            ax.axhline(y=0, color='red', linestyle='--', alpha=0.7)
            ax.axhline(y=2*std_dev, color='orange', linestyle=':', alpha=0.5)
            ax.axhline(y=-2*std_dev, color='orange', linestyle=':', alpha=0.5)

            # Highlight peak
            color = 'red' if event['Direction'] == 'Positive' else 'purple'
            ax.plot(event['Peak_Time'], event['Peak_Surge'], 'o', color=color, markersize=10)

            # Format x-axis
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d %H:00'))
            ax.xaxis.set_major_locator(mdates.HourLocator(interval=6))

            # Add event details
            direction = event['Direction']
            magnitude = abs(event['Peak_Surge'])
            duration = event['Duration_Hours']

            ax.set_title(f'Event {i+1}: {direction} Surge of {magnitude:.3f}m on {peak_time.strftime("%Y-%m-%d %H:%M")}')
            ax.text(0.02, 0.85, f'Duration: {duration:.1f} hours', transform=ax.transAxes,
                   bbox=dict(facecolor='white', alpha=0.7))

            ax.grid(True, alpha=0.3)
            if i == 0:
                ax.legend()

        plt.tight_layout()
        plt.savefig(f'{output_dir}/top_surge_events.png', dpi=300)
        plt.show()

    # Plot 3: Histogram of filtered surge with normal distribution overlay
    plt.figure(figsize=(10, 6))

    # Histogram
    n, bins, patches = plt.hist(surge_df['Filtered_Surge'], bins=50,
                               color='skyblue', edgecolor='black', alpha=0.7,
                               density=True, label='Filtered Surge')

    # Fit normal distribution
    mu = surge_stats['Mean']
    sigma = surge_stats['Std Dev']
    x = np.linspace(mu - 4*sigma, mu + 4*sigma, 100)
    plt.plot(x, stats.norm.pdf(x, mu, sigma), 'r-', linewidth=2,
            label=f'Normal Distribution\n(μ={mu:.3f}, σ={sigma:.3f})')

    # Add vertical lines
    plt.axvline(x=0, color='black', linestyle='-', alpha=0.4)
    plt.axvline(x=2*std_dev, color='orange', linestyle='--', label='+2σ Threshold')
    plt.axvline(x=-2*std_dev, color='orange', linestyle='--')

    plt.xlabel('Filtered Storm Surge (m)')
    plt.ylabel('Probability Density')
    plt.title('Distribution of Filtered Storm Surge Values')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(f'{output_dir}/filtered_surge_distribution.png', dpi=300)
    plt.show()

    print("Visualizations complete")

# Generate a final comprehensive report
def generate_final_report(surge_df, surge_stats, events_df):
    """Generate a comprehensive final report of the entire analysis"""
    print("Generating final analysis report...")

    report_file = f'{output_dir}/final_analysis_report.txt'

    with open(report_file, 'w') as f:
        f.write("TIDAL HARMONIC ANALYSIS AND STORM SURGE REPORT\n")
        f.write("============================================\n\n")

        # Data summary
        f.write("DATA SUMMARY\n")
        f.write("-----------\n")
        start_date = surge_df['Timestamp'].min().strftime('%Y-%m-%d')
        end_date = surge_df['Timestamp'].max().strftime('%Y-%m-%d')
        duration_days = (surge_df['Timestamp'].max() - surge_df['Timestamp'].min()).days
        f.write(f"Time period: {start_date} to {end_date} ({duration_days} days)\n")
        f.write(f"Number of data points: {len(surge_df)}\n\n")

        # Filtered surge statistics
        f.write("FILTERED STORM SURGE STATISTICS\n")
        f.write("------------------------------\n")
        for key, value in surge_stats.items():
            f.write(f"{key}: {value:.4f} m\n")

        # Calculate additional statistics
        positive_surges = surge_df[surge_df['Filtered_Surge'] > 0]['Filtered_Surge']
        negative_surges = surge_df[surge_df['Filtered_Surge'] < 0]['Filtered_Surge']
        pct_positive = len(positive_surges) / len(surge_df) * 100
        pct_negative = len(negative_surges) / len(surge_df) * 100

        f.write(f"\nPositive surge percentage: {pct_positive:.1f}%\n")
        f.write(f"Negative surge percentage: {pct_negative:.1f}%\n")

        # Check for normality of distribution
        from scipy import stats
        _, p_value = stats.normaltest(surge_df['Filtered_Surge'].dropna())
        f.write(f"\nNormality test p-value: {p_value:.6f}")
        if p_value < 0.05:
            f.write(" (Distribution is not normal)\n\n")
        else:
            f.write(" (Distribution appears normal)\n\n")

        # Significant events
        f.write("SIGNIFICANT SURGE EVENTS (>2σ)\n")
        f.write("----------------------------\n")
        if len(events_df) > 0:
            for i, event in events_df.iterrows():
                if i >= 15:  # Limit to top 15 events
                    break

                # Calculate percent of maximum historic surge
                max_historic = surge_stats['Abs Max']
                percent_of_max = abs(event['Peak_Surge']) / max_historic * 100

                f.write(f"{i+1}. {event['Direction']} Surge on ")
                f.write(f"{event['Peak_Time'].strftime('%Y-%m-%d %H:%M')}\n")
                f.write(f"   Peak magnitude: {abs(event['Peak_Surge']):.4f} m ")
                f.write(f"({percent_of_max:.1f}% of historic maximum)\n")
                f.write(f"   Duration: {event['Duration_Hours']:.1f} hours\n")
                f.write(f"   Period: {event['Start_Time'].strftime('%Y-%m-%d %H:%M')} to ")
                f.write(f"{event['End_Time'].strftime('%Y-%m-%d %H:%M')}\n\n")
        else:
            f.write("No significant surge events detected\n\n")

        # Monthly statistics
        f.write("MONTHLY SURGE STATISTICS\n")
        f.write("----------------------\n")
        surge_df['Month'] = surge_df['Timestamp'].dt.month
        monthly_stats = surge_df.groupby('Month')['Filtered_Surge'].agg([
            'mean', 'std', 'min', 'max', 'count'
        ])

        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

        for i, month in enumerate(months, 1):
            if i in monthly_stats.index:
                stats = monthly_stats.loc[i]
                f.write(f"{month}: Mean={stats['mean']:.4f}m, ")
                f.write(f"StdDev={stats['std']:.4f}m, ")
                f.write(f"Min={stats['min']:.4f}m, ")
                f.write(f"Max={stats['max']:.4f}m, ")
                f.write(f"Count={int(stats['count'])}\n")

        # Conclusion
        f.write("\nCONCLUSION\n")
        f.write("----------\n")
        f.write("This analysis successfully separated the tidal and non-tidal components\n")
        f.write("of the sea level record. The filtered storm surge record shows the\n")
        f.write("meteorological influences on sea level after removing the\n")
        f.write("astronomical tidal signal.\n\n")

        # Most significant finding
        if len(events_df) > 0:
            max_event = events_df.iloc[0]
            f.write("The most significant surge event occurred on ")
            f.write(f"{max_event['Peak_Time'].strftime('%Y-%m-%d %H:%M')}, ")
            f.write(f"with a {max_event['Direction'].lower()} surge of {abs(max_event['Peak_Surge']):.4f} meters.\n")

    print(f"Final report saved to {report_file}")

# Main function to filter and analyze surge data
def filter_and_analyze_surge(cutoff_period=12, order=3, std_multiplier=2):
    """
    Main function to filter and analyze storm surge data

    Parameters:
    -----------
    cutoff_period : float, optional
        Cutoff period for the filter in hours (default: 12)
    order : int, optional
        Filter order (default: 3)
    std_multiplier : float, optional
        Multiple of standard deviation to use as event threshold (default: 2)
    """

    print(f"\n= Step 4: Filtering Storm Surge and Identifying Events =\n")

    # Load raw surge data from Script 3
    surge_df = load_raw_surge_data()

    # Demonstrate different filter settings (educational)
    explore_filter_settings(surge_df)

    # Apply Butterworth filter to the raw surge
    filtered_df = apply_butterworth_filter(surge_df, cutoff_period, order)

    # Identify significant surge events
    surge_stats, events_df = identify_surge_events(filtered_df, std_multiplier)

    # Create visualizations
    visualize_filtered_surge(filtered_df, surge_stats, events_df)

    # Save filtered surge data
    print("Saving filtered surge data...")
    filtered_df.to_csv(f'{output_dir}/filtered_surge.csv', index=False)

    # Save significant events
    if len(events_df) > 0:
        events_df.to_csv(f'{output_dir}/significant_surge_events.csv', index=False)

    # Generate comprehensive final report
    generate_final_report(filtered_df, surge_stats, events_df)

    # Print summary statistics
    print("\nFILTERED STORM SURGE SUMMARY STATISTICS")
    print("=====================================")
    for key, value in surge_stats.items():
        print(f"{key}: {value:.4f} m")

    # Print top surge events
    if len(events_df) > 0:
        print("\nTOP 5 SIGNIFICANT SURGE EVENTS")
        print("=============================")
        display_events = min(5, len(events_df))
        for i in range(display_events):
            event = events_df.iloc[i]
            print(f"{i+1}. {event['Peak_Time'].strftime('%Y-%m-%d %H:%M')}: ", end="")
            print(f"{event['Peak_Surge']:.4f}m {event['Direction']} surge ", end="")
            print(f"({event['Duration_Hours']:.1f} hours)")

    print(f"\nAll filtered surge data saved to {output_dir}/filtered_surge.csv")
    print(f"Final analysis report saved to {output_dir}/final_analysis_report.txt")

    return filtered_df, surge_stats, events_df

# Add utility function for creating correlation analysis with weather data
def correlate_with_weather(surge_df, weather_file):
    """
    Optional function to correlate surge with weather data if available

    Parameters:
    -----------
    surge_df : pandas.DataFrame
        DataFrame containing filtered surge data
    weather_file : str
        Path to CSV file with weather data (must have Timestamp column)
    """
    if os.path.exists(weather_file):
        print(f"Correlating surge with weather data from {weather_file}...")

        # Load weather data
        weather_df = pd.read_csv(weather_file)
        weather_df['Timestamp'] = pd.to_datetime(weather_df['Timestamp'])

        # Merge with surge data
        merged = pd.merge(surge_df, weather_df, on='Timestamp', how='inner')

        # Check which weather variables are available
        weather_vars = [col for col in merged.columns if col not in
                       ['Timestamp', 'Original_SSH', 'Predicted_SSH', 'Storm_Surge', 'Filtered_Surge']]

        # Calculate correlations
        corr_data = []
        for var in weather_vars:
            corr = merged['Filtered_Surge'].corr(merged[var])
            corr_data.append({'Variable': var, 'Correlation': corr})

        # Create correlation DataFrame
        corr_df = pd.DataFrame(corr_data).sort_values(by='Correlation', key=abs, ascending=False)

        # Save correlations
        corr_df.to_csv(f'{output_dir}/weather_correlations.csv', index=False)

        # Plot top correlations
        if len(corr_df) > 0:
            top_var = corr_df.iloc[0]['Variable']
            plt.figure(figsize=(10, 6))
            plt.scatter(merged[top_var], merged['Filtered_Surge'], alpha=0.5)
            plt.xlabel(top_var)
            plt.ylabel('Filtered Storm Surge (m)')
            plt.title(f'Correlation between Storm Surge and {top_var}')
            plt.grid(True, alpha=0.3)
            plt.tight_layout()
            plt.savefig(f'{output_dir}/surge_weather_correlation.png', dpi=300)
            plt.show()

        print(f"Weather correlation analysis saved to {output_dir}/weather_correlations.csv")
        return corr_df
    else:
        print("No weather data file provided or file not found.")
        return None

# Execute the analysis
if __name__ == "__main__":
    # Set filter parameters
    cutoff_period = 12  # hours (adjust based on your analysis needs)
    filter_order = 3    # typical value for Butterworth filter

    # Set event threshold
    std_multiplier = 2  # Events exceeding 2 standard deviations

    # Run the filtering and analysis
    filtered_df, surge_stats, events_df = filter_and_analyze_surge(
        cutoff_period=cutoff_period,
        order=filter_order,
        std_multiplier=std_multiplier
    )

    # If you have weather data, uncomment this line and provide the file path
    # weather_corr = correlate_with_weather(filtered_df, 'path_to_weather_data.csv')

    print("\n==== EDUCATIONAL NOTES ====")
    print("The Butterworth filter is a type of signal processing filter designed to have a")
    print("frequency response as flat as possible in the passband. It's used here to remove")
    print("high-frequency noise from the storm surge signal.")
    print("\nWhy filter the storm surge?")
    print("  - Removes measurement noise and high-frequency oscillations")
    print("  - Isolates meteorological effects, which typically occur on longer time scales")
    print("  - Makes it easier to identify significant surge events")
    print("\nSignificant surge events (exceeding 2 standard deviations) represent")
    print("periods when water levels were substantially higher or lower than")
    print("predicted by astronomical tides alone. These events often correspond")
    print("to strong weather systems affecting the area.")
    print("\nThis completes our four-step tidal harmonic analysis process")
