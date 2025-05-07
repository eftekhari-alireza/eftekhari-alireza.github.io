# 🌊 Storm Surge Detection Model

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/yourusername/storm-surge-detection-model/blob/main/storm_surge_analysis.ipynb)
[![Python 3.6+](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)

> **A comprehensive framework for tidal analysis and storm surge detection, now available in an easy-to-use Google Colab notebook!**

---

## 📊 Overview

Storm surges represent abnormal sea level rises or falls caused by meteorological conditions such as atmospheric pressure changes and wind forcing. This toolkit provides a complete analysis pipeline that you can run **entirely in Google Colab** - no local installation required!

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

```csv
timestamp,sea_level_height
2022-01-01 00:00:00,1.23
2022-01-01 01:00:00,1.45
...
```

## 🚀 Getting Started with Google Colab

1. **Open our notebook**: Click the "Open in Colab" badge at the top of this README
2. **Upload your data**: Use the Colab file upload widget or connect to Google Drive
3. **Run cells sequentially**: Each analysis step is in its own cell
4. **Visualize results**: See plots and analysis in real-time
5. **Experiment**: Modify parameters and instantly see the effects

## 📝 Step-by-Step Analysis in Colab

### Cell 1: Setup and Data Loading
```python
# Just run this cell to install all requirements
!pip install numpy pandas matplotlib scipy scikit-learn

# Upload your data or connect to Google Drive
from google.colab import files
uploaded = files.upload()  # Upload your SSH data CSV
```

### Cell 2: Determining Tidal Constituents
```python
# Run this cell to analyze tidal constituents
# Modify parameters as needed
input_file = "your_ssh_data.csv"
constituent_count = 8  # Change this to analyze more/fewer constituents
```

### Cell 3: Predicting Tidal Signal
```python
# Run this cell to generate the predicted tidal signal
# Interactive widgets appear for customization
```

### Cell 4: Calculating Storm Surge Residuals
```python
# Run this cell to extract the storm surge signal
# Plots show original, tidal, and residual components
```

### Cell 5: Filtering and Event Detection
```python
# Interactive filter customization
cutoff_hours = 12  # Adjust the filter cutoff frequency
filter_order = 3   # Adjust the Butterworth filter order
threshold = 2.0    # Set detection threshold (sigma units)
```

### Cell 6: Visualization and Reporting
```python
# Generate comprehensive visualizations and reports
# Export results to your Google Drive if desired
```

## 🔬 Methodology

Our approach combines several key techniques:

1. **Tidal Harmonic Analysis**
   - Decomposes SSH signal into known constituents (M2, S2, K1, etc.)
   - Uses linear regression with sine and cosine terms

2. **Storm Surge Extraction**
   - Storm Surge = Original SSH - Predicted Tide

3. **Signal Filtering**
   - Butterworth low-pass filter with customizable parameters

4. **Event Detection**
   - Multiple threshold options (statistical or absolute)
   - Automated event grouping and characterization

## 📈 Example Results

| Event Date & Time | Surge (m) | Direction | Duration |
|-------------------|-----------|-----------|----------|
| 2022-03-15 08:00  | +0.4532   | Positive  | 18.0 h   |
| 2022-10-27 14:00  | -0.3981   | Negative  | 12.5 h   |
| 2022-01-22 21:00  | +0.3754   | Positive  | 15.0 h   |
| 2022-09-08 03:00  | -0.3421   | Negative  | 9.5 h    |
| 2022-05-31 16:00  | +0.3102   | Positive  | 8.0 h    |

## 🧠 Why Google Colab?

- ✅ Zero setup time
- ✅ Interactive parameters
- ✅ Educational experience
- ✅ Free GPU acceleration
- ✅ Version control and Drive integration
- ✅ Shareable and collaborative

## 📚 Citations

If you use this code in your research, please cite:

```bibtex
@software{storm_surge_detection_model,
  author = {Eftekhari, Alireza},
  title = {Storm Surge Detection Model},
  url = {https://github.com/eftekhari-alireza/eftekhari-alireza.github.io/tree/main/Storm%20Surge%20Detection%20Model},
  year = {2025}
}
```

## 📧 Contact

**Alireza Eftekhari**  
📨 a.eftekhari2@universityofgalway.ie  
🔗 [Project Link](https://github.com/eftekhari-alireza/eftekhari-alireza.github.io/tree/main/Storm%20Surge%20Detection%20Model)

---

Helping to understand and predict coastal hazards through advanced tidal analysis - now more accessible than ever with Google Colab!
