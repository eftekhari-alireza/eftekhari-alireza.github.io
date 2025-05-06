"""
# Enhanced Residual Visualization
# ==============================
#
# This script creates comprehensive educational visualizations of the storm surge residuals
# to help students understand the non-tidal components of sea level variation.
#
# Run this script after Step 3 (or Step 4 if you want filtered results too)
# It will create a series of specialized plots focusing on different aspects
# of the residuals to enhance understanding.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.gridspec as gridspec
from matplotlib.patches import Patch
import matplotlib.cm as cm
from scipy import stats
from datetime import datetime, timedelta
import os
import calendar

# Create output directory for saving results
output_dir = './tidal_analysis_results/residual_visualizations'
os.makedirs(output_dir, exist_ok=True)

# Function to load data from previous steps
def load_surge_data():
    """Load surge data from previous analysis steps"""
    print("Loading surge data...")

    # First try to find filtered data (from Step 4)
    filtered_path = './tidal_analysis_results/filtered_surge.csv'
    raw_path = './tidal_analysis_results/storm_surge_raw.csv'

    if os.path.exists(filtered_path):
        print(f"Found filtered surge data: {filtered_path}")
        surge_df = pd.read_csv(filtered_path)
        has_filtered = True
    elif os.path.exists(raw_path):
        print(f"Found raw surge data: {raw_path}")
        surge_df = pd.read_csv(raw_path)
        has_filtered = False
    else:
        raise FileNotFoundError("No surge data found. Run previous scripts first.")

    # Ensure timestamp is datetime
    surge_df['Timestamp'] = pd.to_datetime(surge_df['Timestamp'])

    # If we don't have a Month column, add it
    if 'Month' not in surge_df.columns:
        surge_df['Month'] = surge_df['Timestamp'].dt.month

    # Add more time columns for analysis
    surge_df['Day'] = surge_df['Timestamp'].dt.day
    surge_df['Hour'] = surge_df['Timestamp'].dt.hour
    surge_df['DayOfYear'] = surge_df['Timestamp'].dt.dayofyear
    surge_df['WeekOfYear'] = surge_df['Timestamp'].dt.isocalendar().week

    # If we only have raw data, create a placeholder filtered column
    if 'Filtered_Surge' not in surge_df.columns and not has_filtered:
        print("No filtered surge found, using raw surge for all visualizations")
        surge_df['Filtered_Surge'] = surge_df['Storm_Surge']

    print(f"Loaded {len(surge_df)} data points")
    return surge_df, has_filtered

# 1. Create a comprehensive time series visualization with annotations
def create_annotated_timeseries(surge_df, has_filtered=True):
    """Create a comprehensive annotated time series of the residuals"""
    print("Creating annotated time series visualization...")

    # Set up the figure
    fig, ax = plt.subplots(figsize=(15, 8))

    # Plot raw surge
    raw_line = ax.plot(surge_df['Timestamp'], surge_df['Storm_Surge'],
                      color='green', alpha=0.6, linewidth=1,
                      label='Raw Storm Surge')

    # Plot filtered surge if available
    if has_filtered:
        filtered_line = ax.plot(surge_df['Timestamp'], surge_df['Filtered_Surge'],
                               color='blue', linewidth=1.5,
                               label='Filtered Storm Surge')

    # Calculate statistics
    raw_mean = surge_df['Storm_Surge'].mean()
    raw_std = surge_df['Storm_Surge'].std()

    # Add horizontal lines
    ax.axhline(y=0, color='red', linestyle='-', alpha=0.5, linewidth=1.5, label='Zero Line')
    ax.axhline(y=raw_mean, color='black', linestyle='--', alpha=0.5, linewidth=1, label='Mean')
    ax.axhline(y=raw_mean + 2*raw_std, color='orange', linestyle=':', alpha=0.7, linewidth=1.5, label='+2σ')
    ax.axhline(y=raw_mean - 2*raw_std, color='orange', linestyle=':', alpha=0.7, linewidth=1.5, label='-2σ')

    # Format x-axis
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    fig.autofmt_xdate()

    # Add annotations for seasonal transitions
    seasons = [
        {'name': 'Winter', 'date': '2022-01-01', 'y': 0.6, 'color': 'darkblue'},
        {'name': 'Spring', 'date': '2022-03-20', 'y': 0.6, 'color': 'green'},
        {'name': 'Summer', 'date': '2022-06-21', 'y': 0.6, 'color': 'red'},
        {'name': 'Fall', 'date': '2022-09-22', 'y': 0.6, 'color': 'darkorange'},
        {'name': 'Winter', 'date': '2022-12-21', 'y': 0.6, 'color': 'darkblue'}
    ]

    for season in seasons:
        season_date = pd.to_datetime(season['date'])
        ax.axvline(x=season_date, color=season['color'], linestyle='-', alpha=0.3)
        ax.text(season_date, season['y'], season['name'],
               ha='center', va='center', rotation=90,
               bbox=dict(facecolor='white', alpha=0.8))

    # Find extreme events
    threshold = raw_mean + 2*raw_std
    neg_threshold = raw_mean - 2*raw_std

    # Identify events exceeding 2 standard deviations
    if has_filtered:
        extreme_metric = 'Filtered_Surge'
    else:
        extreme_metric = 'Storm_Surge'

    pos_extremes = surge_df[surge_df[extreme_metric] > threshold].copy()
    neg_extremes = surge_df[surge_df[extreme_metric] < neg_threshold].copy()

    # Group into events
    if len(pos_extremes) > 0:
        pos_extremes['event_diff'] = pos_extremes['Timestamp'].diff().dt.total_seconds() / 3600
        pos_extremes['event_group'] = (pos_extremes['event_diff'] > 3).cumsum()

        # Find the peak of each positive event
        pos_peaks = []
        for group in pos_extremes['event_group'].unique():
            group_data = pos_extremes[pos_extremes['event_group'] == group]
            peak_idx = group_data[extreme_metric].idxmax()
            pos_peaks.append(pos_extremes.loc[peak_idx])
    else:
        pos_peaks = []

    if len(neg_extremes) > 0:
        neg_extremes['event_diff'] = neg_extremes['Timestamp'].diff().dt.total_seconds() / 3600
        neg_extremes['event_group'] = (neg_extremes['event_diff'] > 3).cumsum()

        # Find the peak of each negative event
        neg_peaks = []
        for group in neg_extremes['event_group'].unique():
            group_data = neg_extremes[neg_extremes['event_group'] == group]
            peak_idx = group_data[extreme_metric].idxmin()
            neg_peaks.append(neg_extremes.loc[peak_idx])
    else:
        neg_peaks = []

    # Plot the peaks
    for peak in pos_peaks:
        ax.plot(peak['Timestamp'], peak[extreme_metric], 'o', color='red', markersize=8)

    for peak in neg_peaks:
        ax.plot(peak['Timestamp'], peak[extreme_metric], 'o', color='purple', markersize=8)

    # Annotate the top 5 most extreme events
    all_extremes = pos_peaks + neg_peaks
    if all_extremes:
        if extreme_metric == 'Filtered_Surge':
            sorted_extremes = sorted(all_extremes, key=lambda x: abs(x['Filtered_Surge']), reverse=True)
        else:
            sorted_extremes = sorted(all_extremes, key=lambda x: abs(x['Storm_Surge']), reverse=True)

        for i, extreme in enumerate(sorted_extremes[:5]):
            if extreme_metric == 'Filtered_Surge':
                value = extreme['Filtered_Surge']
            else:
                value = extreme['Storm_Surge']

            # Determine if it's a positive or negative event
            if value > 0:
                y_offset = 0.05
                color = 'red'
            else:
                y_offset = -0.05
                color = 'purple'

            # Add an annotation arrow
            ax.annotate(f"{extreme['Timestamp'].strftime('%Y-%m-%d')}\n{value:.2f}m",
                       xy=(extreme['Timestamp'], value),
                       xytext=(extreme['Timestamp'], value + y_offset),
                       ha='center', va='center',
                       bbox=dict(boxstyle="round,pad=0.3", fc='white', alpha=0.8),
                       arrowprops=dict(arrowstyle="->", connectionstyle="arc3", color=color),
                       fontsize=9)

    # Add legend and labels
    ax.legend(loc='upper right')
    ax.set_xlabel('Date')
    ax.set_ylabel('Storm Surge (m)')
    ax.set_title('Annotated Storm Surge Time Series', fontsize=14)
    ax.grid(True, alpha=0.3)

    # Add explanatory text
    fig.text(0.02, 0.02,
             "Storm surge represents the non-tidal component of sea level variation.\n"
             "Positive values indicate water levels higher than predicted by tides alone,\n"
             "while negative values indicate lower than predicted levels.",
             fontsize=10, ha='left', va='bottom',
             bbox=dict(facecolor='white', alpha=0.8))

    plt.tight_layout()
    plt.savefig(f'{output_dir}/annotated_storm_surge.png', dpi=300)
    plt.show()
    print("Annotated time series created")

# 2. Create a seasonal analysis visualization
def create_seasonal_analysis(surge_df, has_filtered=True):
    """Create a comprehensive seasonal analysis of the residuals"""
    print("Creating seasonal analysis visualization...")

    # Determine which surge metric to use
    surge_metric = 'Filtered_Surge' if has_filtered else 'Storm_Surge'

    # Create a figure with 3 subplots: monthly, daily pattern, hourly pattern
    fig = plt.figure(figsize=(15, 12))
    gs = gridspec.GridSpec(2, 2, height_ratios=[1.5, 1])

    # 1. Monthly box plot
    ax1 = fig.add_subplot(gs[0, :])

    # Prepare monthly data
    monthly_data = []
    month_names = []

    for month in range(1, 13):
        monthly_data.append(surge_df[surge_df['Month'] == month][surge_metric])
        month_names.append(calendar.month_abbr[month])

    # Create box plot
    ax1.boxplot(monthly_data,
               patch_artist=True,
               boxprops=dict(facecolor='lightblue', alpha=0.8),
               medianprops=dict(color='red'))

    # Calculate and plot monthly means
    monthly_means = [data.mean() for data in monthly_data]
    ax1.plot(range(1, 13), monthly_means, 'ro-', linewidth=2, label='Monthly Mean')

    # Add zero line
    ax1.axhline(y=0, color='black', linestyle='-', alpha=0.3)

    # Add season bands
    ax1.axvspan(0.5, 3.5, alpha=0.1, color='blue', label='Winter')     # Dec-Feb
    ax1.axvspan(3.5, 6.5, alpha=0.1, color='green', label='Spring')    # Mar-May
    ax1.axvspan(6.5, 9.5, alpha=0.1, color='red', label='Summer')      # Jun-Aug
    ax1.axvspan(9.5, 12.5, alpha=0.1, color='orange', label='Fall')    # Sep-Nov

    # Set labels and title
    ax1.set_xlabel('Month')
    ax1.set_ylabel('Storm Surge (m)')
    ax1.set_title('Seasonal Pattern of Storm Surge', fontsize=14)
    ax1.set_xticks(range(1, 13))
    ax1.set_xticklabels(month_names)
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # 2. Day of month analysis
    ax2 = fig.add_subplot(gs[1, 0])

    # Group by day of month
    surge_df['Day'] = surge_df['Timestamp'].dt.day
    daily_means = surge_df.groupby('Day')[surge_metric].mean()

    # Plot
    ax2.plot(daily_means.index, daily_means.values, 'bo-', alpha=0.7)
    ax2.axhline(y=0, color='red', linestyle='--', alpha=0.3)
    ax2.set_xlabel('Day of Month')
    ax2.set_ylabel('Average Storm Surge (m)')
    ax2.set_title('Average Storm Surge by Day of Month', fontsize=12)
    ax2.grid(True, alpha=0.3)

    # 3. Hourly analysis
    ax3 = fig.add_subplot(gs[1, 1])

    # Group by hour
    hourly_means = surge_df.groupby('Hour')[surge_metric].mean()

    # Plot
    ax3.plot(hourly_means.index, hourly_means.values, 'go-', alpha=0.7)
    ax3.axhline(y=0, color='red', linestyle='--', alpha=0.3)
    ax3.set_xlabel('Hour of Day')
    ax3.set_ylabel('Average Storm Surge (m)')
    ax3.set_title('Average Storm Surge by Hour of Day', fontsize=12)
    ax3.set_xticks(range(0, 24, 2))
    ax3.grid(True, alpha=0.3)

    # Add explanatory text
    fig.text(0.02, 0.02,
             f"This analysis shows how storm surge varies across different time scales.\n"
             f"The monthly pattern often relates to seasonal weather patterns, while daily and hourly\n"
             f"patterns may reveal tidal constituents not captured in the harmonic analysis.",
             fontsize=10, ha='left', va='bottom',
             bbox=dict(facecolor='white', alpha=0.8))

    plt.tight_layout()
    plt.savefig(f'{output_dir}/seasonal_analysis.png', dpi=300)
    plt.show()
    print("Seasonal analysis created")

# 3. Create a frequency analysis visualization
def create_frequency_analysis(surge_df, has_filtered=True):
    """Create a frequency analysis of the residuals"""
    print("Creating frequency analysis visualization...")

    # Determine which surge metrics to use
    raw_metric = 'Storm_Surge'
    filtered_metric = 'Filtered_Surge' if has_filtered else 'Storm_Surge'

    fig, axes = plt.subplots(2, 1, figsize=(14, 12))

    # 1. Histogram and distribution
    ax1 = axes[0]

    # Calculate statistics
    raw_mean = surge_df[raw_metric].mean()
    raw_std = surge_df[raw_metric].std()

    if has_filtered:
        filtered_mean = surge_df[filtered_metric].mean()
        filtered_std = surge_df[filtered_metric].std()

    # Create histograms
    bins = np.linspace(raw_mean - 4*raw_std, raw_mean + 4*raw_std, 50)

    # Raw surge histogram
    ax1.hist(surge_df[raw_metric], bins=bins, alpha=0.4, color='green',
             density=True, label=f'Raw Storm Surge (σ={raw_std:.3f}m)')

    # Filtered surge histogram (if available)
    if has_filtered and filtered_metric != raw_metric:
        ax1.hist(surge_df[filtered_metric], bins=bins, alpha=0.4, color='blue',
                density=True, label=f'Filtered Storm Surge (σ={filtered_std:.3f}m)')

    # Add normal distribution curves
    x = np.linspace(raw_mean - 4*raw_std, raw_mean + 4*raw_std, 100)
    raw_pdf = stats.norm.pdf(x, raw_mean, raw_std)
    ax1.plot(x, raw_pdf, 'g-', linewidth=2, alpha=0.7, label='Normal Distribution (Raw)')

    if has_filtered and filtered_metric != raw_metric:
        filtered_pdf = stats.norm.pdf(x, filtered_mean, filtered_std)
        ax1.plot(x, filtered_pdf, 'b-', linewidth=2, alpha=0.7, label='Normal Distribution (Filtered)')

    # Add vertical lines for thresholds
    ax1.axvline(x=raw_mean + 2*raw_std, color='orange', linestyle='--', label='+2σ Threshold')
    ax1.axvline(x=raw_mean - 2*raw_std, color='orange', linestyle='--')

    # Set labels and title
    ax1.set_xlabel('Storm Surge (m)')
    ax1.set_ylabel('Probability Density')
    ax1.set_title('Distribution of Storm Surge Values', fontsize=14)
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # 2. Quantile-Quantile Plot
    ax2 = axes[1]

    # Create Q-Q plot for raw surge
    stats.probplot(surge_df[raw_metric], dist="norm", plot=ax2)

    # Set labels and title
    ax2.set_xlabel('Theoretical Quantiles')
    ax2.set_ylabel('Sample Quantiles')
    ax2.set_title('Q-Q Plot of Storm Surge (Tests for Normality)', fontsize=14)
    ax2.grid(True, alpha=0.3)

    # Add annotations
    # Get the normality test p-value
    _, p_value = stats.normaltest(surge_df[raw_metric].dropna())
    normality_result = "Normal" if p_value > 0.05 else "Non-normal"

    # Add text about normality
    ax2.text(0.02, 0.95,
             f"Distribution is {normality_result} (p={p_value:.6f})\n"
             f"Deviation from the diagonal line indicates non-normality.\n"
             f"Storm surge typically shows 'heavy tails', meaning\n"
             f"extreme events occur more frequently than a normal distribution would predict.",
             transform=ax2.transAxes,
             fontsize=10, ha='left', va='top',
             bbox=dict(facecolor='white', alpha=0.8))

    plt.tight_layout()
    plt.savefig(f'{output_dir}/frequency_analysis.png', dpi=300)
    plt.show()
    print("Frequency analysis created")

# 4. Create a raw vs. filtered comparison
def create_filtering_comparison(surge_df, has_filtered=True):
    """Create a visualization showing how filtering affects the residual"""
    print("Creating filtering comparison visualization...")

    if not has_filtered:
        print("No filtered data available, skipping this visualization")
        return

    # Set up the figure - we'll show 3 different time windows
    fig, axes = plt.subplots(3, 1, figsize=(15, 15))

    # Time windows to display (full year, month, week)
    windows = [
        {'name': 'Full Year', 'days': 365, 'title': 'Full Year Comparison'},
        {'name': 'One Month', 'days': 30, 'title': 'One Month Comparison (January)'},
        {'name': 'One Week', 'days': 7, 'title': 'One Week Comparison (January 1-7)'}
    ]

    # For each time window
    for i, window in enumerate(windows):
        ax = axes[i]

        # Create slice for this window
        start_date = pd.to_datetime('2022-01-01')
        end_date = start_date + pd.Timedelta(days=window['days'])
        mask = (surge_df['Timestamp'] >= start_date) & (surge_df['Timestamp'] < end_date)
        window_data = surge_df.loc[mask]

        # Plot raw and filtered surge
        ax.plot(window_data['Timestamp'], window_data['Storm_Surge'],
               color='green', alpha=0.6, linewidth=1,
               label='Raw Storm Surge')

        ax.plot(window_data['Timestamp'], window_data['Filtered_Surge'],
               color='blue', linewidth=1.5,
               label='Filtered Storm Surge')

        # Calculate the difference between raw and filtered
        window_data['Difference'] = window_data['Storm_Surge'] - window_data['Filtered_Surge']

        # Plot the difference
        ax.plot(window_data['Timestamp'], window_data['Difference'],
               color='red', alpha=0.4, linewidth=1,
               label='Difference (Raw - Filtered)')

        # Add zero line
        ax.axhline(y=0, color='black', linestyle='-', alpha=0.5)

        # Format axis
        if window['name'] == 'Full Year':
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
            ax.xaxis.set_major_locator(mdates.MonthLocator())
        elif window['name'] == 'One Month':
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
            ax.xaxis.set_major_locator(mdates.WeekdayLocator())
        else:
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:00'))
            ax.xaxis.set_major_locator(mdates.DayLocator())

        # Set labels and title
        ax.set_xlabel('Date')
        ax.set_ylabel('Storm Surge (m)')
        ax.set_title(window['title'], fontsize=12)
        ax.legend()
        ax.grid(True, alpha=0.3)

    # Add explanatory text
    fig.text(0.02, 0.01,
             "This comparison shows how filtering affects the storm surge signal.\n"
             "The filter removes high-frequency oscillations (red) while preserving the\n"
             "underlying meteorological signal. Note how the detail level changes at different time scales.",
             fontsize=10, ha='left', va='bottom',
             bbox=dict(facecolor='white', alpha=0.8))

    fig.autofmt_xdate()
    plt.tight_layout()
    plt.savefig(f'{output_dir}/filtering_comparison.png', dpi=300)
    plt.show()
    print("Filtering comparison created")

# 5. Create a comprehensive educational summary plot
def create_educational_summary(surge_df, has_filtered=True):
    """Create a comprehensive educational summary of residual analysis"""
    print("Creating educational summary visualization...")

    # Determine which metric to use
    surge_metric = 'Filtered_Surge' if has_filtered else 'Storm_Surge'

    # Create a figure with multiple panels
    fig = plt.figure(figsize=(15, 15))

    # Define a custom grid layout
    gs = gridspec.GridSpec(3, 3, height_ratios=[1.5, 1, 1])

    # 1. Main time series plot (spans full width)
    ax_main = fig.add_subplot(gs[0, :])

    # Plot the surge
    ax_main.plot(surge_df['Timestamp'], surge_df[surge_metric],
                color='blue', linewidth=1, alpha=0.8)

    # Add zero line and threshold
    mean = surge_df[surge_metric].mean()
    std = surge_df[surge_metric].std()
    ax_main.axhline(y=0, color='black', linestyle='-', alpha=0.5)
    ax_main.axhline(y=mean + 2*std, color='red', linestyle='--', alpha=0.5, label='+2σ')
    ax_main.axhline(y=mean - 2*std, color='red', linestyle='--', alpha=0.5, label='-2σ')

    # Format x-axis
    ax_main.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    ax_main.xaxis.set_major_locator(mdates.MonthLocator())

    # Set labels and title
    ax_main.set_xlabel('Date')
    ax_main.set_ylabel('Storm Surge (m)')
    ax_main.set_title('Storm Surge Time Series', fontsize=14)
    ax_main.legend()
    ax_main.grid(True, alpha=0.3)

    # 2. Monthly heatmap
    ax_heatmap = fig.add_subplot(gs[1, 0:2])

    # Create a pivot table with months and days
    surge_df['Day'] = surge_df['Timestamp'].dt.day
    monthly_pivot = surge_df.pivot_table(
        index='Month',
        columns='Day',
        values=surge_metric,
        aggfunc='mean'
    )

    # Create heatmap
    im = ax_heatmap.imshow(monthly_pivot, cmap='coolwarm', aspect='auto',
                          vmin=-0.3, vmax=0.3)

    # Add colorbar
    cbar = fig.colorbar(im, ax=ax_heatmap)
    cbar.set_label('Storm Surge (m)')

    # Format axes
    ax_heatmap.set_yticks(range(12))
    ax_heatmap.set_yticklabels([calendar.month_abbr[i+1] for i in range(12)])
    ax_heatmap.set_xticks(range(0, 31, 5))
    ax_heatmap.set_xticklabels(range(1, 32, 5))

    # Set labels and title
    ax_heatmap.set_xlabel('Day of Month')
    ax_heatmap.set_ylabel('Month')
    ax_heatmap.set_title('Monthly Pattern of Storm Surge', fontsize=12)

    # 3. Distribution histogram
    ax_hist = fig.add_subplot(gs[1, 2])

    # Create histogram
    ax_hist.hist(surge_df[surge_metric], bins=30, color='skyblue',
                edgecolor='black', alpha=0.7)

    # Add vertical lines
    ax_hist.axvline(x=0, color='black', linestyle='-', alpha=0.5)
    ax_hist.axvline(x=mean + 2*std, color='red', linestyle='--', alpha=0.5)
    ax_hist.axvline(x=mean - 2*std, color='red', linestyle='--', alpha=0.5)

    # Set labels and title
    ax_hist.set_xlabel('Storm Surge (m)')
    ax_hist.set_ylabel('Frequency')
    ax_hist.set_title('Distribution of Storm Surge', fontsize=12)
    ax_hist.grid(True, alpha=0.3)

    # 4. Weekly pattern
    ax_weekly = fig.add_subplot(gs[2, 0])

    # Add day of week
    surge_df['DayOfWeek'] = surge_df['Timestamp'].dt.dayofweek
    weekly_means = surge_df.groupby('DayOfWeek')[surge_metric].mean()

    # Plot
    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    ax_weekly.bar(days, weekly_means.values, color='lightgreen')
    ax_weekly.axhline(y=0, color='red', linestyle='--', alpha=0.5)

    # Set labels and title
    ax_weekly.set_xlabel('Day of Week')
    ax_weekly.set_ylabel('Average Storm Surge (m)')
    ax_weekly.set_title('Weekly Pattern', fontsize=12)
    ax_weekly.grid(True, alpha=0.3)

    # 5. Top events table
    ax_table = fig.add_subplot(gs[2, 1:])

    # Find top events
    threshold = mean + 2*std

    # Identify events exceeding 2 standard deviations
    extremes = surge_df[np.abs(surge_df[surge_metric] - mean) > 2*std].copy()

    if len(extremes) > 0:
        # Group into events
        extremes['event_diff'] = extremes['Timestamp'].diff().dt.total_seconds() / 3600
        extremes['event_group'] = (extremes['event_diff'] > 3).cumsum()

        # Find the peak of each event
        peaks = []
        for group in extremes['event_group'].unique():
            group_data = extremes[extremes['event_group'] == group]

            if any(group_data[surge_metric] > mean):  # Positive event
                peak_idx = group_data[surge_metric].idxmax()
                direction = 'Positive'
            else:  # Negative event
                peak_idx = group_data[surge_metric].idxmin()
                direction = 'Negative'

            # Calculate duration
            duration = (group_data['Timestamp'].max() - group_data['Timestamp'].min()).total_seconds() / 3600

            peaks.append({
                'Timestamp': extremes.loc[peak_idx, 'Timestamp'],
                'Surge': extremes.loc[peak_idx, surge_metric],
                'Direction': direction,
                'Duration': duration
            })

        # Sort peaks by absolute magnitude
        peaks.sort(key=lambda x: abs(x['Surge']), reverse=True)

        # Create table data
        table_data = []
        for i, peak in enumerate(peaks[:8]):  # Show top 8 events
            date_str = peak['Timestamp'].strftime('%Y-%m-%d')
            surge_str = f"{peak['Surge']:.3f} m"
            dir_str = peak['Direction']
            dur_str = f"{peak['Duration']:.1f} hr"

            table_data.append([i+1, date_str, surge_str, dir_str, dur_str])

        # Create table
        table = ax_table.table(
            cellText=table_data,
            colLabels=['Rank', 'Date', 'Peak Surge', 'Direction', 'Duration'],
            loc='center',
            cellLoc='center'
        )

        # Set table properties
        table.auto_set_font_size(False)
        table.set_fontsize(10)
        table.scale(1, 1.5)
        for key, cell in table._cells.items():
            if key[0] == 0:  # Header
                cell.set_facecolor('lightgrey')
    else:
        ax_table.text(0.5, 0.5, "No significant events found",
                     ha='center', va='center', fontsize=12)

    # Remove axes for table
    ax_table.axis('off')
    ax_table.set_title('Top Storm Surge Events', fontsize=12)

    # Add educational text
    fig.text(0.5, 0.01,
             "EDUCATIONAL SUMMARY: STORM SURGE ANALYSIS\n\n"
             "Storm surge is the non-tidal component of sea level variation, primarily caused by:\n"
             "• Atmospheric pressure changes (low pressure = higher water)\n"
             "• Wind forcing (wind pushing water toward or away from coast)\n"
             "• Ocean circulation patterns\n\n"
             "Analysis of storm surge patterns helps identify meteorological influences\n"
             "and improve coastal hazard predictions.",
             fontsize=12, ha='center', va='bottom',
             bbox=dict(facecolor='white', alpha=0.9, boxstyle="round,pad=0.5"))

    plt.tight_layout(rect=[0, 0.05, 1, 1])
    plt.savefig(f'{output_dir}/educational_summary.png', dpi=300)
    plt.show()
    print("Educational summary created")

# Main function to run all visualizations
def create_residual_visualizations():
    """Main function to create comprehensive residual visualizations"""

    print("\n= Enhanced Residual Visualization =\n")

    # Load data
    surge_df, has_filtered = load_surge_data()

    # Create visualizations
    create_annotated_timeseries(surge_df, has_filtered)
    create_seasonal_analysis(surge_df, has_filtered)
    create_frequency_analysis(surge_df, has_filtered)

    if has_filtered:
        create_filtering_comparison(surge_df, has_filtered)

    create_educational_summary(surge_df, has_filtered)

    print("\nAll visualizations saved to:", output_dir)
    print("\nThese visualizations provide multiple perspectives on the residual data,")
    print("highlighting seasonal patterns, extreme events, frequency distributions,")
    print("and filtering effects. They are designed to enhance understanding of")
    print("the non-tidal components of sea level variation.")

# Run the visualization script
if __name__ == "__main__":
    create_residual_visualizations()
