📊 A Comprehensive Tool for Tidal Analysis and Storm Surge Detection
This project provides a complete framework for performing harmonic tidal analysis, extracting storm surge signals, and identifying significant meteorological events affecting sea levels. Using advanced signal processing techniques, this toolset allows researchers, oceanographers, and coastal engineers to analyze sea level data, decompose it into tidal and non-tidal components, and detect extreme events.

📋 Table of Contents

Overview
Features
Installation
Data Requirements
Usage

Script 1: Determining Tidal Constituents

Script 2: Predicting Tidal Signal

Script 3: Calculating Storm Surge Residuals

Script 4: Filtering Storm Surge and Identifying Events

Supplementary Analysis: Threshold Selection

Enhanced Residual Visualization




Methodology
Example Results
Educational Resources
Contributing
License
Citations
Contact



🌊 Overview


Storm surges represent abnormal sea level rises or falls caused by meteorological conditions such as atmospheric pressure changes and wind forcing. Accurate detection and analysis of these events are crucial for coastal management, hazard assessment, and understanding climate change impacts.


Storm surges can cause significant coastal flooding during extreme weather events, especially when they coincide with high tides. Conversely, negative storm surges (abnormally low water levels) can disrupt shipping and harbor operations. By accurately identifying and characterizing these events, coastal communities can develop more effective adaptation and mitigation strategies.


This project implements a complete pipeline for storm surge analysis:

Harmonic Tidal Analysis - Identifying and extracting tidal constituents from sea level measurements by decomposing the signal into astronomical components (M2, S2, K1, etc.) using linear regression on trigonometric functions. This step isolates the predictable, astronomically-driven tidal variations.


Tidal Prediction - Reconstructing the pure astronomical tidal signal by combining the identified constituents with their calculated amplitudes and phases. This creates a "clean" tidal prediction that represents what would occur under normal astronomical forces alone.


Residual Calculation - Extracting the non-tidal (storm surge) component by subtracting the predicted tidal signal from original measurements. This residual contains all meteorological and other non-astronomical influences on sea level.


Signal Filtering - Separating meteorological signal from noise using Butterworth low-pass filters, which remove high-frequency oscillations while preserving the meteorologically-driven variations that typically occur over hours to days.


Event Detection - Identifying significant surge events with adaptive thresholding based on statistical properties of the data. The system automatically groups consecutive threshold exceedances into discrete events and calculates their key characteristics.


Visualization - Creating comprehensive educational visualizations of the results, including time series analysis, seasonal patterns, statistical distributions, and detailed event characterizations.


The modular architecture allows users to perform the complete analysis pipeline or utilize individual components for specific research needs. Each module can be run independently with appropriate input data, making the system adaptable to various research and operational contexts.

✨ Features

Robust Tidal Analysis: Accurate identification of major and minor tidal constituents including M2 (principal lunar semidiurnal), S2 (principal solar semidiurnal), N2 (larger lunar elliptic semidiurnal), K1 (lunar diurnal), O1 (lunar diurnal), and more. The system calculates precise amplitude and phase values for each constituent.


Advanced Signal Processing: Butterworth low-pass filtering to separate meteorological signals from noise. The implementation allows customization of filter order and cutoff frequency to adapt to different data sampling rates and noise characteristics.


Adaptive Thresholding: Tools for selecting appropriate threshold levels for event detection based on statistical properties of the data. The system supports multiple threshold methods including standard deviation-based (1σ to 3σ) and absolute value thresholds.


Comprehensive Visualization: Multiple visualization techniques to explore and present results, including time series plots, heatmaps of seasonal patterns, distribution analysis, and comparative visualizations of raw versus filtered data.


Statistical Analysis: Detailed statistical characterization of surge events including duration, magnitude, onset rate, and frequency of occurrence. The system calculates standard statistical measures and provides tools for examining the distribution properties of surge events.


Educational Components: Built-in educational visualizations and explanations that help users understand the physical processes behind tidal patterns and storm surges. Each script includes detailed comments explaining oceanographic concepts.


Seasonal Analysis: Tools for examining seasonal patterns in storm surge, including monthly statistics, seasonal trends, and correlation with typical weather patterns. The system can identify months and seasons with higher surge activity.


Frequency Analysis: Distribution and statistical tools for surge characterization, including histogram analysis, quantile-quantile plots for normality testing, and extreme value analysis.


Extreme Event Identification: Automated detection of significant surge events using configurable thresholds and duration criteria. The system can group consecutive threshold exceedances into coherent events and characterize their properties.



🛠️ Installation
bash# Clone the repository
git clone https://github.com/yourusername/storm-surge-detection-model.git
cd storm-surge-detection-model

# Create a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install required packages
pip install -r requirements.txt
Requirements



pip install numpy pandas matplotlib scipy scikit-learn



Python 3.6+
NumPy
Pandas
Matplotlib
SciPy
scikit-learn

📊 Data Requirements
The model requires sea surface height (SSH) data as input, typically in CSV format. The data should:

Contain time-series measurements of sea level


Be regularly sampled (ideally hourly)


Span a sufficiently long period (minimum 1 month, ideally 1 year) to capture all tidal constituents


Have minimal gaps (the code includes interpolation for small gaps)

Example format:
timestamp,sea_level_height
2022-01-01 00:00:00,1.23
2022-01-01 01:00:00,1.45
...
📝 Usage
The analysis is split into multiple scripts that can be run sequentially or individually:


Script 1: Determining Tidal Constituents

This script performs the first step in tidal harmonic analysis: identifying and calculating the amplitude and phase of tidal constituents.
bashpython 1_tidal_constituents.py --input your_ssh_data.csv --output ./tidal_analysis_results



Key operations:

Loads SSH (Sea Surface Height) data
Creates a design matrix based on tidal constituent frequencies
Fits a linear model to determine amplitude and phase of each constituent
Saves the results for subsequent processing



Output:

tidal_constituents.csv: Details of identified tidal constituents
model_parameters.npz: Model parameters for subsequent analysis
top_constituents.png: Visualization of dominant tidal constituents




Script 2: Predicting Tidal Signal
This script uses the constituent information to reconstruct/predict the tidal signal.
bashpython 2_predict_tide.py --input your_ssh_data.csv --output ./tidal_analysis_results




Key operations:

Loads the constituent data from Script 1
Creates a time series with proper timestamps
Reconstructs the tidal signal using the constituent amplitudes and phases
Visualizes the predicted tide


Output:

predicted_tide.csv: Time series of original and predicted tidal signals
ssh_comparison_full.png: Comparison of original and predicted sea level
constituent_contributions.png: Visualization of individual constituent contributions


Script 3: Calculating Storm Surge Residuals


This script calculates the residual (storm surge) by subtracting the predicted tide from the original sea surface height.
bashpython 3_storm_surge.py --output ./tidal_analysis_results



Key operations:

Loads the original data and predicted tide from Script 2
Calculates the residual (original - predicted)
Analyzes the statistical properties of the residual
Visualizes the storm surge components

Output:

storm_surge_raw.csv: Raw storm surge residual data
extreme_surge_events_raw.csv: Detected extreme surge events
surge_statistics_raw.txt: Statistical analysis of surge data
storm_surge_raw.png: Visualization of raw storm surge




Script 4: Filtering Storm Surge and Identifying Events
This script applies a Butterworth low-pass filter to separate meteorological signals from noise and identify significant events.
bashpython 4_filter_surge.py --cutoff 12 --order 3 --threshold 2.0 --output ./tidal_analysis_results



Key operations:

Loads the raw storm surge data from Script 3
Applies a Butterworth low-pass filter to separate meteorological signals from noise
Identifies and characterizes significant surge events
Creates comprehensive visualizations
Generates a final report



Output:

filtered_surge.csv: Filtered storm surge data
significant_surge_events.csv: Details of significant surge events
final_analysis_report.txt: Comprehensive analysis report
filtered_surge_full.png: Visualization of filtered surge with events
top_surge_events.png: Detailed views of top events



Supplementary Analysis: Threshold Selection


This script demonstrates how different thresholds and identification methods affect storm surge event detection.
bashpython threshold_analysis.py --output ./tidal_analysis_results/threshold_analysis
Key operations:



Applies multiple threshold levels (1σ, 1.5σ, 2σ, 2.5σ, 3σ)
Identifies events using different criteria
Creates educational visualizations showing the impact of these choices
Generates comparison statistics



Output:

raw_vs_filtered_comparison.png: Comparison of detection in raw vs filtered data
threshold_comparison.png: Effect of different thresholds on event detection
Various threshold-specific visualizations and reports


Enhanced Residual Visualization



This script creates comprehensive educational visualizations of the storm surge residuals.
bashpython residual_visualization.py --output ./tidal_analysis_results/residual_visualizations



Key operations:

Creates annotated time series visualization
Performs seasonal analysis
Conducts frequency analysis
Compares raw vs. filtered data
Generates educational summary visualization

Output:

annotated_storm_surge.png: Comprehensive annotated time series
seasonal_analysis.png: Seasonal patterns in storm surge
frequency_analysis.png: Statistical distribution analysis
filtering_comparison.png: Effect of filtering across time scales
educational_summary.png: Multi-panel educational summary

🔬 Methodology

Tidal Harmonic Analysis

The model uses harmonic analysis to decompose tidal signals into constituent frequencies:

Constituent Identification: The model analyzes astronomical tidal constituents like M2 (principal lunar semidiurnal), S2 (principal solar semidiurnal), K1 (lunar diurnal), and others.
Each constituent represents a specific astronomical force with a known frequency:

M2 (12.42 hour period): Principal lunar semidiurnal tide, caused by the moon's gravitational pull

S2 (12.00 hour period): Principal solar semidiurnal tide, caused by the sun's gravitational pull

N2 (12.66 hour period): Larger lunar elliptic semidiurnal, related to monthly variations in moon's distance

K1 (23.93 hour period): Lunar diurnal tide, caused by lunar declination

O1 (25.82 hour period): Lunar diurnal tide, caused by lunar orbit inclination

Plus several others including shallow water overtides (M4) and long-period constituents (Mf, Mm, Ssa)


Design Matrix: A design matrix is constructed using sine and cosine terms for each constituent frequency.

For each constituent frequency (f), the model includes both sine and cosine components:

Cosine term: cos(2πft)

Sine term: sin(2πft)

This creates a design matrix X where each column represents either a sine or cosine component for a specific frequency, and each row represents a time point.

Linear Regression: The model uses linear regression to determine the amplitude and phase of each constituent.


The linear model fits: SSH = X·β + ε


Where:

SSH is the sea surface height measurements
X is the design matrix described above
β are the coefficient parameters to be estimated
ε is the residual error

From the fitted coefficients, amplitude and phase are calculated as:

Amplitude = √(C²+S²) where C and S are the cosine and sine coefficients

Phase = arctan(S/C) (adjusted to appropriate quadrant)



Storm Surge Extraction

Storm surge is obtained by removing the predicted tidal signal from the original sea level measurements:

Storm Surge = Original SSH - Predicted Tide

This residual represents all non-tidal influences on sea level, including:


Meteorological effects (atmospheric pressure, wind forcing)
Oceanic circulation patterns
Measurement errors and instrumental noise
Seismic events (tsunamis, if present in the data)
Other unmodeled effects



The quality of storm surge extraction depends directly on the accuracy of the tidal prediction, which is why capturing all relevant tidal constituents is critical.


Signal Filtering
A Butterworth low-pass filter is applied to separate meteorological signals from noise:

Filter Design: A Butterworth filter is designed with customizable cutoff frequency and order.

The Butterworth filter is chosen because it has a maximally flat frequency response in the passband (minimal ripple), making it ideal for this application. Key parameters include:

Cutoff period: Typically 12 hours, to separate meteorological signals (which typically vary over days) from higher-frequency noise

Filter order: Typically 3-5, controlling the steepness of the roll-off

Sampling rate: Matched to the data collection frequency (typically hourly)


Application: The filter is applied to the raw storm surge to obtain a cleaner signal.

The implementation uses SciPy's filtfilt function, which applies the filter forward and backward to achieve zero phase distortion. This preserves the timing of surge events, which is critical for accurate event detection.

Comparison: The script provides tools to explore different filter settings and their effects.

Users can visualize how different filter parameters affect:

Signal preservation vs. noise reduction

Event onset/decay characteristics

Peak magnitude preservation

Event duration measurement



Event Detection

Significant events are identified using statistical thresholds:

Threshold Definition: Events are defined as exceedances of a threshold based on standard deviations (typically 2σ or 3σ).

The system supports multiple threshold approaches:

Statistical thresholds based on standard deviations from the mean

Absolute thresholds in physical units (meters)

Percentile-based thresholds (e.g., 95th or 99th percentile)


The default approach uses standard deviation multipliers to automatically adapt to the statistical properties of the specific data set being analyzed.

Event Grouping: Consecutive threshold exceedances are grouped into events.


The system applies these steps:

Identify all data points exceeding the threshold

Calculate time differences between consecutive exceedances

Group exceedances that occur within a specified time window (typically 3 hours)

Assign unique event IDs to each group of consecutive exceedances


Characterization: Events are characterized by their duration, peak magnitude, and direction (positive or negative).

For each identified event, the system calculates:

Start time and end time

Peak time (time of maximum absolute excursion)

Event duration (end time - start time)

Peak magnitude (maximum excursion during the event)

Direction (positive = higher than predicted, negative = lower than predicted)

Rate of onset (how quickly the surge developed)

Additional user-configurable metrics



📈 Example Results

The analysis identifies significant surge events and provides detailed characterization:
TOP 5 SIGNIFICANT SURGE EVENTS
=============================
1. 2022-03-15 08:00: 0.4532m Positive surge (18.0 hours)
2. 2022-10-27 14:00: -0.3981m Negative surge (12.5 hours)
3. 2022-01-22 21:00: 0.3754m Positive surge (15.0 hours)
4. 2022-09-08 03:00: -0.3421m Negative surge (9.5 hours)
5. 2022-05-31 16:00: 0.3102m Positive surge (8.0 hours)
Each event is characterized by:

Timestamp: The exact date and time of peak surge

Magnitude: The maximum deviation from predicted tide (in meters)

Direction: Whether water level was higher (positive) or lower (negative) than predicted

Duration: How long the event persisted above threshold (in hours)


The system also calculates additional metrics for each event:

Rate of onset (how quickly the surge developed)

Percent of historical maximum (comparing to the most extreme recorded event)

Time of day and seasonal context

Statistical significance relative to typical conditions

📚 Educational Resources

This project includes several educational components designed to help users understand the physical processes behind tidal patterns and storm surges:

Explanatory Comments: All scripts include detailed comments explaining oceanographic concepts, including:

The astronomical origins of tidal constituents

The physics of storm surge development

Signal processing principles for meteorological data

Statistical approaches to extreme value analysis

Seasonal variations in sea level phenomena


Visualizations: Educational visualizations demonstrate key concepts:

Tidal constituent contributions: Interactive plots showing how individual astronomical forces (M2, S2, K1, etc.) combine to create complex tidal patterns

Filtering effects: Comparative visualizations showing the impact of different filter settings on signal preservation and noise reduction

Threshold selection impacts: Analysis of how different threshold choices affect event detection sensitivity and specificity

Seasonal patterns: Heatmaps and seasonal breakdowns of storm surge activity throughout the year

Frequency distributions: Statistical visualizations showing the probability distribution of surge events


Analysis Reports: Generated reports include explanations of findings and their implications:

Comprehensive statistical summaries with interpretations

Detailed event characterizations with physical explanations

Comparative analyses across different time scales (daily, monthly, seasonal, annual)

Educational notes explaining the oceanographic and meteorological significance of detected patterns



Tutorial Scripts: The supplementary analysis scripts function as tutorials demonstrating:

How threshold selection affects event detection

The importance of filtering in signal processing

The relationship between tidal prediction accuracy and surge detection

Methods for validating detection algorithms


Educational Notes: Each script includes dedicated educational notes sections that explain:

The physical processes behind the observed patterns

Interpretation guidelines for the results

Common pitfalls in tidal and surge analysis

Connections to broader oceanographic and climate science concepts



📚 Citations
If you use this code in your research, please cite:
@software{storm_surge_detection_model,
  author = {Eftekhari, Alireza},
  title = {Storm Surge Detection Model},
  url = {https://github.com/eftekhari-alireza/eftekhari-alireza.github.io/tree/main/Storm%20Surge%20Detection%20Model},
  year = {2025},
}
📧 Contact
Alireza Eftekhari - a.eftekhari2@universityofgalway.ie
Project Link: https://github.com/eftekhari-alireza/eftekhari-alireza.github.io

<p align="center">
  <i>Helping to understand and predict coastal hazards through advanced tidal analysis</i>
</p>
