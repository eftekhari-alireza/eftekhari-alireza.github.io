"""
# Supplementary Analysis: Threshold Selection in Storm Surge Identification
# =========================================================================
#
# This script demonstrates how different thresholds and identification methods
# affect storm surge event detection - a critical educational component.
#
# The script:
# 1. Loads both raw and filtered surge data from previous analyses
# 2. Applies multiple threshold levels (1σ, 1.5σ, 2σ, 2.5σ, 3σ)
# 3. Identifies events using different criteria
# 4. Creates educational visualizations showing the impact of these choices
# 5. Generates comparison statistics for discussion
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
import os

# Create output directory for saving results
output_dir = './tidal_analysis_results/threshold_analysis'
os.makedirs(output_dir, exist_ok=True)

# Function to load surge data (uses previous analysis results)
def load_surge_data():
    """Load surge data from previous analysis steps"""
    print("Loading surge data...")

    # Try to load filtered surge data first
    filtered_file = './tidal_analysis_results/filtered_surge.csv'
    if os.path.exists(filtered_file):
        surge_df = pd.read_csv(filtered_file)
        has_filtered = True
    else:
        # If filtered data not available, use raw surge
        raw_file = './tidal_analysis_results/storm_surge_raw.csv'
        if not os.path.exists(raw_file):
            raise FileNotFoundError("No surge data found. Run previous analysis scripts first.")
        surge_df = pd.read_csv(raw_file)
        # Create a placeholder filtered surge column if it doesn't exist
        if 'Filtered_Surge' not in surge_df.columns:
            surge_df['Filtered_Surge'] = surge_df['Storm_Surge']
        has_filtered = False

    # Ensure timestamp is datetime
    surge_df['Timestamp'] = pd.to_datetime(surge_df['Timestamp'])

    print(f"Loaded {len(surge_df)} data points")
    return surge_df, has_filtered

# Function to identify events using different thresholds and methods
def identify_events_with_thresholds(surge_df, threshold_factors=[1.0, 1.5, 2.0, 2.5, 3.0],
                                   min_durations=[1, 3, 6], use_filtered=True):
    """
    Identify surge events using different threshold levels and duration requirements

    Parameters:
    -----------
    surge_df : pandas.DataFrame
        DataFrame containing surge data
    threshold_factors : list, optional
        List of standard deviation multiples to use as thresholds
    min_durations : list, optional
        List of minimum durations (in hours) required for an event
    use_filtered : bool, optional
        Whether to use filtered or raw surge data

    Returns:
    --------
    dict
        Dictionary of event information for each threshold and duration
    """
    print("Identifying events with different thresholds...")

    # Select which surge data to use
    surge_column = 'Filtered_Surge' if use_filtered else 'Storm_Surge'
    surge_values = surge_df[surge_column].values

    # Calculate statistics
    surge_mean = np.mean(surge_values)
    surge_std = np.std(surge_values)

    # Store results
    results = {}

    # Process each threshold factor
    for factor in threshold_factors:
        threshold = factor * surge_std

        # Create key for this threshold
        factor_key = f"{factor:.1f}σ"
        results[factor_key] = {
            'threshold_value': threshold,
            'durations': {}
        }

        # Identify exceedances (both positive and negative)
        exceedances = surge_df[np.abs(surge_df[surge_column] - surge_mean) > threshold].copy()

        # For each minimum duration
        for min_duration in min_durations:
            # Group consecutive exceedances
            if len(exceedances) > 0:
                # Add event group identifier
                exceedances['event_diff'] = exceedances['Timestamp'].diff().dt.total_seconds() / 3600
                exceedances['event_group'] = (exceedances['event_diff'] > 3).cumsum()

                # Find characteristics of each event group
                event_groups = []
                for group_id, group in exceedances.groupby('event_group'):
                    # Only include events that meet minimum duration
                    duration_hours = (group['Timestamp'].max() - group['Timestamp'].min()).total_seconds() / 3600

                    if duration_hours >= min_duration:
                        # Find peak value
                        peak_idx = group[surge_column].abs().idxmax()
                        peak_row = group.loc[peak_idx].copy()

                        # Create event summary
                        event = {
                            'Start_Time': group['Timestamp'].min(),
                            'End_Time': group['Timestamp'].max(),
                            'Peak_Time': peak_row['Timestamp'],
                            'Duration_Hours': duration_hours,
                            'Peak_Surge': peak_row[surge_column],
                            'Direction': 'Positive' if peak_row[surge_column] > surge_mean else 'Negative',
                            'Event_Group': group_id
                        }
                        event_groups.append(event)

                # Create DataFrame of event summaries
                if event_groups:
                    events_df = pd.DataFrame(event_groups)
                    # Sort by absolute magnitude
                    events_df = events_df.sort_values(by='Peak_Surge', key=abs, ascending=False)
                else:
                    # Create empty DataFrame if no events found
                    events_df = pd.DataFrame(columns=[
                        'Start_Time', 'End_Time', 'Peak_Time', 'Duration_Hours',
                        'Peak_Surge', 'Direction', 'Event_Group'
                    ])
            else:
                # Create empty DataFrame if no events found
                events_df = pd.DataFrame(columns=[
                    'Start_Time', 'End_Time', 'Peak_Time', 'Duration_Hours',
                    'Peak_Surge', 'Direction', 'Event_Group'
                ])

            # Store in results
            results[factor_key]['durations'][f"{min_duration}h"] = {
                'events_df': events_df,
                'count': len(events_df),
                'pos_count': len(events_df[events_df['Direction'] == 'Positive']),
                'neg_count': len(events_df[events_df['Direction'] == 'Negative'])
            }

    print("Event identification complete")
    return results, surge_mean, surge_std

# Function to create comparative visualization of different thresholds
def create_threshold_comparison_plots(surge_df, results, surge_mean, surge_std, use_filtered=True):
    """Create visualizations showing how different thresholds affect event identification"""
    print("Creating threshold comparison visualizations...")

    # Select which surge data to use
    surge_column = 'Filtered_Surge' if use_filtered else 'Storm_Surge'
    data_type = 'Filtered' if use_filtered else 'Raw'

    # Create bar chart showing number of events by threshold and duration
    plt.figure(figsize=(14, 8))

    # Extract data for plotting
    thresholds = list(results.keys())
    durations = list(results[thresholds[0]]['durations'].keys())

    # Set up bar positions
    bar_width = 0.25
    r1 = np.arange(len(thresholds))
    r2 = [x + bar_width for x in r1]
    r3 = [x + bar_width for x in r2]

    # Plot bars for each duration
    for i, duration in enumerate([durations[0], durations[1], durations[2]]):
        event_counts = [results[t]['durations'][duration]['count'] for t in thresholds]
        positions = [r1, r2, r3][i]
        plt.bar(positions, event_counts, width=bar_width,
                label=f'Min Duration: {duration}')

    # Add labels and legend
    plt.xlabel('Threshold Level')
    plt.ylabel('Number of Events')
    plt.title(f'Number of {data_type} Surge Events by Threshold and Minimum Duration')
    plt.xticks([r + bar_width for r in range(len(thresholds))], thresholds)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(f'{output_dir}/{data_type.lower()}_event_count_comparison.png', dpi=300)
    plt.close()

    # Create plots for each threshold level showing the events
    for threshold in thresholds:
        threshold_value = results[threshold]['threshold_value']

        # Create figure with subplots for each duration requirement
        fig, axes = plt.subplots(len(durations), 1, figsize=(14, 4*len(durations)), sharex=True)

        for i, duration in enumerate(durations):
            ax = axes[i]
            events = results[threshold]['durations'][duration]['events_df']

            # Plot the surge data
            ax.plot(surge_df['Timestamp'], surge_df[surge_column], color='blue', linewidth=1, alpha=0.7)

            # Add horizontal lines for thresholds
            ax.axhline(y=surge_mean, color='red', linestyle='-', alpha=0.5, label='Mean')
            ax.axhline(y=surge_mean + threshold_value, color='orange', linestyle='--',
                      alpha=0.7, label=f'+{threshold}')
            ax.axhline(y=surge_mean - threshold_value, color='orange', linestyle='--', alpha=0.7)

            # Highlight events
            for _, event in events.iterrows():
                color = 'red' if event['Direction'] == 'Positive' else 'purple'
                # Mark peak
                ax.plot(event['Peak_Time'], event['Peak_Surge'], 'o', color=color, markersize=8)

                # Highlight full event duration
                mask = (surge_df['Timestamp'] >= event['Start_Time']) & (surge_df['Timestamp'] <= event['End_Time'])
                if any(mask):
                    ax.plot(surge_df.loc[mask, 'Timestamp'], surge_df.loc[mask, surge_column],
                           color=color, linewidth=2, alpha=0.7)

            # Add event count annotation
            count = len(events)
            ax.text(0.02, 0.92, f'Events: {count} (Min Duration: {duration})',
                   transform=ax.transAxes, bbox=dict(facecolor='white', alpha=0.7))

            # Add legend, title, and grid
            ax.legend(loc='upper right')
            ax.set_title(f'{data_type} Surge with {threshold} Threshold, {duration} Min Duration')
            ax.grid(True, alpha=0.3)

            # Format y-axis
            ax.set_ylabel('Surge (m)')

        # Format x-axis
        axes[-1].xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        axes[-1].xaxis.set_major_locator(mdates.MonthLocator())
        axes[-1].set_xlabel('Date')
        fig.autofmt_xdate()

        # Save figure
        plt.tight_layout()
        plt.savefig(f'{output_dir}/{data_type.lower()}_events_{threshold}_{durations[-1]}.png', dpi=300)
        plt.close()

    # Create a 3σ and 1σ comparison (to show dramatic difference)
    plt.figure(figsize=(14, 8))
    plt.plot(surge_df['Timestamp'], surge_df[surge_column], color='blue', linewidth=1, alpha=0.7, label='Surge')

    # Add threshold lines
    plt.axhline(y=surge_mean, color='red', linestyle='-', alpha=0.5, label='Mean')
    plt.axhline(y=surge_mean + 3*surge_std, color='purple', linestyle='--', alpha=0.7, label='3σ')
    plt.axhline(y=surge_mean - 3*surge_std, color='purple', linestyle='--', alpha=0.7)
    plt.axhline(y=surge_mean + 1*surge_std, color='green', linestyle=':', alpha=0.7, label='1σ')
    plt.axhline(y=surge_mean - 1*surge_std, color='green', linestyle=':', alpha=0.7)

    # Mark 3σ events
    events_3sigma = results['3.0σ']['durations']['3h']['events_df']
    for _, event in events_3sigma.iterrows():
        plt.plot(event['Peak_Time'], event['Peak_Surge'], 'o', color='purple', markersize=10)

    # Mark 1σ events (only the top 20 to avoid cluttering)
    events_1sigma = results['1.0σ']['durations']['3h']['events_df'].head(20)
    for _, event in events_1sigma.iterrows():
        plt.plot(event['Peak_Time'], event['Peak_Surge'], 's', color='green', markersize=6)

    # Format axes
    plt.xlabel('Date')
    plt.ylabel('Surge (m)')
    plt.title(f'Comparison of 1σ vs 3σ Threshold on {data_type} Surge (3h min duration)')
    plt.legend()
    plt.grid(True, alpha=0.3)

    # Format x-axis dates
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
    plt.gcf().autofmt_xdate()

    # Add annotations
    plt.text(0.02, 0.92, f'3σ Events: {len(events_3sigma)}', transform=plt.gca().transAxes,
             bbox=dict(facecolor='white', alpha=0.7), color='purple')
    plt.text(0.02, 0.85, f'1σ Events: {results["1.0σ"]["durations"]["3h"]["count"]} (top 20 shown)',
             transform=plt.gca().transAxes, bbox=dict(facecolor='white', alpha=0.7), color='green')

    plt.tight_layout()
    plt.savefig(f'{output_dir}/{data_type.lower()}_threshold_comparison.png', dpi=300)
    plt.close()

    print("Visualizations complete")

# Function to create comprehensive threshold analysis report
def generate_threshold_analysis_report(results, surge_mean, surge_std, use_filtered=True):
    """Generate a comprehensive report on threshold analysis results"""
    print("Generating threshold analysis report...")

    data_type = 'Filtered' if use_filtered else 'Raw'
    report_file = f'{output_dir}/{data_type.lower()}_threshold_analysis_report.txt'

    with open(report_file, 'w') as f:
        f.write(f"STORM SURGE THRESHOLD ANALYSIS REPORT ({data_type} DATA)\n")
        f.write("=================================================\n\n")

        f.write("THRESHOLD STATISTICS\n")
        f.write("-------------------\n")
        f.write(f"Mean: {surge_mean:.4f} m\n")
        f.write(f"Standard Deviation: {surge_std:.4f} m\n\n")

        f.write("THRESHOLD VALUES\n")
        f.write("---------------\n")
        for threshold, data in results.items():
            f.write(f"{threshold}: ±{data['threshold_value']:.4f} m\n")
        f.write("\n")

        # Event counts by threshold and duration
        f.write("EVENT COUNTS BY THRESHOLD AND MINIMUM DURATION\n")
        f.write("--------------------------------------------\n")

        # Table header
        thresholds = list(results.keys())
        durations = list(results[thresholds[0]]['durations'].keys())

        # Create header row
        header = "Threshold"
        for duration in durations:
            header += f" | {duration} (All/+/-)"
        f.write(f"{header}\n")
        f.write("-" * len(header) + "\n")

        # Create rows for each threshold
        for threshold in thresholds:
            row = f"{threshold}"
            for duration in durations:
                dur_data = results[threshold]['durations'][duration]
                row += f" | {dur_data['count']} ({dur_data['pos_count']}/{dur_data['neg_count']})"
            f.write(f"{row}\n")
        f.write("\n")

        # Detailed information about top events
        f.write("TOP 5 EVENTS BY THRESHOLD (3h MINIMUM DURATION)\n")
        f.write("--------------------------------------------\n")

        for threshold in thresholds:
            f.write(f"\n{threshold} THRESHOLD:\n")
            events = results[threshold]['durations']['3h']['events_df']

            if len(events) > 0:
                # Show top 5 events or all if less than 5
                top_events = events.head(min(5, len(events)))
                for i, (_, event) in enumerate(top_events.iterrows(), 1):
                    f.write(f"{i}. {event['Direction']} Surge on ")
                    f.write(f"{event['Peak_Time'].strftime('%Y-%m-%d %H:%M')}\n")
                    f.write(f"   Peak magnitude: {abs(event['Peak_Surge']):.4f} m\n")
                    f.write(f"   Duration: {event['Duration_Hours']:.1f} hours\n")
            else:
                f.write("No events detected\n")

        # Educational implications
        f.write("\nEDUCATIONAL IMPLICATIONS\n")
        f.write("------------------------\n")
        f.write("1. Threshold Selection: The choice of threshold dramatically affects the number\n")
        f.write("   of events identified. Lower thresholds detect more events but include less\n")
        f.write("   significant ones, while higher thresholds focus only on the most extreme events.\n\n")

        f.write("2. Duration Requirements: Requiring events to persist for longer periods filters\n")
        f.write("   out noise and transient phenomena. This is particularly important for\n")
        f.write("   distinguishing meteorologically-driven surges from other influences.\n\n")

        f.write("3. Balance: The ideal threshold and duration settings depend on the specific\n")
        f.write("   research or operational question being addressed. For educational purposes,\n")
        f.write("   examining multiple thresholds provides insight into the spectrum of events.\n")

    print(f"Threshold analysis report saved to {report_file}")
    return report_file

# Function to compare raw vs filtered surge across thresholds
def compare_raw_vs_filtered(raw_results, filtered_results, raw_mean, raw_std, filtered_mean, filtered_std):
    """Create comparison of how filtering affects event detection across thresholds"""
    print("Creating raw vs filtered comparison...")

    # Create comparison plot of event counts
    plt.figure(figsize=(14, 8))

    # Extract data for plotting
    thresholds = list(raw_results.keys())

    # Count events for 3h duration requirement
    raw_counts = [raw_results[t]['durations']['3h']['count'] for t in thresholds]
    filtered_counts = [filtered_results[t]['durations']['3h']['count'] for t in thresholds]

    # Set up bar positions
    bar_width = 0.35
    r1 = np.arange(len(thresholds))
    r2 = [x + bar_width for x in r1]

    # Plot bars
    plt.bar(r1, raw_counts, width=bar_width, label='Raw Surge', color='lightblue')
    plt.bar(r2, filtered_counts, width=bar_width, label='Filtered Surge', color='orange')

    # Add labels and legend
    plt.xlabel('Threshold Level')
    plt.ylabel('Number of Events')
    plt.title('Comparison of Event Counts: Raw vs Filtered Surge (3h min duration)')
    plt.xticks([r + bar_width/2 for r in range(len(thresholds))], thresholds)
    plt.legend()
    plt.grid(True, alpha=0.3)

    # Add value labels on bars
    for i in range(len(thresholds)):
        plt.text(r1[i], raw_counts[i] + 1, str(raw_counts[i]),
                ha='center', va='bottom', fontsize=10)
        plt.text(r2[i], filtered_counts[i] + 1, str(filtered_counts[i]),
                ha='center', va='bottom', fontsize=10)

    plt.tight_layout()
    plt.savefig(f'{output_dir}/raw_vs_filtered_comparison.png', dpi=300)
    plt.close()

    # Create comparison table
    comparison_file = f'{output_dir}/raw_vs_filtered_comparison.txt'

    with open(comparison_file, 'w') as f:
        f.write("COMPARISON OF RAW VS FILTERED SURGE EVENT DETECTION\n")
        f.write("================================================\n\n")

        f.write("BASIC STATISTICS\n")
        f.write("--------------\n")
        f.write(f"Raw Surge - Mean: {raw_mean:.4f} m, StdDev: {raw_std:.4f} m\n")
        f.write(f"Filtered Surge - Mean: {filtered_mean:.4f} m, StdDev: {filtered_std:.4f} m\n\n")

        f.write("EVENT COUNTS BY THRESHOLD (3h MINIMUM DURATION)\n")
        f.write("-------------------------------------------\n")

        # Table header
        f.write("Threshold | Raw Events | Filtered Events | Difference | % Reduction\n")
        f.write("---------|-----------|-----------------|-----------|-----------\n")

        # Table rows
        for i, threshold in enumerate(thresholds):
            raw_count = raw_results[threshold]['durations']['3h']['count']
            filtered_count = filtered_results[threshold]['durations']['3h']['count']
            difference = raw_count - filtered_count
            pct_reduction = (difference / raw_count * 100) if raw_count > 0 else 0

            f.write(f"{threshold} | {raw_count} | {filtered_count} | {difference} | {pct_reduction:.1f}%\n")

        f.write("\nEDUCATIONAL IMPLICATIONS OF FILTERING\n")
        f.write("----------------------------------\n")
        f.write("1. Noise Reduction: Filtering removes high-frequency oscillations that may be\n")
        f.write("   measurement noise or phenomena with timescales shorter than meteorological events.\n\n")

        f.write("2. Event Consolidation: Multiple raw exceedances close in time often represent\n")
        f.write("   a single meteorological event. Filtering consolidates these into a clearer signal.\n\n")

        f.write("3. Threshold Selection: The appropriate threshold depends on whether you're using\n")
        f.write("   raw or filtered data. Lower thresholds may be appropriate for filtered data\n")
        f.write("   since noise has already been reduced.\n\n")

        f.write("4. Research vs. Operations: Research may benefit from examining both raw and filtered\n")
        f.write("   data, while operational forecasting typically relies on filtered data for clarity.\n")

    print(f"Raw vs filtered comparison saved to {comparison_file}")

# Main function to perform threshold analysis
def perform_threshold_analysis():
    """Main function to perform comprehensive threshold analysis"""

    print("\n= Supplementary Analysis: Threshold Selection in Storm Surge Identification =\n")

    # Load surge data
    surge_df, has_filtered = load_surge_data()

    # Set threshold factors to analyze
    threshold_factors = [1.0, 1.5, 2.0, 2.5, 3.0]  # Multiple of standard deviation
    min_durations = [1, 3, 6]  # Hours

    # Analyze raw surge data
    print("\nAnalyzing raw surge data...")
    raw_results, raw_mean, raw_std = identify_events_with_thresholds(
        surge_df, threshold_factors, min_durations, use_filtered=False
    )

    # Create visualizations for raw surge
    create_threshold_comparison_plots(surge_df, raw_results, raw_mean, raw_std, use_filtered=False)

    # Generate report for raw surge
    raw_report = generate_threshold_analysis_report(raw_results, raw_mean, raw_std, use_filtered=False)

    # If filtered data is available, analyze it too
    if has_filtered:
        print("\nAnalyzing filtered surge data...")
        filtered_results, filtered_mean, filtered_std = identify_events_with_thresholds(
            surge_df, threshold_factors, min_durations, use_filtered=True
        )

        # Create visualizations for filtered surge
        create_threshold_comparison_plots(surge_df, filtered_results, filtered_mean, filtered_std, use_filtered=True)

        # Generate report for filtered surge
        filtered_report = generate_threshold_analysis_report(filtered_results, filtered_mean, filtered_std, use_filtered=True)

        # Compare raw vs filtered
        compare_raw_vs_filtered(raw_results, filtered_results, raw_mean, raw_std, filtered_mean, filtered_std)

    # Print summary
    print("\nTHRESHOLD ANALYSIS SUMMARY")
    print("=========================")
    print(f"Raw surge analysis complete - report saved to {raw_report}")

    if has_filtered:
        print(f"Filtered surge analysis complete - report saved to {filtered_report}")
        print(f"Comparison analysis saved to {output_dir}/raw_vs_filtered_comparison.txt")

    print("\nAll visualizations saved to the following directory:")
    print(f"  {output_dir}/")

    print("\n==== EDUCATIONAL GUIDANCE ====")
    print("To use these results effectively in teaching:")
    print("1. Start with the threshold comparison visualization to show how different")
    print("   thresholds dramatically change the number of identified events.")
    print("2. Use the event count bar charts to discuss the tradeoffs between")
    print("   sensitivity (lower thresholds) and specificity (higher thresholds).")
    print("3. If you have filtered data, use the raw vs filtered comparison to")
    print("   demonstrate the purpose and effect of signal processing in oceanography.")
    print("4. For advanced students, discuss how different event definitions")
    print("   (threshold + duration) affect research conclusions and operational decisions.")

    return raw_results, filtered_results if has_filtered else None

# Execute the analysis
if __name__ == "__main__":
    raw_results, filtered_results = perform_threshold_analysis()
