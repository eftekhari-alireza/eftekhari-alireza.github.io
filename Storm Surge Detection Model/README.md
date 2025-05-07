# 🌊 Storm Surge Detection Model

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/yourusername/storm-surge-detection-model/blob/main/storm_surge_analysis.ipynb)
[![Python 3.6+](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)


> **A comprehensive framework for tidal analysis and storm surge detection, now available in an easy-to-use Google Colab notebook!**

## 📊 Overview

Storm surges represent abnormal sea level rises or falls caused by meteorological conditions such as atmospheric pressure changes and wind forcing. This toolkit provides a complete analysis pipeline that you can run **entirely in Google Colab** - no local installation required!

![Storm Surge Visualization](https://raw.githubusercontent.com/yourusername/storm-surge-detection-model/main/images/sample_visualization.png)

### Why use our Colab-ready model?

- **Instant setup** - Skip installation headaches
- **Interactive workflow** - Run each step in its own cell
- **Easy experimentation** - Modify parameters with simple widgets
- **Visual results** - See plots and analysis immediately
- **Cloud computing** - Process large datasets without local resources
- **Shareable analysis** - Collaborate seamlessly with colleagues

## ✨ Features

- **Robust Tidal Analysis**: Identify major and minor constituents (M2, S2, N2, K1, O1, etc.) with precise amplitudes and phases
- **Advanced Signal Processing**: Butterworth filtering with customizable cutoff frequency and filter order
- **Adaptive Thresholding**: Multiple threshold methods (1σ–3σ, absolute, percentile-based)
- **Comprehensive Visualization**: Time series plots, seasonal heatmaps, distribution histograms
- **Statistical Analysis**: Event duration, magnitude, onset rate, frequency of occurrence
- **Educational Components**: Detailed comments, explanations, and visual guides
- **Seasonal & Frequency Analysis**: Monthly patterns, statistical distributions, extreme value analysis
- **Extreme Event Identification**: Automated detection of significant surges with full event metadata

## 📊 Data Requirements

Our model works with sea surface height (SSH) data, typically in CSV format. The data should:

- Contain time-series measurements of sea level
- Be regularly sampled (ideally hourly)
- Cover at least 1 month (preferably 1 year)
- Have minimal gaps (small gaps are interpolated)

csv
timestamp,sea_level_height
2022-01-01 00:00:00,1.23
2022-01-01 01:00:00,1.45
...
🚀 Getting Started with Google Colab

Open our notebook: Click the "Open in Colab" badge at the top of this README
Upload your data: Use the Colab file upload widget or connect to Google Drive
Run cells sequentially: Each analysis step is in its own cell
Visualize results: See plots and analysis in real-time
Experiment: Modify parameters and instantly see the effects

📝 Step-by-Step Analysis in Colab
Cell 1: Setup and Data Loading
python# Just run this cell to install all requirements
!pip install numpy pandas matplotlib scipy scikit-learn

# Upload your data or connect to Google Drive
from google.colab import files
uploaded = files.upload()  # Upload your SSH data CSV
Cell 2: Determining Tidal Constituents
python# Run this cell to analyze tidal constituents
# Modify parameters as needed
input_file = "your_ssh_data.csv"
constituent_count = 8  # Change this to analyze more/fewer constituents

# The analysis runs automatically when you execute the cell!
# Results and visualizations appear below the cell
Cell 3: Predicting Tidal Signal
python# Run this cell to generate the predicted tidal signal
# Interactive widgets appear for customization
Cell 4: Calculating Storm Surge Residuals
python# Run this cell to extract the storm surge signal
# Plots show original, tidal, and residual components
Cell 5: Filtering and Event Detection
python# Interactive filter customization
cutoff_hours = 12  # Adjust the filter cutoff frequency
filter_order = 3   # Adjust the Butterworth filter order
threshold = 2.0    # Set detection threshold (σ units)

# The analysis updates as you modify parameters!
Cell 6: Visualization and Reporting
python# Generate comprehensive visualizations and reports
# Export results to your Google Drive if desired
🔬 Methodology
Our approach combines several key techniques:

Tidal Harmonic Analysis

Decomposes SSH signal into known constituents (M2, S2, K1, etc.)
Uses linear regression with sine and cosine terms
Key frequencies: M2 (12.42h), S2 (12.00h), N2, K1 (23.93h), O1 (25.82h), etc.


Storm Surge Extraction

Storm Surge = Original SSH - Predicted Tide
Captures meteorological influences, ocean circulation, and anomalies


Signal Filtering

Butterworth low-pass filter with customizable parameters
Zero-phase filtering for accurate event timing


Event Detection

Multiple threshold options (statistical or absolute)
Automated event grouping and characterization



📈 Example Results
Event Date & TimeSurge (m)DirectionDuration2022-03-15 08:00+0.4532Positive18.0 h2022-10-27 14:00-0.3981Negative12.5 h2022-01-22 21:00+0.3754Positive15.0 h2022-09-08 03:00-0.3421Negative9.5 h2022-05-31 16:00+0.3102Positive8.0 h
🧠 Why Google Colab?

Zero setup time: Start analyzing in seconds
Interactive parameters: Adjust thresholds, filters with immediate feedback
Educational experience: Perfect for learning tidal analysis concepts
Free GPU acceleration: Process large datasets faster
Version control: Save different analysis versions to your Drive
Shareable results: Send complete analyses to colleagues

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

Helping to understand and predict coastal hazards through advanced tidal analysis - now more accessible than ever with Google Colab!
