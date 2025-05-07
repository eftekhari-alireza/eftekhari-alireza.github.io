# 📊 A Comprehensive Tool for Tidal Analysis and Storm Surge Detection

This project provides a complete framework for performing harmonic tidal analysis, extracting storm surge signals, and identifying significant meteorological events affecting sea levels. Using advanced signal processing techniques, this toolset allows researchers, oceanographers, and coastal engineers to analyze sea level data, decompose it into tidal and non-tidal components, and detect extreme events.

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Installation](#️-installation)
- [Data Requirements](#-data-requirements)
- [Usage](#-usage)
  - Script 1: Determining Tidal Constituents
  - Script 2: Predicting Tidal Signal
  - Script 3: Calculating Storm Surge Residuals
  - Script 4: Filtering Storm Surge and Identifying Events
  - Supplementary Analysis: Threshold Selection
  - Enhanced Residual Visualization
- [Methodology](#-methodology)
- [Example Results](#-example-results)
- [Educational Resources](#-educational-resources)
- [Contributing](#contributing)
- [License](#license)
- [Citations](#-citations)
- [Contact](#-contact)

---

## 🌊 Overview

Storm surges represent abnormal sea level rises or falls caused by meteorological conditions such as atmospheric pressure changes and wind forcing. Accurate detection and analysis of these events are crucial for coastal management, hazard assessment, and understanding climate change impacts.

Storm surges can cause significant coastal flooding during extreme weather events, especially when they coincide with high tides. Conversely, negative storm surges (abnormally low water levels) can disrupt shipping and harbor operations. By accurately identifying and characterizing these events, coastal communities can develop more effective adaptation and mitigation strategies.

This project implements a complete pipeline for storm surge analysis:

- **Harmonic Tidal Analysis** – Extract tidal constituents (M2, S2, K1, etc.) using linear regression on trigonometric functions.
- **Tidal Prediction** – Reconstruct pure astronomical tidal signals using calculated amplitudes and phases.
- **Residual Calculation** – Subtract predicted tide from original measurements to isolate non-tidal (storm surge) components.
- **Signal Filtering** – Apply Butterworth low-pass filters to remove high-frequency noise while retaining meteorological signals.
- **Event Detection** – Use adaptive thresholding to identify and group significant storm surge events.
- **Visualization** – Produce detailed, educational plots of all analysis outputs.

Each module is independent, making the system flexible for different research needs.

---

## ✨ Features

- **Robust Tidal Analysis**: Identifies major and minor constituents (M2, S2, N2, K1, O1, etc.) with precise amplitudes and phases.
- **Advanced Signal Processing**: Butterworth filtering with customizable cutoff frequency and filter order.
- **Adaptive Thresholding**: Supports various threshold methods (1σ–3σ, absolute, percentile-based).
- **Comprehensive Visualization**: Time series plots, seasonal heatmaps, distribution histograms, and more.
- **Statistical Analysis**: Event duration, magnitude, onset rate, frequency of occurrence.
- **Educational Components**: Detailed comments, explanations, and visual guides for oceanographic learning.
- **Seasonal & Frequency Analysis**: Monthly patterns, statistical distributions, and extreme value analysis.
- **Extreme Event Identification**: Automated detection of significant surges with full event metadata.

---

## 🛠️ Installation


# Clone the repository
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
Cover at least 1 month (preferably 1 year)
Have minimal gaps (small gaps are interpolated)
Example format:

timestamp,sea_level_height
2022-01-01 00:00:00,1.23
2022-01-01 01:00:00,1.45
...
📝 Usage

Script 1: Determining Tidal Constituents
python 1_tidal_constituents.py --input your_ssh_data.csv --output ./tidal_analysis_results
Loads SSH data
Builds design matrix
Fits linear model for amplitude and phase
Saves:
tidal_constituents.csv
model_parameters.npz
top_constituents.png
Script 2: Predicting Tidal Signal
python 2_predict_tide.py --input your_ssh_data.csv --output ./tidal_analysis_results
Loads constituent data
Reconstructs tidal signal
Saves:
predicted_tide.csv
ssh_comparison_full.png
constituent_contributions.png
Script 3: Calculating Storm Surge Residuals
python 3_storm_surge.py --output ./tidal_analysis_results
Subtracts predicted tide from original
Analyzes residual
Saves:
storm_surge_raw.csv
extreme_surge_events_raw.csv
surge_statistics_raw.txt
storm_surge_raw.png
Script 4: Filtering Storm Surge and Identifying Events
python 4_filter_surge.py --cutoff 12 --order 3 --threshold 2.0 --output ./tidal_analysis_results
Applies Butterworth filter
Identifies significant events
Saves:
filtered_surge.csv
significant_surge_events.csv
final_analysis_report.txt
filtered_surge_full.png
top_surge_events.png
Supplementary: Threshold Selection
python threshold_analysis.py --output ./tidal_analysis_results/threshold_analysis
Applies multiple thresholds
Saves visualizations:
raw_vs_filtered_comparison.png
threshold_comparison.png
Enhanced Residual Visualization
python residual_visualization.py --output ./tidal_analysis_results/residual_visualizations
Saves:
annotated_storm_surge.png
seasonal_analysis.png
frequency_analysis.png
filtering_comparison.png
educational_summary.png
🔬 Methodology

Tidal Harmonic Analysis
Decomposes SSH signal into known constituents (M2, S2, K1, etc.)
Uses linear regression with sine and cosine terms:
Amplitude = √(C²+S²)
Phase = arctan(S/C)
Key frequencies:
M2 (12.42h), S2 (12.00h), N2, K1 (23.93h), O1 (25.82h), etc.
Storm Surge Extraction
Storm Surge = Original SSH - Predicted Tide
Includes meteorological influences (pressure, wind), ocean circulation, and other anomalies.

Signal Filtering
Butterworth low-pass filter:
Cutoff: ~12 hours
Order: 3–5
Zero-phase filtering (using filtfilt)
Allows tuning of:
Signal preservation vs. noise reduction
Event sharpness vs. smoothness
Event Detection
Thresholds: 2σ, 3σ, absolute meters, or percentile-based
Groups exceedances into events
Calculates:
Start/end time
Peak magnitude
Duration
Direction (positive/negative)
📈 Example Results

Top 5 Significant Surge Events
Date & Time	Surge (m)	Direction	Duration
2022-03-15 08:00	+0.4532	Positive	18.0 h
2022-10-27 14:00	-0.3981	Negative	12.5 h
2022-01-22 21:00	+0.3754	Positive	15.0 h
2022-09-08 03:00	-0.3421	Negative	9.5 h
2022-05-31 16:00	+0.3102	Positive	8.0 h
📚 Educational Resources

In-Script Comments: Explain concepts like:
Astronomical tides
Surge physics
Signal processing
Visualizations:
Interactive constituent plots
Filtering demonstrations
Threshold analysis
Seasonal surge heatmaps
Reports:
Stats summaries with interpretation
Educational explanations
Event insights by time/season
Tutorial Scripts:
Guide through threshold choice, filtering, and validation
📚 Citations

If you use this code in your research, please cite:

@software{storm_surge_detection_model,
  author = {Eftekhari, Alireza},
  title = {Storm Surge Detection Model},
  url = {https://github.com/eftekhari-alireza/eftekhari-alireza.github.io/tree/main/Storm%20Surge%20Detection%20Model},
  year = {2025}
}
📧 Contact

Alireza Eftekhari
📨 a.eftekhari2@universityofgalway.ie
🔗 Project Link

Helping to understand and predict coastal hazards through advanced tidal analysis.
